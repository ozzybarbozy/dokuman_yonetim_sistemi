import os
import math
from datetime import datetime
from pathlib import Path
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, send_from_directory, abort, send_file
)
from flask_login import login_required, current_user
from flask import current_app
from werkzeug.utils import secure_filename
from ..models.document import Document, DocumentSequence
from ..models.settings import Originator, DocumentType, Discipline, Category, BuildingCode
from .. import db
from ..forms.document import DocumentUploadForm
from ..utils import log_activity, generate_document_number, validate_file
from functools import wraps

# Create blueprint for document
document_bp = Blueprint('documents', __name__, url_prefix='/documents')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@document_bp.route('/')
@login_required
def index():
    search_query = request.args.get('query', '').lower()
    filter_category = request.args.get('filter_category', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Document.query
    if search_query:
        query = query.filter(
            db.or_(
                Document.filename.ilike(f'%{search_query}%'),
                Document.description.ilike(f'%{search_query}%')
            )
        )
    if filter_category:
        query = query.filter_by(category=filter_category)

    total_docs = query.count()
    documents = query.order_by(Document.upload_date.desc()) \
                     .offset((page - 1) * per_page) \
                     .limit(per_page) \
                     .all()
    total_pages = math.ceil(total_docs / per_page) if total_docs else 1
    return render_template('document/index.html',
                        documents=documents,
                        search_query=search_query,
                        filter_category=filter_category,
                        current_page=page,
                        total_pages=total_pages,
                        per_page=per_page,
                        total_docs=total_docs)

@document_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload():
    form = DocumentUploadForm()
    
    # Populate form choices
    form.originator.choices = [(o.id, o.code) for o in Originator.query.order_by(Originator.code)]
    form.document_type.choices = [(t.id, t.code) for t in DocumentType.query.order_by(DocumentType.code)]
    form.discipline.choices = [(d.id, d.code) for d in Discipline.query.order_by(Discipline.code)]
    form.category.choices = [(c.id, c.code) for c in Category.query.order_by(Category.code)]
    form.building_code.choices = [(b.id, b.code) for b in BuildingCode.query.order_by(BuildingCode.code)]
    
    if form.validate_on_submit():
        try:
            # Get the next sequence number
            sequence = DocumentSequence.query.filter_by(
                originator_id=form.originator.data,
                document_type_id=form.document_type.data,
                discipline_id=form.discipline.data,
                category_id=form.category.data,
                building_code_id=form.building_code.data
            ).first()
            
            if not sequence:
                sequence = DocumentSequence(
                    originator_id=form.originator.data,
                    document_type_id=form.document_type.data,
                    discipline_id=form.discipline.data,
                    category_id=form.category.data,
                    building_code_id=form.building_code.data,
                    next_number=1
                )
                db.session.add(sequence)
                db.session.commit()
            
            # Generate document number
            originator = Originator.query.get(form.originator.data)
            doc_type = DocumentType.query.get(form.document_type.data)
            discipline = Discipline.query.get(form.discipline.data)
            category = Category.query.get(form.category.data)
            building_code = BuildingCode.query.get(form.building_code.data)
            
            doc_number = f"{originator.code}-{doc_type.code}-{discipline.code}-{category.code}-{building_code.code}-{sequence.next_number:03d}"
            
            # Save the file
            file = form.file.data
            filename = f"{doc_number}{Path(file.filename).suffix}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Create document record
            document = Document(
                document_number=doc_number,
                filename=filename,
                originator_id=form.originator.data,
                document_type_id=form.document_type.data,
                discipline_id=form.discipline.data,
                category_id=form.category.data,
                building_code_id=form.building_code.data,
                description=form.description.data,
                uploader_id=current_user.id
            )
            
            # Update sequence number
            sequence.next_number += 1
            
            db.session.add(document)
            db.session.commit()
            
            flash('Document uploaded successfully!', 'success')
            return redirect(url_for('documents.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error uploading document: {str(e)}', 'error')
    
    return render_template('document/upload.html', form=form)

@document_bp.route('/download/<filename>')
@login_required
def download_file(filename):
    safe_filename = secure_filename(filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)
    if not os.path.exists(file_path):
        flash('File not found', 'error')
        return redirect(url_for('documents.index'))
    doc = Document.query.filter_by(filename=safe_filename).first()
    if not doc:
        abort(403)
    log_activity('download', safe_filename)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], safe_filename, as_attachment=True)

@document_bp.route('/delete/<filename>')
@login_required
def delete_file(filename):
    if current_user.role != 'admin':
        abort(403)
    safe_filename = secure_filename(filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)
    doc = Document.query.filter_by(filename=safe_filename).first()
    if not doc:
        flash('File not found in database', 'error')
        return redirect(url_for('documents.index'))
    try:
        db.session.delete(doc)
        db.session.commit()
        if os.path.exists(file_path):
            os.remove(file_path)
        log_activity('delete', safe_filename)
        flash('File deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('File deletion error', 'error')
    return redirect(url_for('documents.index'))

@document_bp.route('/preview/<filename>')
@login_required
def preview_file(filename):
    file_ext = filename.rsplit('.', 1)[-1].lower()
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(file_path):
        flash("Dosya bulunamadı", "error")
        return redirect(url_for('documents.index'))

    # PDF ve TXT dosyalarını doğrudan göster
    if file_ext in ['pdf', 'txt']:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

    # DOCX, XLSX vb. için Google Docs Viewer ile yönlendirme
    if file_ext in ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']:
        file_url = url_for('documents.public_download', filename=filename, _external=True)
        viewer_url = f"https://docs.google.com/gview?url={file_url}&embedded=true"
        return redirect(viewer_url)

    # Diğer desteklenmeyen uzantılar
    flash("Bu dosya türü için önizleme desteklenmiyor.", "error")
    return redirect(url_for('documents.index'))

@document_bp.route('/public_download/<filename>')
def public_download(filename):
    safe_filename = secure_filename(filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)
    if not os.path.exists(file_path):
        abort(404)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], safe_filename)

import os
import math
from datetime import datetime
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, send_from_directory, abort
)
from flask_login import login_required, current_user
from flask import current_app
from werkzeug.utils import secure_filename
from models import Document, DocumentSequence
from extensions import db
from app import log_activity, generate_document_number, validate_file

document_bp = Blueprint('documents', __name__)

@document_bp.route('/documents')
@login_required
def documents():
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
    return render_template('index.html',
                           documents=documents,
                           search_query=search_query,
                           filter_category=filter_category,
                           current_page=page,
                           total_pages=total_pages,
                           per_page=per_page)

@document_bp.route('/download/<filename>')
@login_required
def download_file(filename):
    safe_filename = secure_filename(filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)
    if not os.path.exists(file_path):
        flash('File not found', 'error')
        return redirect(url_for('documents.documents'))
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
        return redirect(url_for('documents.documents'))
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
    return redirect(url_for('documents.documents'))

@document_bp.route('/preview/<filename>')
@login_required
def preview_file(filename):
    file_ext = filename.rsplit('.', 1)[-1].lower()
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(file_path):
        flash("Dosya bulunamadı", "error")
        return redirect(url_for('documents.documents'))

    # PDF ve TXT dosyalarını doğrudan göster
    if file_ext in ['pdf', 'txt']:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

    # DOCX, XLSX vb. için Google Docs Viewer ile yönlendirme (login olmadan erişilebilir hale getiriyoruz)
    if file_ext in ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']:
        file_url = url_for('documents.public_download', filename=filename, _external=True)
        viewer_url = f"https://docs.google.com/gview?url={file_url}&embedded=true"
        return redirect(viewer_url)

    # Diğer desteklenmeyen uzantılar
    flash("Bu dosya türü için önizleme desteklenmiyor.", "error")
    return redirect(url_for('documents.documents'))

@document_bp.route('/public_download/<filename>')
def public_download(filename):
    safe_filename = secure_filename(filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)
    if not os.path.exists(file_path):
        abort(404)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], safe_filename)

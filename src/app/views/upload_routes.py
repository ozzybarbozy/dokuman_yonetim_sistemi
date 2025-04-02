import os
import re
from datetime import datetime
from flask import (
    Blueprint, request, redirect,
    url_for, flash, render_template
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import (
    Document, DocumentSequence,
    Originator, DocumentType, Discipline,
    BuildingCode, Category
)
from extensions import db
from app import log_activity, validate_file, generate_document_number
from utils.filename_parser import parse_and_validate_filename

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/admin/upload')
@login_required
def admin_upload_form():
    if current_user.role != 'admin':
        flash("Bu sayfaya yalnızca yöneticiler erişebilir.", "error")
        return redirect(url_for('documents.documents'))

    originators = Originator.query.order_by(Originator.code).all()
    document_types = DocumentType.query.order_by(DocumentType.code).all()
    disciplines = Discipline.query.order_by(Discipline.code).all()
    building_codes = BuildingCode.query.order_by(BuildingCode.code).all()
    categories = Category.query.order_by(Category.code).all()

    return render_template(
        'upload.html',
        originators=originators,
        document_types=document_types,
        disciplines=disciplines,
        building_codes=building_codes,
        categories=categories
    )

@upload_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if current_user.role != 'admin':
        flash("Bu işlem sadece yöneticiler tarafından yapılabilir.", "error")
        return redirect(url_for('documents.documents'))

    if 'file' not in request.files:
        flash('Dosya seçilmedi', 'error')
        return redirect(url_for('documents.documents'))

    file = request.files['file']
    if file.filename == '':
        flash('Dosya adı boş olamaz', 'error')
        return redirect(url_for('documents.documents'))

    filename = secure_filename(file.filename)
    base_name, ext = os.path.splitext(filename)
    ext = ext.lower().strip('.')

    allowed_extensions = {'pdf', 'docx', 'txt', 'xlsx', 'dwg', 'jpg', 'jpeg', 'png'}
    max_file_size = 10 * 1024 * 1024  # 10 MB

    if ext not in allowed_extensions:
        flash(f"'{ext}' uzantılı dosyalar desteklenmiyor", 'error')
        return redirect(url_for('documents.documents'))

    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)
    if file_length > max_file_size:
        flash('Dosya 10 MB sınırını aşıyor', 'error')
        return redirect(url_for('documents.documents'))

    description = request.form.get('description', '')
    category = request.form.get('category', '')
    revision = 0
    document_number = None

    parsed = parse_and_validate_filename(base_name)

    if parsed:
        originator = parsed['originator']
        doc_type = parsed['document_type']
        discipline = parsed['discipline']
        building_code = parsed['building_code']
        revision = parsed['revision']
        document_number = base_name
    else:
        # Manuel formdan alınan bilgilerle numara üret
        originator = request.form.get('originator')
        doc_type = request.form.get('document_type')
        discipline = request.form.get('discipline')
        building_code = request.form.get('building_code')

        if not all([originator, doc_type, discipline, building_code]):
            flash("Lütfen tüm alanları doldurun veya geçerli bir dosya adı kullanın.", "error")
            return redirect(url_for('documents.documents'))

        document_number = generate_document_number(originator, doc_type, discipline, building_code, revision)

    filename = f"{document_number}.{ext}"
    upload_folder = os.getenv('UPLOAD_FOLDER', 'uploads')
    file_path = os.path.join(upload_folder, filename)
    counter = 1
    while os.path.exists(file_path):
        filename = f"{document_number}_{counter}.{ext}"
        file_path = os.path.join(upload_folder, filename)
        counter += 1

    try:
        file.save(file_path)

        new_doc = Document(
            filename=filename,
            description=description,
            upload_date=datetime.utcnow(),
            user_id=current_user.id,
            category=category,
            project_code="SPP2",
            revision=revision,
            document_number=document_number
        )
        db.session.add(new_doc)
        db.session.commit()
        log_activity('upload', filename)
        flash('Dosya başarıyla yüklendi', 'success')

    except Exception as e:
        db.session.rollback()
        flash('Dosya yüklenirken bir hata oluştu', 'error')

    return redirect(url_for('documents.documents'))

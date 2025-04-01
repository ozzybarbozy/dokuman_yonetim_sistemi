from flask import Blueprint, send_from_directory, current_app
import os

public_bp = Blueprint('public', __name__)

@public_bp.route('/public_download/<filename>')
def public_download(filename):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    return "Dosya bulunamadı", 404

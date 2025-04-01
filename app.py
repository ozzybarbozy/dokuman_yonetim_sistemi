import os
import base64
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from io import BytesIO
import mimetypes
import filetype

from flask import (
    Flask, render_template, request, redirect,
    url_for, send_from_directory, flash, abort, jsonify
)
from flask_login import (
    LoginManager, current_user
)
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

from models import User, DocumentSequence
from extensions import db

# Yükle .env
load_dotenv()

# === Loglama ayarları ===
def configure_logging():
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(os.path.join(log_dir, 'app.log'), encoding='utf-8', maxBytes=10_000_000, backupCount=5),
            logging.StreamHandler()
        ]
    )
    if os.name == 'nt':
        try:
            from ctypes import windll
            windll.kernel32.SetConsoleOutputCP(65001)
        except Exception:
            pass

configure_logging()
logger = logging.getLogger(__name__)

# === Flask Uygulaması ===
app = Flask(__name__)
app.config.from_object('config.Config')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'instance', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# === Eklentiler ===
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# === Ortak yardımcılar ===
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def guess_mime_from_bytes(data: bytes):
    kind = filetype.guess(data)
    return kind.mime if kind else None

def validate_file(file_storage):
    filename = file_storage.filename
    ext = os.path.splitext(filename)[1].lower().strip('.')
    if ext not in app.config['ALLOWED_EXTENSIONS']:
        raise ValueError(f"Disallowed file extension: {ext}")
    file_storage.seek(0)
    data = file_storage.read()
    file_storage.seek(0)
    detected_mime = guess_mime_from_bytes(data)
    if not detected_mime:
        raise ValueError("Could not guess file type from content.")
    if detected_mime not in app.config['ALLOWED_MIME_TYPES']:
        raise ValueError(f"Disallowed file type: {detected_mime}")
    return True

def log_activity(action, filename=None):
    logger.info("User: %s - Action: %s - File: %s", 
                current_user.username if current_user.is_authenticated else "Anonymous", 
                action, filename or 'None')

def generate_document_number(originator, document_type, discipline, building_code, revision):
    default_project_code = "SPP2"
    default_revision_format = "R%02d"

    seq = DocumentSequence.query.filter_by(
        originator=originator,
        document_type=document_type,
        discipline=discipline,
        building_code=building_code
    ).first()

    if not seq:
        seq = DocumentSequence(
            originator=originator,
            document_type=document_type,
            discipline=discipline,
            building_code=building_code,
            next_sequence=1
        )
        db.session.add(seq)

    sequence_number = seq.next_sequence
    seq.next_sequence += 1
    db.session.commit()

    revision_str = default_revision_format % revision
    document_number = f"{originator}-{default_project_code}-{document_type}-{discipline}-{building_code}-{sequence_number:03d}_{revision_str}"
    return document_number

# === Blueprint kayıtları ===
from views.auth_routes import auth_bp
app.register_blueprint(auth_bp)

from views.document_routes import document_bp
app.register_blueprint(document_bp)

from views.upload_routes import upload_bp
app.register_blueprint(upload_bp)

from views.admin_settings_routes import settings_bp
app.register_blueprint(settings_bp)

from views.users_routes import users_bp
app.register_blueprint(users_bp)

from views.preview_routes import preview_bp
app.register_blueprint(preview_bp)

from views.public_routes import public_bp
app.register_blueprint(public_bp)

# === Favicon ===
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# === Global güvenlik & hata yönetimi ===
@app.before_request
def before_request():
    if not current_user.is_authenticated:
        if request.endpoint:
            if request.endpoint.startswith("static"):
                return  # static dosyalar için engel olma
            if request.endpoint in ['auth.login', 'auth.logout']:
                return  # giriş çıkış işlemleri için engel olma
        return redirect(url_for('auth.login', next=request.url))

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'error': 'Not found'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"Server error: {str(e)}")
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500

# === Uygulama çalıştırma ===
if __name__ == '__main__':
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])

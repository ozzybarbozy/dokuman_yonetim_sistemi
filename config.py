import os
from pathlib import Path
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    # Güvenlik
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32))
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY', os.urandom(32))

    # Veritabanı
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///{BASE_DIR / 'instance' / 'app.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Dosya Yükleme
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'xlsx', 'dwg', 'jpg', 'jpeg', 'png'}
    ALLOWED_MIME_TYPES = {
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/plain',
        'image/jpeg',
        'image/png',
    }

    # PDF önizleme için Poppler
    POPPLER_PATH = os.getenv("POPPLER_PATH", r"C:\Release-24.08.0-0\poppler-24.08.0\Library\bin")

    # Oturum
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    PERMANENT_SESSION_LIFETIME = int(os.getenv('SESSION_LIFETIME', 3600))

    # Loglama
    LOG_DIR = BASE_DIR / 'logs'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY') or os.urandom(32)
    
    # Database
    DATABASE_FILE = Path(__file__).parent / 'instance' / 'app.db'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_FILE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Uploads
    UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'xlsx', 'dwg', 'jpg', 'jpeg', 'png'}
    ALLOWED_MIME_TYPES = {
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'image/jpeg',
        'image/png',
        # DWG için: MIME tipi değişkenlik gösterebilir, gerekirse ekleyin.
    }
    POPPLER_PATH = r"C:\Release-24.08.0-0\poppler-24.08.0\Library\bin"

    # Session
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

    # Logging
    LOG_DIR = Path(__file__).parent / 'logs'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    TEMPLATES_AUTO_RELOAD = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    DATABASE_FILE = ':memory:'

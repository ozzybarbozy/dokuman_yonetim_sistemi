import os
from pathlib import Path
from . import Config

# Get the absolute path to the instance directory
BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / 'instance'

# Create instance directory if it doesn't exist
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

# Convert Windows path to SQLite compatible format
DB_PATH = str(INSTANCE_DIR / 'app.db').replace('\\', '/')

# Create uploads directory
UPLOADS_DIR = INSTANCE_DIR / 'uploads'
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    REMEMBER_COOKIE_HTTPONLY = False
    
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Ensure instance path is set
    INSTANCE_PATH = str(INSTANCE_DIR)
    
    # Upload configuration
    UPLOAD_FOLDER = str(UPLOADS_DIR)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Cache configuration
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Debug settings
    TESTING = False

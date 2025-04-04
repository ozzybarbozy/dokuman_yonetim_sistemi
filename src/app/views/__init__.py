# This file makes the directory a Python package

from .auth import auth_bp
from .document_routes import document_bp
from .upload_routes import upload_bp
from .admin_settings_routes import settings_bp
from .users_routes import users_bp
from .preview_routes import preview_bp
from .public import public_bp

__all__ = ['auth_bp', 'document_bp', 'upload_bp', 'users_bp', 'preview_bp', 'public_bp', 'settings_bp']

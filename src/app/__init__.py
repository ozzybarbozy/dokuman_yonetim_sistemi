from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
bcrypt = Bcrypt()
cache = Cache()
csrf = CSRFProtect()

def create_app(config_name='development'):
    """Application factory function."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(f'config.{config_name}')
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cache.init_app(app)
    csrf.init_app(app)
    
    # Register blueprints
    from .views.auth import auth_bp
    from .views.document import document_bp
    from .views.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(admin_bp)
    
    return app 
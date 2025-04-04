# This file makes the directory a Python package

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models to ensure they are registered with SQLAlchemy
from .user import User
from .document import Document, DocumentSequence
from .settings import Originator, DocumentType, Discipline, Category, BuildingCode

# Create a list of all models
models = [
    User,
    Document,
    DocumentSequence,
    Originator,
    DocumentType,
    Discipline,
    Category,
    BuildingCode
]

# Register all models with SQLAlchemy
for model in models:
    if not hasattr(model, '_sa_registry'):
        model.metadata = db.metadata
        model.query = db.session.query_property()

__all__ = ['db'] + [model.__name__ for model in models]

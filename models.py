from extensions import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    document_number = db.Column(db.String(50))
    description = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category = db.Column(db.String(50))
    project_code = db.Column(db.String(50))
    revision = db.Column(db.Integer, default=1)

class DocumentSequence(db.Model):
    __tablename__ = 'document_sequences'
    id = db.Column(db.Integer, primary_key=True)
    originator = db.Column(db.String(50), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    discipline = db.Column(db.String(50), nullable=False)
    building_code = db.Column(db.String(50), nullable=False)
    next_sequence = db.Column(db.Integer, nullable=False, default=1)

    __table_args__ = (
        db.UniqueConstraint('originator', 'document_type', 'discipline', 'building_code', name='uq_doc_seq'),
    )

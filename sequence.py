# sequence.py
from extensions import db

class DocumentSequence(db.Model):
    __tablename__ = 'document_sequences'
    id = db.Column(db.Integer, primary_key=True)
    originator = db.Column(db.String(50), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    discipline = db.Column(db.String(50), nullable=False)
    building_code = db.Column(db.String(50), nullable=False)
    next_sequence = db.Column(db.Integer, default=1, nullable=False)

    # Bir kombinasyonun benzersiz olmasını sağlamak için (originator, document_type, discipline, building_code) benzersiz olmalıdır.
    __table_args__ = (db.UniqueConstraint('originator', 'document_type', 'discipline', 'building_code', name='uix_doc_seq'),)

from .. import db

class DocumentSequence(db.Model):
    __tablename__ = 'document_sequences'

    id = db.Column(db.Integer, primary_key=True)
    originator_id = db.Column(db.Integer, db.ForeignKey('originators.id'), nullable=False)
    document_type_id = db.Column(db.Integer, db.ForeignKey('document_types.id'), nullable=False)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    building_code_id = db.Column(db.Integer, db.ForeignKey('building_codes.id'), nullable=False)
    next_number = db.Column(db.Integer, default=1, nullable=False)

    # Relationships
    originator = db.relationship('Originator', backref=db.backref('sequences', lazy=True))
    document_type = db.relationship('DocumentType', backref=db.backref('sequences', lazy=True))
    discipline = db.relationship('Discipline', backref=db.backref('sequences', lazy=True))
    category = db.relationship('Category', backref=db.backref('sequences', lazy=True))
    building_code = db.relationship('BuildingCode', backref=db.backref('sequences', lazy=True))

    def __repr__(self):
        return f'<DocumentSequence {self.id}>'

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    document_number = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    originator_id = db.Column(db.Integer, db.ForeignKey('originators.id'), nullable=False)
    document_type_id = db.Column(db.Integer, db.ForeignKey('document_types.id'), nullable=False)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    building_code_id = db.Column(db.Integer, db.ForeignKey('building_codes.id'), nullable=False)

    # Relationships
    uploader = db.relationship('User', backref=db.backref('documents', lazy=True))
    originator = db.relationship('Originator', backref=db.backref('documents', lazy=True))
    document_type = db.relationship('DocumentType', backref=db.backref('documents', lazy=True))
    discipline = db.relationship('Discipline', backref=db.backref('documents', lazy=True))
    category = db.relationship('Category', backref=db.backref('documents', lazy=True))
    building_code = db.relationship('BuildingCode', backref=db.backref('documents', lazy=True))

    def __repr__(self):
        return f'<Document {self.document_number}>'

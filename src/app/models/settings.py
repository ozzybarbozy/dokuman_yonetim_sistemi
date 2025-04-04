from .. import db

class Originator(db.Model):
    __tablename__ = 'originators'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Originator {self.code}>'

class DocumentType(db.Model):
    __tablename__ = 'document_types'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<DocumentType {self.code}>'

class Discipline(db.Model):
    __tablename__ = 'disciplines'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Discipline {self.code}>'

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Category {self.code}>'

class BuildingCode(db.Model):
    __tablename__ = 'building_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<BuildingCode {self.code}>'

# Register all models with SQLAlchemy
for model in [Originator, DocumentType, Discipline, Category, BuildingCode]:
    if not hasattr(model, '_sa_registry'):
        model.metadata = db.metadata
        model.query = db.session.query_property()

__all__ = ['Originator', 'DocumentType', 'Discipline', 'Category', 'BuildingCode'] 
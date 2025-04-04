import os
import sys
import time
from pathlib import Path

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.app import create_app, db
from src.app.models import (
    User, Document, DocumentSequence,
    Originator, DocumentType, Discipline,
    Category, BuildingCode
)

def init_db():
    app = create_app()
    
    # Remove existing database file if it exists
    db_path = os.path.join(app.root_path, '..', 'instance', 'app.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Existing database file removed.")
    
    with app.app_context():
        # Ensure all models are registered
        all_models = [
            User, Document, DocumentSequence,
            Originator, DocumentType, Discipline,
            Category, BuildingCode
        ]
        
        # Register all models with SQLAlchemy
        for model in all_models:
            if not hasattr(model, '_sa_registry'):
                model.metadata = db.metadata
                model.query = db.session.query_property()
                print(f"Registered model: {model.__name__}")
        
        # Create tables in the correct order to satisfy foreign key constraints
        print("\nCreating database tables...")
        print("Available models:", [model.__name__ for model in all_models])
        
        try:
            # Create all tables at once
            print("\nCreating all tables...")
            db.create_all()
            db.session.commit()
            print("All tables created successfully.")
            
            # Verify tables were created
            inspector = db.inspect(db.engine)
            created_tables = inspector.get_table_names()
            print("\nCreated tables:", created_tables)
            
            # Check if all expected tables were created
            expected_tables = ['users', 'documents', 'document_sequences', 
                             'originators', 'document_types', 'disciplines',
                             'categories', 'building_codes']
            missing_tables = [table for table in expected_tables if table not in created_tables]
            if missing_tables:
                print("\nWARNING: The following tables were not created:", missing_tables)
                print("This may indicate a problem with model registration.")
                sys.exit(1)
            
            # Create admin user if it doesn't exist
            admin = User.query.filter_by(email='admin@example.com').first()
            if not admin:
                admin = User(
                    email='admin@example.com',
                    is_admin=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
            
            # Add initial settings data
            print("\nAdding initial settings data...")
            
            # Originators
            originators = [
                ('KLN', 'KLN'),
                ('SPP', 'SPP'),
                ('SUB', 'SUB')
            ]
            for code, desc in originators:
                if not Originator.query.filter_by(code=code).first():
                    db.session.add(Originator(code=code, description=desc))
            
            # Document Types
            document_types = [
                ('ITP', 'Inspection and Test Plan'),
                ('DRW', 'Drawing'),
                ('SPC', 'Specification'),
                ('CAL', 'Calculation')
            ]
            for code, desc in document_types:
                if not DocumentType.query.filter_by(code=code).first():
                    db.session.add(DocumentType(code=code, description=desc))
            
            # Disciplines
            disciplines = [
                ('CV', 'Civil'),
                ('EL', 'Electrical'),
                ('ME', 'Mechanical'),
                ('PL', 'Piping')
            ]
            for code, desc in disciplines:
                if not Discipline.query.filter_by(code=code).first():
                    db.session.add(Discipline(code=code, description=desc))
            
            # Categories
            categories = [
                ('IFR', 'Issued for Review'),
                ('OFR', 'Issued for Construction'),
                ('MFR', 'Issued for Manufacturing')
            ]
            for code, desc in categories:
                if not Category.query.filter_by(code=code).first():
                    db.session.add(Category(code=code, description=desc))
            
            # Building Codes
            building_codes = [
                ('ES01', 'Energy Storage Building 1'),
                ('ES02', 'Energy Storage Building 2'),
                ('ES03', 'Energy Storage Building 3')
            ]
            for code, desc in building_codes:
                if not BuildingCode.query.filter_by(code=code).first():
                    db.session.add(BuildingCode(code=code, description=desc))
            
            db.session.commit()
            print("Initial settings data added successfully!")
            print("Database initialization completed successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"\nError during database initialization: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    init_db() 
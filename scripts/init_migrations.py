import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.app import create_app, db
from flask_migrate import init, migrate, upgrade

def init_migrations():
    app = create_app()
    with app.app_context():
        # Initialize migrations directory
        init()
        # Create initial migration
        migrate(message='Initial migration')
        # Apply the migration
        upgrade()

if __name__ == '__main__':
    init_migrations() 
import os
from pathlib import Path

def create_initial_files():
    """Create initial file structure for the application."""
    # Create directories
    directories = [
        'src/app/models',
        'src/app/views',
        'src/app/utils',
        'src/app/static',
        'src/app/templates',
        'config',
        'data',
        'scripts',
        'tests',
        'docs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create __init__.py files
    init_files = [
        'src/app/__init__.py',
        'src/app/models/__init__.py',
        'src/app/views/__init__.py',
        'src/app/utils/__init__.py',
        'tests/__init__.py'
    ]
    
    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write('# This file makes the directory a Python package\n')
        print(f"Created file: {init_file}")
    
    # Create view files
    view_files = [
        'src/app/views/auth.py',
        'src/app/views/document.py',
        'src/app/views/admin.py',
        'src/app/views/users.py',
        'src/app/views/preview.py',
        'src/app/views/public.py'
    ]
    
    for view_file in view_files:
        with open(view_file, 'w') as f:
            f.write('from flask import Blueprint\n\n')
            f.write(f'# Create blueprint for {Path(view_file).stem}\n')
            f.write(f'{Path(view_file).stem}_bp = Blueprint(\'{Path(view_file).stem}\', __name__)\n\n')
            f.write('@{0}_bp.route(\'/\')\n'.format(Path(view_file).stem))
            f.write('def index():\n')
            f.write('    return "Hello from {}"\n'.format(Path(view_file).stem))
        print(f"Created file: {view_file}")
    
    # Create model files
    model_files = [
        'src/app/models/user.py',
        'src/app/models/document.py',
        'src/app/models/sequence.py'
    ]
    
    for model_file in model_files:
        with open(model_file, 'w') as f:
            f.write('from .. import db\n\n')
            f.write(f'class {Path(model_file).stem.capitalize()}(db.Model):\n')
            f.write('    __tablename__ = \'{}\'\n\n'.format(Path(model_file).stem))
            f.write('    id = db.Column(db.Integer, primary_key=True)\n')
            f.write('    # Add your model fields here\n')
        print(f"Created file: {model_file}")
    
    # Create utility files
    util_files = [
        'src/app/utils/helpers.py',
        'src/app/utils/sequence.py'
    ]
    
    for util_file in util_files:
        with open(util_file, 'w') as f:
            f.write('# Utility functions for {}\n'.format(Path(util_file).stem))
            f.write('def example_function():\n')
            f.write('    pass\n')
        print(f"Created file: {util_file}")
    
    # Create configuration file
    with open('config/development.py', 'w') as f:
        f.write('import os\n\n')
        f.write('class DevelopmentConfig:\n')
        f.write('    SECRET_KEY = os.environ.get(\'SECRET_KEY\') or \'dev\'\n')
        f.write('    SQLALCHEMY_DATABASE_URI = os.environ.get(\'DATABASE_URL\') or \\\n')
        f.write('        \'sqlite:///instance/app.db\'\n')
        f.write('    SQLALCHEMY_TRACK_MODIFICATIONS = False\n')
    print("Created file: config/development.py")
    
    print("Initial file structure created successfully!")

if __name__ == '__main__':
    create_initial_files() 
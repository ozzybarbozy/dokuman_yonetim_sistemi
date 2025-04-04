import os
import shutil
from pathlib import Path

def cleanup_project():
    """Clean up and optimize project structure."""
    # Get current directory
    current_dir = Path.cwd()
    
    # Files and directories to remove
    items_to_remove = [
        # Backup files
        '*.bak',
        # Duplicate virtual environments
        'venv/',
        # Unnecessary files
        'sqlite3.exe',
        'Sheet2.txt',
        # Old migration files
        'migrations/',
        # Duplicate directories
        'utils/',
        'views/',
        'templates/',
        'static/',
        # Old project directory
        'dokuman_yonetim_sistemi/',
        # Cache directories
        '__pycache__/',
        '.pytest_cache/',
        # Log files
        'app.log',
        'app.log.1',
        # Old configuration files
        '.flaskenv.bak',
        '.env.bak',
        'render.yaml.bak',
        'procfile',
        'insert_code.sql',
        'auto-push.ps1.bak',
        'auto-push.bat.bak',
        'run_tests.bat.bak',
        'setup_test_env.bat.bak',
        'pytest.ini.bak',
        'requirements.txt.bak',
        'requirements-dev.txt.bak',
        '.gitignore.bak',
        'README.md.bak'
    ]
    
    # Remove items
    for item in items_to_remove:
        if '*' in item:
            # Handle glob patterns
            for file in current_dir.glob(item):
                if file.is_file():
                    try:
                        file.unlink()
                        print(f"Removed file: {file}")
                    except Exception as e:
                        print(f"Error removing {file}: {str(e)}")
        else:
            # Handle single files/directories
            path = current_dir / item
            if path.exists():
                try:
                    if path.is_dir():
                        shutil.rmtree(path)
                        print(f"Removed directory: {path}")
                    else:
                        path.unlink()
                        print(f"Removed file: {path}")
                except Exception as e:
                    print(f"Error removing {path}: {str(e)}")
    
    # Create optimized directory structure
    directories = [
        'src/app/models',
        'src/app/views',
        'src/app/utils',
        'src/app/static',
        'src/app/templates',
        'src/app/forms',
        'src/app/schemas',
        'src/app/services',
        'src/app/middleware',
        'config',
        'data',
        'scripts',
        'tests',
        'docs',
        'logs',
        'uploads',
        'migrations'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create essential files
    essential_files = {
        'README.md': '# Document Management System\n\nA Flask-based document management system.',
        '.gitignore': '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Logs
logs/
*.log

# Database
*.db
*.sqlite3

# Testing
.coverage
htmlcov/
.pytest_cache/

# OS
.DS_Store
Thumbs.db

# Project specific
instance/
uploads/
''',
        'requirements.txt': '''Flask==2.0.1
Flask-SQLAlchemy==2.5.1
Flask-Login==0.5.0
Flask-Migrate==3.1.0
Flask-Bcrypt==0.7.1
Flask-Caching==1.10.1
Flask-WTF==0.15.1
SQLAlchemy==1.4.23
Werkzeug==2.0.1
python-dotenv==0.19.0
''',
        'requirements-dev.txt': '''-r requirements.txt
pytest==6.2.5
pytest-cov==2.12.1
black==21.7b0
flake8==3.9.2
isort==5.9.3
''',
        '.env': '''FLASK_APP=src.app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/app.db
''',
        '.flaskenv': '''FLASK_APP=src.app
FLASK_ENV=development
'''
    }
    
    for file_name, content in essential_files.items():
        with open(file_name, 'w') as f:
            f.write(content)
        print(f"Created file: {file_name}")
    
    print("Project cleanup and optimization completed!")

if __name__ == '__main__':
    cleanup_project() 
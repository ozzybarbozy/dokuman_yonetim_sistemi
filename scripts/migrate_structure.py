import os
import shutil
from pathlib import Path

def migrate_structure():
    """Migrate the project to the new structure."""
    # Create necessary directories
    directories = [
        'src/app/models',
        'src/app/views',
        'src/app/utils',
        'src/app/static/css',
        'src/app/static/js',
        'src/app/static/img',
        'src/app/templates/auth',
        'src/app/templates/admin',
        'tests/test_models',
        'tests/test_views',
        'tests/test_utils',
        'scripts',
        'config',
        'data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Move files to their new locations
    moves = [
        ('models.py', 'src/app/models/__init__.py'),
        ('views/*', 'src/app/views/'),
        ('utils/*', 'src/app/utils/'),
        ('static/*', 'src/app/static/'),
        ('templates/*', 'src/app/templates/'),
        ('tests/*', 'tests/'),
        ('*.py', 'scripts/'),
        ('*.xlsx', 'data/'),
        ('config.py', 'config/'),
        ('requirements*.txt', '.'),
        ('*.yaml', '.'),
        ('*.md', '.'),
        ('*.bat', '.'),
        ('*.ps1', '.'),
        ('*.ini', '.'),
        ('.env', '.'),
        ('.flaskenv', '.'),
        ('.gitignore', '.')
    ]
    
    for pattern, dest in moves:
        for file in Path('.').glob(pattern):
            if file.is_file():
                try:
                    if os.path.exists(dest) and os.path.isdir(dest):
                        # If destination is a directory, append filename
                        dest_path = os.path.join(dest, file.name)
                    else:
                        dest_path = dest
                    
                    if os.path.exists(dest_path):
                        # Backup existing file
                        backup_path = f"{dest_path}.bak"
                        shutil.move(dest_path, backup_path)
                        print(f"Backed up existing file to {backup_path}")
                    
                    shutil.move(str(file), dest_path)
                    print(f"Moved {file} to {dest_path}")
                except Exception as e:
                    print(f"Error moving {file}: {str(e)}")
    
    # Create __init__.py files
    init_files = [
        'src/app/models',
        'src/app/views',
        'src/app/utils',
        'src/app/templates/auth',
        'src/app/templates/admin',
        'tests/test_models',
        'tests/test_views',
        'tests/test_utils',
        'config'
    ]
    
    for directory in init_files:
        init_path = os.path.join(directory, '__init__.py')
        if not os.path.exists(init_path):
            with open(init_path, 'w') as f:
                f.write('# This file makes the directory a Python package\n')
    
    print("Migration completed successfully!")

if __name__ == '__main__':
    migrate_structure() 
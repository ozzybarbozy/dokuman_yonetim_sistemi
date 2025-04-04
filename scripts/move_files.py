import os
import shutil
from pathlib import Path

def move_files():
    """Move files to their new locations."""
    # Get the current directory
    current_dir = Path.cwd()
    
    # Define source and destination mappings
    moves = [
        # Models
        ('models.py', 'src/app/models/__init__.py'),
        
        # Views
        ('views/auth_routes.py', 'src/app/views/auth.py'),
        ('views/document_routes.py', 'src/app/views/document.py'),
        ('views/admin_settings_routes.py', 'src/app/views/admin.py'),
        ('views/users_routes.py', 'src/app/views/users.py'),
        ('views/preview_routes.py', 'src/app/views/preview.py'),
        ('views/public_routes.py', 'src/app/views/public.py'),
        
        # Utils
        ('utils/*', 'src/app/utils/'),
        ('helpers.py', 'src/app/utils/helpers.py'),
        ('sequence.py', 'src/app/utils/sequence.py'),
        
        # Static files
        ('static/*', 'src/app/static/'),
        
        # Templates
        ('templates/*', 'src/app/templates/'),
        
        # Configuration
        ('config.py', 'config/development.py'),
        
        # Data files
        ('*.xlsx', 'data/'),
        
        # Scripts
        ('import_codes.py', 'scripts/import_codes.py'),
        ('check_codes.py', 'scripts/check_codes.py'),
        ('auto_push.py', 'scripts/auto_push.py'),
        
        # Tests
        ('test_app.py', 'tests/test_app.py'),
        ('tests/*', 'tests/'),
    ]
    
    # Move files
    for src, dest in moves:
        if '*' in src:
            # Handle glob patterns
            for file in current_dir.glob(src):
                if file.is_file():
                    try:
                        dest_path = current_dir / dest / file.name
                        if dest_path.exists():
                            backup_path = dest_path.with_suffix(dest_path.suffix + '.bak')
                            shutil.move(str(dest_path), str(backup_path))
                            print(f"Backed up existing file to {backup_path}")
                        os.makedirs(dest_path.parent, exist_ok=True)
                        shutil.move(str(file), str(dest_path))
                        print(f"Moved {file} to {dest_path}")
                    except Exception as e:
                        print(f"Error moving {file}: {str(e)}")
        else:
            # Handle single files
            src_path = current_dir / src
            if not src_path.exists():
                print(f"Source file not found: {src_path}")
                continue
                
            try:
                if (current_dir / dest).is_dir():
                    dest_path = current_dir / dest / src_path.name
                else:
                    dest_path = current_dir / dest
                
                if dest_path.exists():
                    backup_path = dest_path.with_suffix(dest_path.suffix + '.bak')
                    shutil.move(str(dest_path), str(backup_path))
                    print(f"Backed up existing file to {backup_path}")
                
                os.makedirs(dest_path.parent, exist_ok=True)
                shutil.move(str(src_path), str(dest_path))
                print(f"Moved {src_path} to {dest_path}")
            except Exception as e:
                print(f"Error moving {src_path}: {str(e)}")
    
    print("File movement completed!")

if __name__ == '__main__':
    move_files() 
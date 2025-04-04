import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.app import create_app
from src.app.models.user import User

app = create_app()

with app.app_context():
    # Check admin user
    admin = User.query.filter_by(email='admin@example.com').first()
    if admin:
        print(f"Admin user found: {admin.email}")
        print(f"is_admin: {admin.is_admin}")
    else:
        print("Admin user not found")

    # Check registered routes
    print("\nRegistered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

    # Check registered blueprints
    print("\nRegistered blueprints:")
    for name, blueprint in app.blueprints.items():
        print(f"{name}: {blueprint}") 
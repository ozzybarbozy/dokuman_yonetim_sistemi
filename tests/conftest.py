import pytest
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.app import create_app, db
from src.app.models import User, Document

@pytest.fixture
def client():
    """Create a test client for the app."""
    app = create_app('testing')
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def test_user():
    """Create a test user."""
    user = User(
        username='testuser',
        password='testpassword',
        role='user',
        first_name='Test',
        last_name='User'
    )
    return user

@pytest.fixture
def test_document():
    """Create a test document."""
    document = Document(
        filename='test_document.pdf',
        document_number='TEST-001',
        description='Test document',
        category='test',
        project_code='TEST'
    )
    return document 
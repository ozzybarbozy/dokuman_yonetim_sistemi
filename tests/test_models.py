import pytest
from models import User, Document, DocumentSequence

def test_user_creation(test_user):
    """Test user creation and properties."""
    assert test_user.username == 'testuser'
    assert test_user.role == 'user'
    assert test_user.first_name == 'Test'
    assert test_user.last_name == 'User'

def test_document_creation(test_document):
    """Test document creation and properties."""
    assert test_document.filename == 'test_document.pdf'
    assert test_document.document_number == 'TEST-001'
    assert test_document.description == 'Test document'
    assert test_document.category == 'test'
    assert test_document.project_code == 'TEST'

def test_document_sequence_creation():
    """Test document sequence creation and properties."""
    sequence = DocumentSequence(
        originator='TEST',
        document_type='DOC',
        discipline='ENG',
        building_code='B001',
        next_sequence=1
    )
    assert sequence.originator == 'TEST'
    assert sequence.document_type == 'DOC'
    assert sequence.discipline == 'ENG'
    assert sequence.building_code == 'B001'
    assert sequence.next_sequence == 1 
import pytest
from flask import url_for

def test_index_route(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 302  # Should redirect to login

def test_login_route(client):
    """Test the login route."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Giri\xc5\x9f Yap' in response.data  # Check for Turkish "Giriş Yap"

def test_upload_route_unauthorized(client):
    """Test upload route without authentication."""
    response = client.get('/upload')
    assert response.status_code == 302  # Should redirect to login

def test_admin_route_unauthorized(client):
    """Test admin route without authentication."""
    response = client.get('/admin')
    assert response.status_code == 302  # Should redirect to login

def test_document_list_route_unauthorized(client):
    """Test document list route without authentication."""
    response = client.get('/documents')
    assert response.status_code == 302  # Should redirect to login 
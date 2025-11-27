"""
Tests for authentication endpoints
"""
import pytest
import json
from api.app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client


def test_login_success(client):
    """Test successful login"""
    response = client.post(
        '/api/v1/auth/login',
        data=json.dumps({
            'username': 'admin',
            'password': 'admin123'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['user']['username'] == 'admin'
    assert data['user']['role'] == 'admin'


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post(
        '/api/v1/auth/login',
        data=json.dumps({
            'username': 'admin',
            'password': 'wrong_password'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data


def test_login_missing_credentials(client):
    """Test login with missing credentials"""
    response = client.post(
        '/api/v1/auth/login',
        data=json.dumps({
            'username': 'admin'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_refresh_token(client):
    """Test token refresh"""
    # First, login to get tokens
    login_response = client.post(
        '/api/v1/auth/login',
        data=json.dumps({
            'username': 'admin',
            'password': 'admin123'
        }),
        content_type='application/json'
    )
    
    refresh_token = login_response.get_json()['refresh_token']
    
    # Use refresh token to get new access token
    response = client.post(
        '/api/v1/auth/refresh',
        headers={'Authorization': f'Bearer {refresh_token}'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data


def test_get_current_user(client):
    """Test get current user endpoint"""
    # Login first
    login_response = client.post(
        '/api/v1/auth/login',
        data=json.dumps({
            'username': 'admin',
            'password': 'admin123'
        }),
        content_type='application/json'
    )
    
    access_token = login_response.get_json()['access_token']
    
    # Get current user
    response = client.get(
        '/api/v1/auth/me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['user']['username'] == 'admin'


def test_protected_endpoint_without_token(client):
    """Test accessing protected endpoint without token"""
    response = client.get('/api/v1/auth/me')
    
    assert response.status_code == 401


def test_register_new_user(client):
    """Test user registration"""
    response = client.post(
        '/api/v1/auth/register',
        data=json.dumps({
            'username': 'newuser',
            'password': 'newpass123'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['user']['username'] == 'newuser'
    assert data['user']['role'] == 'user'


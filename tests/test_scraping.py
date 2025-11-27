"""
Tests for scraping endpoints
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


@pytest.fixture
def admin_token(client):
    """Get admin access token"""
    response = client.post(
        '/api/v1/auth/login',
        data=json.dumps({
            'username': 'admin',
            'password': 'admin123'
        }),
        content_type='application/json'
    )
    return response.get_json()['access_token']


@pytest.fixture
def user_token(client):
    """Get regular user access token"""
    response = client.post(
        '/api/v1/auth/login',
        data=json.dumps({
            'username': 'user',
            'password': 'user123'
        }),
        content_type='application/json'
    )
    return response.get_json()['access_token']


def test_trigger_scraping_as_admin(client, admin_token):
    """Test triggering scraping as admin"""
    response = client.post(
        '/api/v1/scraping/trigger',
        data=json.dumps({
            'pages': 1,
            'format': 'json',
            'output': 'test_books'
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 202
    data = response.get_json()
    assert 'job_id' in data
    assert data['parameters']['pages'] == 1


def test_trigger_scraping_as_user(client, user_token):
    """Test triggering scraping as regular user (should fail)"""
    response = client.post(
        '/api/v1/scraping/trigger',
        data=json.dumps({
            'pages': 1
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {user_token}'}
    )
    
    assert response.status_code == 403


def test_trigger_scraping_without_token(client):
    """Test triggering scraping without token"""
    response = client.post(
        '/api/v1/scraping/trigger',
        data=json.dumps({
            'pages': 1
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 401


def test_trigger_scraping_invalid_params(client, admin_token):
    """Test triggering scraping with invalid parameters"""
    response = client.post(
        '/api/v1/scraping/trigger',
        data=json.dumps({
            'pages': 100  # Too many pages
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 400


def test_list_jobs_as_admin(client, admin_token):
    """Test listing scraping jobs as admin"""
    response = client.get(
        '/api/v1/scraping/jobs',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'jobs' in data
    assert 'total' in data


def test_get_job_status(client, admin_token):
    """Test getting job status"""
    # First trigger a job
    trigger_response = client.post(
        '/api/v1/scraping/trigger',
        data=json.dumps({
            'pages': 1
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    job_id = trigger_response.get_json()['job_id']
    
    # Get job status
    response = client.get(
        f'/api/v1/scraping/jobs/{job_id}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['job_id'] == job_id
    assert 'status' in data


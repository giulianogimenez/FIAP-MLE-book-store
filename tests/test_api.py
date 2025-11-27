"""
Tests for the API module
"""
import pytest
from api.app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_get_books(client):
    """Test get all books endpoint"""
    response = client.get('/api/v1/books')
    assert response.status_code == 200
    data = response.get_json()
    assert 'books' in data
    assert 'total' in data


def test_get_book_by_id(client):
    """Test get book by ID"""
    response = client.get('/api/v1/books/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'book' in data


def test_get_nonexistent_book(client):
    """Test get nonexistent book"""
    response = client.get('/api/v1/books/999')
    assert response.status_code == 404


def test_create_book(client):
    """Test create new book"""
    new_book = {
        'title': 'Test Book',
        'author': 'Test Author',
        'isbn': '978-1234567890',
        'price': 29.99,
        'category': 'Test'
    }
    response = client.post('/api/v1/books', json=new_book)
    assert response.status_code == 201
    data = response.get_json()
    assert data['book']['title'] == 'Test Book'


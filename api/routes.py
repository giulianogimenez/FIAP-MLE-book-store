"""
API Routes and Endpoints
"""
from flask import Blueprint, jsonify, request
from api.controllers.book_controller import BookController

api_bp = Blueprint('api', __name__)
book_controller = BookController()


@api_bp.route('/books', methods=['GET'])
def get_books():
    """
    Get all books
    Query params: page, limit, search
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    search = request.args.get('search', '', type=str)
    
    result = book_controller.get_all_books(page=page, limit=limit, search=search)
    return jsonify(result)


@api_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Get a specific book by ID
    """
    result = book_controller.get_book_by_id(book_id)
    if result.get('error'):
        return jsonify(result), 404
    return jsonify(result)


@api_bp.route('/books', methods=['POST'])
def create_book():
    """
    Create a new book
    """
    data = request.get_json()
    result = book_controller.create_book(data)
    return jsonify(result), 201


@api_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Update an existing book
    """
    data = request.get_json()
    result = book_controller.update_book(book_id, data)
    if result.get('error'):
        return jsonify(result), 404
    return jsonify(result)


@api_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Delete a book
    """
    result = book_controller.delete_book(book_id)
    if result.get('error'):
        return jsonify(result), 404
    return jsonify(result)


@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get statistics about the book collection
    """
    result = book_controller.get_statistics()
    return jsonify(result)


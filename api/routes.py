"""
API Routes and Endpoints

Follows Dependency Inversion Principle (DIP):
- Routes depend on abstractions (controllers)
- Controllers are injected with dependencies (repositories)
"""
import logging
import pandas as pd
from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from api.controllers.book_controller import BookController
from api.repositories.book_repository import BookRepository
from api.auth.decorators import admin_required

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Dependency Injection: Controller depends on Repository
book_repository = BookRepository(data_file='data/output/books.json')
book_controller = BookController(repository=book_repository)


@api_bp.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    """
    Listar todos os livros (requer autenticação)
    ---
    tags:
      - Books
    security:
      - Bearer: []
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: "Número da página (mínimo: 1)"
        minimum: 1
      - name: limit
        in: query
        type: integer
        default: 10
        description: "Livros por página (mínimo: 1, máximo: 100)"
        minimum: 1
        maximum: 100
      - name: search
        in: query
        type: string
        description: Buscar por título ou autor
    responses:
      200:
        description: Lista de livros
        schema:
          type: object
          properties:
            books:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  title:
                    type: string
                    example: Clean Code
                  author:
                    type: string
                    example: Robert C. Martin
                  isbn:
                    type: string
                    example: 978-0132350884
                  price:
                    type: number
                    example: 39.99
                  category:
                    type: string
                    example: Technology
            total:
              type: integer
              example: 2
            page:
              type: integer
              example: 1
            limit:
              type: integer
              example: 10
            total_pages:
              type: integer
              example: 1
      400:
        description: Parâmetros inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Bad Request"
            message:
              type: string
              example: "Invalid page number: 0. Page must be >= 1"
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    search = request.args.get('search', '', type=str)
    
    try:
        result = book_controller.get_all_books(page=page, limit=limit, search=search)
        return jsonify(result)
    except ValueError as e:
        return jsonify({
            'error': 'Bad Request',
            'message': str(e)
        }), 400


@api_bp.route('/books/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):
    """
    Buscar livro específico por ID (requer autenticação)
    ---
    tags:
      - Books
    security:
      - Bearer: []
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID do livro
    responses:
      200:
        description: Detalhes do livro
        schema:
          type: object
          properties:
            book:
              type: object
              properties:
                id:
                  type: integer
                title:
                  type: string
                author:
                  type: string
                isbn:
                  type: string
                price:
                  type: number
                category:
                  type: string
      404:
        description: Livro não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: Book not found
    """
    result = book_controller.get_book_by_id(book_id)
    if result.get('error'):
        return jsonify(result), 404
    return jsonify(result)


@api_bp.route('/books/search', methods=['GET'])
@jwt_required()
def search_books():
    """
    Buscar livros por título e/ou categoria (requer autenticação)
    ---
    tags:
      - Books
    security:
      - Bearer: []
    parameters:
      - name: title
        in: query
        type: string
        required: false
        description: "Buscar por título (parcial, case-insensitive)"
        example: "Python"
      - name: category
        in: query
        type: string
        required: false
        description: "Buscar por categoria (exata, case-insensitive)"
        example: "Technology"
    responses:
      200:
        description: Lista de livros encontrados
        schema:
          type: object
          properties:
            books:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  title:
                    type: string
                    example: "Python Machine Learning"
                  author:
                    type: string
                    example: "Sebastian Raschka"
                  isbn:
                    type: string
                    example: "978-1789955750"
                  price:
                    type: number
                    example: 44.99
                  category:
                    type: string
                    example: "Technology"
            total:
              type: integer
              example: 2
              description: "Número total de livros encontrados"
        examples:
          application/json:
            books:
              - id: 1
                title: "Python Machine Learning"
                author: "Sebastian Raschka"
                isbn: "978-1789955750"
                price: 44.99
                category: "Technology"
              - id: 2
                title: "Clean Code"
                author: "Robert C. Martin"
                isbn: "978-0132350884"
                price: 39.99
                category: "Technology"
            total: 2
    """
    title = request.args.get('title', None, type=str)
    category = request.args.get('category', None, type=str)
    
    result = book_controller.search_books(title=title, category=category)
    return jsonify(result)


@api_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """
    Obter estatísticas da coleção (requer autenticação)
    ---
    tags:
      - Books
    security:
      - Bearer: []
    responses:
      200:
        description: Estatísticas da coleção de livros
        schema:
          type: object
          properties:
            total_books:
              type: integer
              example: 10
              description: Total de livros na coleção
            average_price:
              type: number
              example: 42.50
              description: Preço médio dos livros
            categories:
              type: object
              description: Contagem de livros por categoria
              example:
                Technology: 5
                Fiction: 3
                Business: 2
    """
    result = book_controller.get_statistics()
    return jsonify(result)


@api_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """
    Listar todas as categorias de livros disponíveis (requer autenticação)
    ---
    tags:
      - Books
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de categorias disponíveis
        schema:
          type: object
          properties:
            categories:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                    example: Technology
                    description: Nome da categoria
                  count:
                    type: integer
                    example: 5
                    description: Número de livros nesta categoria
            total:
              type: integer
              example: 3
              description: Número total de categorias disponíveis
        examples:
          application/json:
            categories:
              - name: Fiction
                count: 3
              - name: Technology
                count: 5
              - name: Business
                count: 2
            total: 3
    """
    result = book_controller.get_categories()
    return jsonify(result)


@api_bp.route('/metrics', methods=['GET'])
def metrics_dashboard():
    """
    Admin Dashboard - Métricas e Monitoramento da API (com autenticação integrada)
    ---
    tags:
      - Metrics
    responses:
      200:
        description: Dashboard de métricas ou página de login (HTML)
        content:
          text/html:
            schema:
              type: string
    """
    # Render login page with integrated authentication
    return render_template('metrics_login.html')


@api_bp.route('/reload', methods=['POST'])
@jwt_required()
@admin_required()
def force_reload():
    """
    Forçar reload imediato dos dados (admin only)
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: Dados recarregados com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: Data reloaded successfully
            books_count:
              type: integer
              example: 600
              description: Total de livros após reload
            timestamp:
              type: string
              format: date-time
              description: Momento do reload
      401:
        description: Não autorizado
      403:
        description: Acesso negado (apenas admin)
    """
    try:
        book_repository.reload()
        books_count = book_repository.count()
        logger.info(f"Manual reload triggered by admin - {books_count} books loaded")
        
        return jsonify({
            'message': 'Data reloaded successfully',
            'books_count': books_count,
            'timestamp': pd.Timestamp.now(tz='UTC').isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error during manual reload: {e}")
        return jsonify({
            'error': 'Reload failed',
            'message': str(e)
        }), 500

"""
API Routes and Endpoints
"""
from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from api.controllers.book_controller import BookController
from api.auth.decorators import admin_required

api_bp = Blueprint('api', __name__)
book_controller = BookController()


@api_bp.route('/books', methods=['GET'])
def get_books():
    """
    Listar todos os livros
    ---
    tags:
      - Books
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: Número da página
      - name: limit
        in: query
        type: integer
        default: 10
        description: Livros por página
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
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    search = request.args.get('search', '', type=str)
    
    result = book_controller.get_all_books(page=page, limit=limit, search=search)
    return jsonify(result)


@api_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Buscar livro específico por ID
    ---
    tags:
      - Books
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
def search_books():
    """
    Buscar livros por título e/ou categoria
    ---
    tags:
      - Books
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
def get_stats():
    """
    Obter estatísticas da coleção
    ---
    tags:
      - Books
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
def get_categories():
    """
    Listar todas as categorias de livros disponíveis
    ---
    tags:
      - Books
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

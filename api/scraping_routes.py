"""
Scraping API Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.auth.decorators import admin_required
from api.controllers.scraping_controller import ScrapingController

scraping_bp = Blueprint('scraping', __name__)
scraping_controller = ScrapingController()


@scraping_bp.route('/trigger', methods=['POST'])
@jwt_required()
@admin_required()
def trigger_scraping():
    """
    Iniciar job de web scraping (Admin only)
    ---
    tags:
      - Scraping
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer {access_token} - Requer role admin
        default: Bearer your_admin_access_token_here
      - name: body
        in: body
        required: false
        description: Parâmetros do scraping (todos opcionais)
        schema:
          type: object
          properties:
            url:
              type: string
              example: "http://books.toscrape.com"
              description: "URL base para scraping (padrão: http://books.toscrape.com)"
            pages:
              type: integer
              example: 3
              minimum: 1
              maximum: 50
              description: "Número de páginas a fazer scraping (padrão: 2)"
            format:
              type: string
              enum:
                - json
                - csv
                - both
              example: both
              description: "Formato de saída (padrão: both)"
            output:
              type: string
              example: books
              description: "Nome do arquivo de saída (padrão: books)"
    responses:
      202:
        description: Job de scraping iniciado
        schema:
          type: object
          properties:
            message:
              type: string
              example: Scraping job started
            job_id:
              type: string
              example: job_1
              description: ID do job para acompanhamento
            parameters:
              type: object
              properties:
                url:
                  type: string
                pages:
                  type: integer
                format:
                  type: string
                output:
                  type: string
      400:
        description: Parâmetros inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: Invalid pages parameter
            message:
              type: string
      401:
        description: Não autenticado
      403:
        description: Acesso negado - Requer role admin
        schema:
          type: object
          properties:
            error:
              type: string
              example: Admin access required
            message:
              type: string
    """
    current_user = get_jwt_identity()
    data = request.get_json() or {}
    
    result, status_code = scraping_controller.trigger_scraping(data)
    
    return jsonify(result), status_code


@scraping_bp.route('/jobs/<job_id>', methods=['GET'])
@jwt_required()
@admin_required()
def get_job_status(job_id):
    """
    Obter status de um job de scraping (Admin only)
    ---
    tags:
      - Scraping
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer {access_token} - Requer role admin
        default: Bearer your_admin_access_token_here
      - name: job_id
        in: path
        type: string
        required: true
        description: ID do job de scraping
        example: job_1
    responses:
      200:
        description: Status do job
        schema:
          type: object
          properties:
            job_id:
              type: string
              example: job_1
            status:
              type: string
              enum:
                - pending
                - running
                - completed
                - failed
              example: completed
            parameters:
              type: object
              properties:
                url:
                  type: string
                pages:
                  type: integer
                format:
                  type: string
                output:
                  type: string
            results:
              type: object
              description: Presente quando status é completed
              properties:
                books_count:
                  type: integer
                  example: 40
                  description: Total de livros coletados
                files:
                  type: array
                  items:
                    type: string
                  example: [data/output/books.json, data/output/books.csv]
                  description: Arquivos gerados
                report:
                  type: object
                  description: Relatório do scraping
            error:
              type: string
              description: Presente quando status é failed
      401:
        description: Não autenticado
      403:
        description: Acesso negado - Requer role admin
      404:
        description: Job não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: Job not found
            message:
              type: string
    """
    result, status_code = scraping_controller.get_job_status(job_id)
    
    return jsonify(result), status_code


@scraping_bp.route('/jobs', methods=['GET'])
@jwt_required()
@admin_required()
def list_jobs():
    """
    Listar todos os jobs de scraping (Admin only)
    ---
    tags:
      - Scraping
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer {access_token} - Requer role admin
        default: Bearer your_admin_access_token_here
    responses:
      200:
        description: Lista de jobs de scraping
        schema:
          type: object
          properties:
            jobs:
              type: array
              items:
                type: object
                properties:
                  job_id:
                    type: string
                    example: job_1
                  status:
                    type: string
                    enum:
                      - pending
                      - running
                      - completed
                      - failed
                    example: completed
                url:
                  type: string
                  example: "http://books.toscrape.com"
                  pages:
                    type: integer
                    example: 3
            total:
              type: integer
              example: 5
              description: Total de jobs
      401:
        description: Não autenticado
      403:
        description: Acesso negado - Requer role admin
    """
    result, status_code = scraping_controller.list_jobs()
    
    return jsonify(result), status_code

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
    Trigger a scraping job (Admin only)
    
    Headers:
        Authorization: Bearer <access_token>
    
    Request body:
        {
            "url": "http://books.toscrape.com",  // optional
            "pages": 3,                            // optional, default: 2
            "format": "both",                      // optional, default: both (json, csv, both)
            "output": "books"                      // optional, default: books
        }
    
    Response:
        {
            "message": "Scraping job started",
            "job_id": "job_1",
            "parameters": {
                "url": "...",
                "pages": 3,
                "format": "both",
                "output": "books"
            }
        }
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
    Get status of a scraping job (Admin only)
    
    Headers:
        Authorization: Bearer <access_token>
    
    Response:
        {
            "job_id": "job_1",
            "status": "completed",
            "parameters": {...},
            "results": {
                "books_count": 40,
                "files": ["data/output/books.json", "data/output/books.csv"],
                "report": {...}
            }
        }
    """
    result, status_code = scraping_controller.get_job_status(job_id)
    
    return jsonify(result), status_code


@scraping_bp.route('/jobs', methods=['GET'])
@jwt_required()
@admin_required()
def list_jobs():
    """
    List all scraping jobs (Admin only)
    
    Headers:
        Authorization: Bearer <access_token>
    
    Response:
        {
            "jobs": [
                {
                    "job_id": "job_1",
                    "status": "completed",
                    "url": "...",
                    "pages": 3
                }
            ],
            "total": 1
        }
    """
    result, status_code = scraping_controller.list_jobs()
    
    return jsonify(result), status_code


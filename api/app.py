"""
Flask REST API Application
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from api.config import Config
from api.routes import api_bp
from api.auth.routes import auth_bp
from api.scraping_routes import scraping_bp
from api.swagger_config import swagger_config, swagger_template


def create_app(config_class=Config):
    """
    Application factory pattern
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize Swagger
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token expired',
            'message': 'The token has expired'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'error': 'Invalid token',
            'message': 'Signature verification failed'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'error': 'Authorization required',
            'message': 'Request does not contain an access token'
        }), 401
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(scraping_bp, url_prefix='/api/v1/scraping')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        """
        Health check da API
        ---
        tags:
          - Health
        responses:
          200:
            description: API está saudável
        """
        return jsonify({
            'status': 'healthy',
            'service': 'book-store-api',
            'version': '2.0.0',
            'features': ['books', 'auth', 'scraping']
        })
    
    # API info endpoint
    @app.route('/api/v1')
    def api_info():
        """
        Informações sobre a API
        ---
        tags:
          - Health
        responses:
          200:
            description: Informações e endpoints disponíveis
        """
        return jsonify({
            'name': 'Book Store API',
            'version': '2.0.0',
            'documentation': '/api/v1/docs',
            'endpoints': {
                'books': '/api/v1/books',
                'auth': {
                    'login': 'POST /api/v1/auth/login',
                    'refresh': 'POST /api/v1/auth/refresh',
                    'me': 'GET /api/v1/auth/me'
                },
                'scraping': {
                    'trigger': 'POST /api/v1/scraping/trigger (admin)',
                    'jobs': 'GET /api/v1/scraping/jobs (admin)',
                    'job_status': 'GET /api/v1/scraping/jobs/<job_id> (admin)'
                }
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', True)
    )


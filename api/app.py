"""
Flask REST API Application
"""
import os
from datetime import datetime
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
        Health check completo da API
        ---
        tags:
          - Health
        responses:
          200:
            description: API está saudável
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: healthy
                service:
                  type: string
                  example: book-store-api
                version:
                  type: string
                  example: 2.0.0
                timestamp:
                  type: string
                  example: "2025-11-27T20:30:45.123456"
                checks:
                  type: object
                  properties:
                    database:
                      type: object
                    storage:
                      type: object
                    config:
                      type: object
          503:
            description: Serviço não disponível (algum check falhou)
        """
        checks = {}
        overall_status = 'healthy'
        status_code = 200
        
        # Check 1: Database (users.csv)
        users_file = 'data/users.csv'
        try:
            if os.path.exists(users_file):
                file_size = os.path.getsize(users_file)
                with open(users_file, 'r') as f:
                    line_count = len(f.readlines())
                checks['database'] = {
                    'status': 'healthy',
                    'type': 'csv',
                    'file': users_file,
                    'size_bytes': file_size,
                    'users_count': max(0, line_count - 1),  # Minus header
                    'readable': True,
                    'writable': os.access(users_file, os.W_OK)
                }
            else:
                checks['database'] = {
                    'status': 'warning',
                    'type': 'csv',
                    'file': users_file,
                    'message': 'Users file not found',
                    'readable': False
                }
                overall_status = 'degraded'
        except Exception as e:
            checks['database'] = {
                'status': 'unhealthy',
                'type': 'csv',
                'error': str(e)
            }
            overall_status = 'unhealthy'
            status_code = 503
        
        # Check 2: Storage (data/output directory)
        output_dir = 'data/output'
        try:
            # Ensure directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Test write permissions
            test_file = os.path.join(output_dir, '.health_check')
            can_write = False
            try:
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                can_write = True
            except:
                pass
            
            # Count files
            files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
            
            checks['storage'] = {
                'status': 'healthy',
                'directory': output_dir,
                'exists': True,
                'writable': can_write,
                'files_count': len(files)
            }
            
            if not can_write:
                checks['storage']['status'] = 'warning'
                checks['storage']['message'] = 'Directory not writable'
                if overall_status == 'healthy':
                    overall_status = 'degraded'
                    
        except Exception as e:
            checks['storage'] = {
                'status': 'unhealthy',
                'directory': output_dir,
                'error': str(e)
            }
            overall_status = 'unhealthy'
            status_code = 503
        
        # Check 3: Configuration
        try:
            jwt_secret = app.config.get('JWT_SECRET_KEY')
            secret_key = app.config.get('SECRET_KEY')
            
            checks['config'] = {
                'status': 'healthy',
                'jwt_configured': jwt_secret is not None and jwt_secret != 'super-secret-jwt-key-change-in-production',
                'secret_key_configured': secret_key is not None and secret_key != 'dev-secret-key-change-in-production',
                'debug_mode': app.config.get('DEBUG', False),
                'host': app.config.get('HOST', '0.0.0.0'),
                'port': app.config.get('PORT', 5000)
            }
            
            # Warn if using default secrets
            if not checks['config']['jwt_configured'] or not checks['config']['secret_key_configured']:
                checks['config']['status'] = 'warning'
                checks['config']['message'] = 'Using default secret keys (not recommended for production)'
                if overall_status == 'healthy':
                    overall_status = 'degraded'
                    
        except Exception as e:
            checks['config'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            overall_status = 'unhealthy'
            status_code = 503
        
        # Check 4: Dependencies
        try:
            import flask
            import flask_jwt_extended
            import flask_cors
            import flasgger
            import requests
            import pandas
            
            checks['dependencies'] = {
                'status': 'healthy',
                'flask': flask.__version__,
                'flask_jwt_extended': 'installed',
                'pandas': pandas.__version__,
                'requests': requests.__version__
            }
        except ImportError as e:
            checks['dependencies'] = {
                'status': 'unhealthy',
                'error': f'Missing dependency: {str(e)}'
            }
            overall_status = 'unhealthy'
            status_code = 503
        
        return jsonify({
            'status': overall_status,
            'service': 'book-store-api',
            'version': '2.0.0',
            'timestamp': datetime.utcnow().isoformat(),
            'features': ['books', 'auth', 'scraping'],
            'checks': checks
        }), status_code
    
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


"""
Swagger/OpenAPI Configuration
"""

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/api/v1/docs/apispec.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/v1/docs",
    "uiversion": 3
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Book Store API",
        "description": "API REST para gerenciamento de livros com autenticação JWT e web scraping",
        "contact": {
            "name": "FIAP MLE",
            "url": "https://github.com/giulianogimenez/FIAP-MLE-book-store",
        },
        "version": "2.0.0"
    },
    "basePath": "/",
    "schemes": [
        "https",
        "http"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "tags": [
        {
            "name": "Authentication",
            "description": "Endpoints de autenticação (login, refresh, register)"
        },
        {
            "name": "Books",
            "description": "Gerenciamento de livros (CRUD)"
        },
        {
            "name": "Scraping",
            "description": "Web scraping de livros (Admin only)"
        },
        {
            "name": "Health",
            "description": "Health check e informações da API"
        }
    ]
}


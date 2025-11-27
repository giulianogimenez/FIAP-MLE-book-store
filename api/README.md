# 📡 API REST - Book Store

Documentação técnica da API REST do Book Store.

## 📋 Índice

- [Arquitetura](#arquitetura)
- [Estrutura de Arquivos](#estrutura-de-arquivos)
- [Configuração](#configuração)
- [Endpoints](#endpoints)
- [Autenticação](#autenticação)
- [Controllers](#controllers)
- [Swagger UI](#swagger-ui)

## Arquitetura

A API segue o padrão **MVC (Model-View-Controller)** adaptado para APIs REST:

```
api/
├── app.py              # Aplicação Flask (Factory Pattern)
├── config.py           # Configurações
├── wsgi.py            # Entry point para Gunicorn
├── routes.py          # Rotas de Books
├── scraping_routes.py # Rotas de Scraping
├── swagger_config.py  # Configuração Swagger/OpenAPI
│
├── auth/              # Módulo de Autenticação
│   ├── models.py      # User model e UserRepository
│   ├── routes.py      # Endpoints de autenticação
│   └── decorators.py  # Decoradores (@admin_required)
│
└── controllers/       # Camada de Negócio
    ├── book_controller.py
    └── scraping_controller.py
```

### Fluxo de Requisição

```
Cliente → Flask Router → Auth Middleware (JWT) → Controller → Response
```

## Estrutura de Arquivos

### `app.py` - Application Factory

Cria e configura a aplicação Flask:

```python
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensões
    CORS(app)
    jwt = JWTManager(app)
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Registrar blueprints
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(scraping_bp, url_prefix='/api/v1/scraping')
    
    return app
```

### `config.py` - Configurações

Gerencia variáveis de ambiente:

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret'
    HOST = os.environ.get('API_HOST', '0.0.0.0')
    PORT = int(os.environ.get('API_PORT', 5000))
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
```

### `routes.py` - Rotas de Books

Endpoints CRUD para livros:

- `GET /api/v1/books` - Listar livros (paginação, busca)
- `GET /api/v1/books/search` - Buscar por título/categoria
- `GET /api/v1/books/:id` - Buscar por ID
- `POST /api/v1/books` - Criar livro
- `PUT /api/v1/books/:id` - Atualizar livro
- `DELETE /api/v1/books/:id` - Deletar livro
- `GET /api/v1/categories` - Listar categorias
- `GET /api/v1/stats` - Estatísticas

### `scraping_routes.py` - Rotas de Scraping

Endpoints para web scraping (requer admin):

- `POST /api/v1/scraping/trigger` - Iniciar scraping
- `GET /api/v1/scraping/jobs` - Listar jobs
- `GET /api/v1/scraping/jobs/:id` - Status do job

### `auth/` - Módulo de Autenticação

#### `auth/models.py`

Define User model e UserRepository:

```python
class User:
    def __init__(self, username, password_hash, role='user'):
        self.username = username
        self.password_hash = password_hash
        self.role = role

class UserRepository:
    def __init__(self, csv_file='data/users.csv'):
        self.csv_file = csv_file
        self.users = self._load_users()
    
    def find_by_username(self, username):
        # Buscar usuário
        
    def create_user(self, username, password, role='user'):
        # Criar novo usuário com hash bcrypt
```

#### `auth/routes.py`

Endpoints de autenticação:

- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Renovar token
- `GET /api/v1/auth/me` - Info do usuário
- `POST /api/v1/auth/register` - Registrar usuário

#### `auth/decorators.py`

Decoradores para controle de acesso:

```python
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({
                    'error': 'Admin access required'
                }), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
```

## Configuração

### Variáveis de Ambiente

Criar arquivo `.env` na raiz:

```bash
# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua-chave-secreta

# JWT
JWT_SECRET_KEY=sua-chave-jwt

# API
API_HOST=0.0.0.0
API_PORT=5000
```

### Gerar Chaves Seguras

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Endpoints

### Endpoints Públicos

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/health` | GET | Health check |
| `/api/v1` | GET | Info da API |
| `/api/v1/docs` | GET | Swagger UI |
| `/api/v1/auth/login` | POST | Login |
| `/api/v1/auth/register` | POST | Registrar |

### Endpoints Protegidos (JWT Required)

| Endpoint | Método | Role | Descrição |
|----------|--------|------|-----------|
| `/api/v1/books` | GET | user/admin | Listar livros |
| `/api/v1/books/search` | GET | user/admin | Buscar livros |
| `/api/v1/books/:id` | GET | user/admin | Buscar por ID |
| `/api/v1/books` | POST | user/admin | Criar livro |
| `/api/v1/books/:id` | PUT | user/admin | Atualizar |
| `/api/v1/books/:id` | DELETE | user/admin | Deletar |
| `/api/v1/categories` | GET | user/admin | Categorias |
| `/api/v1/stats` | GET | user/admin | Estatísticas |
| `/api/v1/auth/me` | GET | user/admin | Info usuário |
| `/api/v1/auth/refresh` | POST | user/admin | Renovar token |

### Endpoints Admin

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/v1/scraping/trigger` | POST | Iniciar scraping |
| `/api/v1/scraping/jobs` | GET | Listar jobs |
| `/api/v1/scraping/jobs/:id` | GET | Status do job |

## Autenticação

Ver documentação completa em [../docs/AUTHENTICATION.md](../docs/AUTHENTICATION.md)

### Quick Example

```python
import requests

# 1. Login
response = requests.post(
    "http://localhost:5000/api/v1/auth/login",
    json={"username": "admin", "password": "admin123"}
)
token = response.json()['access_token']

# 2. Usar token
headers = {"Authorization": f"Bearer {token}"}

# 3. Fazer requisições
books = requests.get(
    "http://localhost:5000/api/v1/books",
    headers=headers
)
```

## Controllers

### BookController

Gerencia lógica de negócio de livros:

```python
class BookController:
    def __init__(self):
        self.books = []  # In-memory storage
        self.next_id = 1
    
    def get_all_books(self, page=1, limit=10, search=''):
        # Lógica de paginação e busca
        
    def search_books(self, title=None, category=None):
        # Busca por título e/ou categoria
        
    def get_categories(self):
        # Lista categorias únicas
```

**Métodos:**
- `get_all_books(page, limit, search)` - Listar com paginação
- `get_book_by_id(book_id)` - Buscar por ID
- `create_book(data)` - Criar novo
- `update_book(book_id, data)` - Atualizar
- `delete_book(book_id)` - Deletar
- `get_statistics()` - Estatísticas
- `get_categories()` - Categorias
- `search_books(title, category)` - Busca avançada

### ScrapingController

Gerencia jobs de scraping:

```python
class ScrapingController:
    def __init__(self):
        self.jobs = {}
        self.job_counter = 0
    
    def trigger_scraping(self, params):
        # Inicia job de scraping
        
    def get_job_status(self, job_id):
        # Retorna status do job
```

## Swagger UI

### Acessar Documentação

```
http://localhost:5000/api/v1/docs
```

### Configuração

Ver `swagger_config.py`:

```python
swagger_config = {
    "headers": [],
    "specs": [{
        "endpoint": 'apispec',
        "route": '/api/v1/docs/apispec.json',
    }],
    "swagger_ui": True,
    "specs_route": "/api/v1/docs",
    "uiversion": 3
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Book Store API",
        "version": "2.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}
```

### Documentar Endpoints

Usar docstrings em YAML:

```python
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
    responses:
      200:
        description: Lista de livros
    """
    pass
```

## Executar a API

### Desenvolvimento

```bash
python run_api.py
```

### Produção (Gunicorn)

```bash
gunicorn api.wsgi:app
```

### Com Workers

```bash
gunicorn -w 4 -b 0.0.0.0:5000 api.wsgi:app
```

### Docker

```bash
docker-compose up api
```

## Testes

```bash
# Todos os testes da API
pytest tests/test_api.py tests/test_auth.py -v

# Com cobertura
pytest tests/test_api.py --cov=api
```

## Logs e Debugging

### Debug Mode

```python
# config.py
DEBUG = True
```

### Logs Personalizados

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@api_bp.route('/books')
def get_books():
    logger.info(f"Listing books, page={page}")
    # ...
```

## Performance

### Otimizações Implementadas

- ✅ Paginação em listagens
- ✅ Cache de configurações
- ✅ In-memory storage (rápido para MVP)

### Próximas Otimizações

- [ ] Implementar Redis cache
- [ ] Adicionar PostgreSQL
- [ ] Implementar rate limiting
- [ ] Adicionar compression (gzip)

## Segurança

### Implementado

- ✅ JWT authentication
- ✅ Password hashing (bcrypt)
- ✅ CORS configurado
- ✅ Role-based access control

### Recomendações Produção

- [ ] HTTPS obrigatório
- [ ] Rate limiting
- [ ] Input validation
- [ ] SQL injection protection (quando usar DB)
- [ ] XSS protection headers

---

**📖 Ver também:**
- [Quick Start](../docs/QUICK_START.md)
- [Autenticação](../docs/AUTHENTICATION.md)
- [Endpoints Detalhados](../docs/ENDPOINTS.md)
- [Troubleshooting](../docs/TROUBLESHOOTING.md)


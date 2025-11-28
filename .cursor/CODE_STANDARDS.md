# 📐 Code Standards & Best Practices

## Conduta de Código - FIAP MLE Book Store API

Este documento define os padrões de código e boas práticas a serem seguidos no desenvolvimento deste projeto.

---

## 🏛️ Princípios SOLID

### 1. **S** - Single Responsibility Principle (Princípio da Responsabilidade Única)

Cada classe deve ter **uma única responsabilidade** e **um único motivo para mudar**.

#### ✅ Boas Práticas
```python
# ✅ BOM: Cada classe tem uma responsabilidade clara
class BookController:
    """Responsável apenas pela lógica de negócio de livros"""
    def get_books(self):
        pass
    
    def search_books(self, title, category):
        pass

class BookRepository:
    """Responsável apenas pelo acesso a dados"""
    def load_books_from_csv(self):
        pass
    
    def save_books_to_csv(self):
        pass

class BookValidator:
    """Responsável apenas pela validação"""
    def validate_book_data(self, book):
        pass
```

#### ❌ Evitar
```python
# ❌ RUIM: Classe com múltiplas responsabilidades
class Book:
    def __init__(self):
        pass
    
    def load_from_csv(self):  # Responsabilidade de persistência
        pass
    
    def validate(self):  # Responsabilidade de validação
        pass
    
    def send_email_notification(self):  # Responsabilidade de notificação
        pass
```

### 2. **O** - Open/Closed Principle (Princípio Aberto/Fechado)

Classes devem estar **abertas para extensão**, mas **fechadas para modificação**.

#### ✅ Boas Práticas
```python
# ✅ BOM: Usar herança/composição para estender funcionalidade
from abc import ABC, abstractmethod

class Scraper(ABC):
    """Classe base abstrata"""
    @abstractmethod
    def scrape(self, url):
        pass

class BookScraper(Scraper):
    """Implementação específica sem modificar a base"""
    def scrape(self, url):
        # Implementação específica para livros
        pass

class ProductScraper(Scraper):
    """Nova funcionalidade por extensão, não modificação"""
    def scrape(self, url):
        # Implementação específica para produtos
        pass
```

### 3. **L** - Liskov Substitution Principle (Princípio da Substituição de Liskov)

Objetos de uma superclasse devem ser **substituíveis** por objetos de suas subclasses sem quebrar o sistema.

#### ✅ Boas Práticas
```python
# ✅ BOM: Subclasse mantém contrato da superclasse
class UserRepository:
    def find_by_username(self, username):
        """Retorna User ou None"""
        pass

class CachedUserRepository(UserRepository):
    def find_by_username(self, username):
        """Mantém mesmo contrato: retorna User ou None"""
        # Verifica cache primeiro, depois chama super()
        pass
```

#### ❌ Evitar
```python
# ❌ RUIM: Subclasse quebra contrato
class UserRepository:
    def find_by_username(self, username):
        """Retorna User ou None"""
        return user or None

class StrictUserRepository(UserRepository):
    def find_by_username(self, username):
        """Quebra contrato: lança exceção em vez de retornar None"""
        if not user:
            raise UserNotFoundException()  # ❌ Comportamento diferente!
```

### 4. **I** - Interface Segregation Principle (Princípio da Segregação de Interface)

Clientes **não devem ser forçados** a depender de interfaces que não usam.

#### ✅ Boas Práticas
```python
# ✅ BOM: Interfaces específicas e coesas
class Readable(ABC):
    @abstractmethod
    def read(self):
        pass

class Writable(ABC):
    @abstractmethod
    def write(self, data):
        pass

class CSVReader(Readable):
    """Implementa apenas o que precisa"""
    def read(self):
        pass

class CSVWriter(Writable):
    """Implementa apenas o que precisa"""
    def write(self, data):
        pass

class CSVHandler(Readable, Writable):
    """Combina quando necessário"""
    def read(self):
        pass
    
    def write(self, data):
        pass
```

#### ❌ Evitar
```python
# ❌ RUIM: Interface "gordinha" força implementação desnecessária
class DataHandler(ABC):
    @abstractmethod
    def read(self):
        pass
    
    @abstractmethod
    def write(self, data):
        pass
    
    @abstractmethod
    def delete(self):
        pass
    
    @abstractmethod
    def update(self, data):
        pass

class ReadOnlyHandler(DataHandler):
    """Forçado a implementar métodos que não usa"""
    def read(self):
        pass
    
    def write(self, data):
        raise NotImplementedError()  # ❌ Não deveria estar aqui
    
    def delete(self):
        raise NotImplementedError()  # ❌ Não deveria estar aqui
    
    def update(self, data):
        raise NotImplementedError()  # ❌ Não deveria estar aqui
```

### 5. **D** - Dependency Inversion Principle (Princípio da Inversão de Dependência)

Módulos de alto nível **não devem depender** de módulos de baixo nível. Ambos devem depender de **abstrações**.

#### ✅ Boas Práticas
```python
# ✅ BOM: Depender de abstrações
from abc import ABC, abstractmethod

class Storage(ABC):
    """Abstração"""
    @abstractmethod
    def save(self, data):
        pass

class CSVStorage(Storage):
    """Implementação concreta"""
    def save(self, data):
        # Salva em CSV
        pass

class DatabaseStorage(Storage):
    """Implementação concreta"""
    def save(self, data):
        # Salva em banco
        pass

class BookService:
    """Alto nível depende de abstração, não implementação"""
    def __init__(self, storage: Storage):
        self.storage = storage  # Pode ser CSV, Database, etc.
    
    def save_book(self, book):
        self.storage.save(book)
```

#### ❌ Evitar
```python
# ❌ RUIM: Alto nível depende de implementação concreta
class BookService:
    def __init__(self):
        self.csv_storage = CSVStorage()  # ❌ Acoplado a implementação concreta
    
    def save_book(self, book):
        self.csv_storage.save(book)  # Difícil de testar e trocar
```

---

## 🧹 Código Limpo (Clean Code)

### 1. **Nomenclatura Significativa**

#### ✅ Boas Práticas
```python
# ✅ BOM: Nomes descritivos e auto-explicativos
def calculate_average_price(books):
    """Calcula preço médio dos livros"""
    total_price = sum(book.price for book in books)
    book_count = len(books)
    return total_price / book_count if book_count > 0 else 0

user_repository = UserRepository()
authenticated_user = user_repository.find_by_username("admin")
```

#### ❌ Evitar
```python
# ❌ RUIM: Nomes genéricos e confusos
def calc(b):
    t = sum(x.p for x in b)
    n = len(b)
    return t / n if n > 0 else 0

ur = UserRepository()
u = ur.find("admin")
```

### 2. **Funções Pequenas e Coesas**

Funções devem fazer **uma coisa**, fazê-la **bem**, e fazê-la **apenas**.

#### ✅ Boas Práticas
```python
# ✅ BOM: Funções pequenas, cada uma com uma responsabilidade
def authenticate_user(username, password):
    """Autentica um usuário"""
    user = find_user(username)
    if not user:
        return None
    
    if verify_password(password, user.password_hash):
        return user
    
    return None

def find_user(username):
    """Busca usuário por username"""
    return user_repository.find_by_username(username)

def verify_password(plain_password, hashed_password):
    """Verifica se a senha está correta"""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
```

#### ❌ Evitar
```python
# ❌ RUIM: Função grande fazendo muitas coisas
def process_user_login(username, password, request, session):
    """Faz login, cria sessão, loga evento, envia email..."""
    # 50+ linhas de código misturando múltiplas responsabilidades
    user = user_repository.find_by_username(username)
    if not user:
        log_failed_attempt(username, request.remote_addr)
        send_security_email(username)
        return None
    # ... mais 40 linhas
```

### 3. **Comentários Quando Necessário**

Código deve ser **auto-explicativo**. Comentários devem explicar **por quê**, não **o quê**.

#### ✅ Boas Práticas
```python
# ✅ BOM: Docstrings e comentários úteis
def search_books(title=None, category=None):
    """
    Busca livros por título e/ou categoria.
    
    Args:
        title (str, optional): Título parcial (case-insensitive)
        category (str, optional): Categoria exata (case-insensitive)
    
    Returns:
        dict: {'books': [...], 'total': int}
    """
    results = self.books
    
    # Filtro parcial no título para melhor UX de busca
    if title:
        title_lower = title.lower()
        results = [book for book in results if title_lower in book.get('title', '').lower()]
    
    # Categoria usa match exato para consistência com /api/v1/categories
    if category:
        category_lower = category.lower()
        results = [book for book in results if book.get('category', '').lower() == category_lower]
    
    return {'books': results, 'total': len(results)}
```

#### ❌ Evitar
```python
# ❌ RUIM: Comentários óbvios ou desatualizados
def search_books(title=None, category=None):
    # Pega os livros
    results = self.books
    
    # Se tiver título
    if title:
        # Converte para lowercase
        title_lower = title.lower()
        # Filtra os livros
        results = [book for book in results if title_lower in book.get('title', '').lower()]
    
    # Retorna os livros  # ❌ Comentário desatualizado (retorna dict, não lista)
    return {'books': results, 'total': len(results)}
```

### 4. **Formatação Consistente**

Use **PEP 8** como guia de estilo para Python.

#### ✅ Boas Práticas
```python
# ✅ BOM: Formatação consistente e legível
class BookController:
    """Controller para gerenciar operações de livros"""
    
    def __init__(self, data_file='data/output/books.json'):
        self.data_file = data_file
        self.books = self._load_books()
    
    def get_books(self, page=1, per_page=10):
        """Retorna livros com paginação"""
        start = (page - 1) * per_page
        end = start + per_page
        
        return {
            'books': self.books[start:end],
            'total': len(self.books),
            'page': page,
            'per_page': per_page
        }
    
    def _load_books(self):
        """Carrega livros do arquivo (método privado)"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
```

### 5. **DRY - Don't Repeat Yourself**

**Evite duplicação de código**. Extraia lógica comum em funções reutilizáveis.

#### ✅ Boas Práticas
```python
# ✅ BOM: Lógica comum extraída
def fetch_with_auth(endpoint):
    """Função reutilizável para requisições autenticadas"""
    return requests.get(
        endpoint,
        headers={'Authorization': f'Bearer {get_token()}'}
    )

# Uso
health_data = fetch_with_auth('/health')
books_data = fetch_with_auth('/api/v1/books')
stats_data = fetch_with_auth('/api/v1/stats')
```

#### ❌ Evitar
```python
# ❌ RUIM: Código duplicado
health_data = requests.get('/health', headers={'Authorization': f'Bearer {get_token()}'})
books_data = requests.get('/api/v1/books', headers={'Authorization': f'Bearer {get_token()}'})
stats_data = requests.get('/api/v1/stats', headers={'Authorization': f'Bearer {get_token()}'})
```

---

## 🎯 Programação Pragmática

### 1. **KISS - Keep It Simple, Stupid**

Prefira **soluções simples** a soluções complexas.

#### ✅ Boas Práticas
```python
# ✅ BOM: Solução simples e direta
def is_admin(user):
    """Verifica se usuário é admin"""
    return user.role == 'admin'

# Uso
if is_admin(current_user):
    # Ação admin
    pass
```

#### ❌ Evitar
```python
# ❌ RUIM: Over-engineering
class RoleChecker:
    def __init__(self, role_validator_factory):
        self.validator = role_validator_factory.create_validator()
    
    def check_role(self, user, role_type):
        return self.validator.validate(user.get_role_object(), role_type.value)

# Uso complicado para algo simples
role_checker = RoleChecker(RoleValidatorFactory())
if role_checker.check_role(current_user, RoleType.ADMIN):
    pass
```

### 2. **YAGNI - You Aren't Gonna Need It**

Não implemente funcionalidade **antes** de precisar dela.

#### ✅ Boas Práticas
```python
# ✅ BOM: Implementa apenas o necessário agora
class User:
    def __init__(self, username, password_hash, role):
        self.username = username
        self.password_hash = password_hash
        self.role = role
```

#### ❌ Evitar
```python
# ❌ RUIM: Funcionalidade especulativa
class User:
    def __init__(self, username, password_hash, role):
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.avatar = None  # ❌ Não usado ainda
        self.preferences = {}  # ❌ Não usado ainda
        self.last_login_locations = []  # ❌ Não usado ainda
        self.notification_settings = {}  # ❌ Não usado ainda
```

### 3. **Fail Fast**

**Falhe rapidamente** e de forma clara quando detectar um problema.

#### ✅ Boas Práticas
```python
# ✅ BOM: Validação antecipada
@admin_required()
def trigger_scraping():
    """Endpoint protegido - falha rápido se não for admin"""
    data = request.get_json()
    
    # Validação antecipada dos parâmetros
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Processa apenas se validações passaram
    result = scraping_controller.trigger(url, data.get('pages', 2))
    return jsonify(result), 200
```

#### ❌ Evitar
```python
# ❌ RUIM: Validação tardia, erro confuso
def trigger_scraping():
    data = request.get_json()
    url = data.get('url') if data else None
    
    # Processa e só depois falha de forma confusa
    try:
        result = scraping_controller.trigger(url, data.get('pages', 2))
        return jsonify(result), 200
    except AttributeError:  # ❌ Erro genérico, difícil de debugar
        return jsonify({'error': 'Something went wrong'}), 500
```

### 4. **Código Coeso e Bem Organizado**

Agrupe código relacionado, separe código não relacionado.

#### ✅ Estrutura de Projeto
```
api/
├── __init__.py
├── app.py                    # Aplicação Flask
├── config.py                 # Configurações
├── routes.py                 # Rotas de Books
├── scraping_routes.py        # Rotas de Scraping
├── auth/                     # Módulo de autenticação
│   ├── __init__.py
│   ├── models.py            # User, UserRepository
│   ├── routes.py            # Login, refresh, register
│   └── decorators.py        # @admin_required
└── controllers/              # Lógica de negócio
    ├── book_controller.py
    └── scraping_controller.py
```

### 5. **Tratamento de Erros Adequado**

Trate erros de forma **específica** e forneça **feedback útil**.

#### ✅ Boas Práticas
```python
# ✅ BOM: Tratamento específico com feedback útil
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'status': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Internal error: {error}')
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred. Please try again later.',
        'status': 500
    }), 500

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'error': 'Token Expired',
        'message': 'The token has expired. Please refresh your token.',
        'status': 401
    }), 401
```

---

## 📋 Checklist de Qualidade

Antes de commitar código, verifique:

- [ ] **SOLID**: Código segue princípios SOLID?
- [ ] **SRP**: Cada classe/função tem uma única responsabilidade?
- [ ] **Nomenclatura**: Nomes são descritivos e auto-explicativos?
- [ ] **Funções**: São pequenas (< 20 linhas idealmente)?
- [ ] **DRY**: Não há duplicação de código?
- [ ] **KISS**: Solução é simples e direta?
- [ ] **YAGNI**: Implementei apenas o necessário?
- [ ] **Comentários**: Código é auto-explicativo? Comentários explicam "por quê"?
- [ ] **Formatação**: Segue PEP 8?
- [ ] **Erros**: Tratamento adequado com mensagens claras?
- [ ] **Testes**: Funcionalidade foi testada?
- [ ] **Documentação**: Docstrings estão presentes e atualizadas?

---

## 🎓 Referências

- **Clean Code** - Robert C. Martin
- **The Pragmatic Programmer** - Andrew Hunt & David Thomas
- **PEP 8** - Style Guide for Python Code
- **SOLID Principles** - Robert C. Martin
- **Design Patterns** - Gang of Four

---

_Este documento é um guia vivo e deve ser atualizado conforme o projeto evolui._

_Última atualização: 2025-11-28_


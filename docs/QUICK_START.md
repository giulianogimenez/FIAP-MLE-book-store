# 🚀 Quick Start Guide

Guia rápido para começar a usar o Book Store API.

## ⚡ Setup Rápido (5 minutos)

### 1. Clone e Configure

```bash
# Clone o repositório
git clone https://github.com/giulianogimenez/FIAP-MLE-book-store.git
cd FIAP-MLE-book-store

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Iniciar a API

```bash
python run_api.py
```

A API estará disponível em: **http://localhost:5000**

### 3. Acessar Swagger UI

Abra no navegador: **http://localhost:5000/api/v1/docs**

## 🔐 Login Rápido

### Usuários Padrão

| Usuário | Senha | Role |
|---------|-------|------|
| `admin` | `admin123` | admin |
| `user` | `user123` | user |

### Fazer Login via cURL

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "username": "admin",
    "role": "admin"
  }
}
```

### Usar o Token

```bash
# Salvar token
TOKEN="seu_access_token_aqui"

# Fazer requisições autenticadas
curl http://localhost:5000/api/v1/books \
  -H "Authorization: Bearer $TOKEN"
```

## 📚 Primeiras Requisições

### 1. Listar Livros

```bash
curl http://localhost:5000/api/v1/books \
  -H "Authorization: Bearer $TOKEN"
```

### 2. Buscar por Categoria

```bash
curl "http://localhost:5000/api/v1/books/search?category=Technology" \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Listar Categorias

```bash
curl http://localhost:5000/api/v1/categories \
  -H "Authorization: Bearer $TOKEN"
```

## 🕷️ Adicionar Livros via Web Scraping

> ℹ️ **Importante**: A adição, edição e exclusão de livros só pode ser feita via scraping.

### Via CLI

```bash
python run_scraper.py --pages 3 --format both
```

### Via API (requer role admin)

```bash
# Login como admin
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  > admin_login.json

ADMIN_TOKEN=$(cat admin_login.json | jq -r '.access_token')

# Iniciar scraping (adiciona livros)
curl -X POST http://localhost:5000/api/v1/scraping/trigger \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"pages": 2, "format": "json"}'
```

## 🐍 Exemplo Python

```python
import requests

# 1. Login
response = requests.post(
    "http://localhost:5000/api/v1/auth/login",
    json={"username": "admin", "password": "admin123"}
)
token = response.json()['access_token']

# 2. Headers com autenticação
headers = {"Authorization": f"Bearer {token}"}

# 3. Listar livros
books = requests.get(
    "http://localhost:5000/api/v1/books",
    headers=headers
)
print(books.json())

# 4. Buscar livros
search = requests.get(
    "http://localhost:5000/api/v1/books/search?title=Python",
    headers=headers
)
print(search.json())
```

## 🧪 Executar Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=api --cov=scraper

# Apenas autenticação
pytest tests/test_auth.py -v
```

## 🔗 Links Úteis

- **Swagger UI**: http://localhost:5000/api/v1/docs
- **Health Check**: http://localhost:5000/health
- **API Info**: http://localhost:5000/api/v1

## 📖 Próximos Passos

- [Documentação Completa da API](../api/README.md)
- [Autenticação JWT](AUTHENTICATION.md)
- [Endpoints Detalhados](ENDPOINTS.md)
- [Web Scraping](../scraper/README.md)
- [Deploy](../DEPLOYMENT.md)

## ⚠️ Troubleshooting

### Porta 5000 já está em uso

```bash
# Usar outra porta
export API_PORT=5001
python run_api.py
```

### Módulo não encontrado

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Token expirado

```bash
# Usar refresh token
curl -X POST http://localhost:5000/api/v1/auth/refresh \
  -H "Authorization: Bearer $REFRESH_TOKEN"
```

---

**✅ Pronto! Você já pode começar a usar a API!**

Para problemas mais específicos, consulte [TROUBLESHOOTING.md](TROUBLESHOOTING.md)


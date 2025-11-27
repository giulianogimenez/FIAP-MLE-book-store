# 🔐 API Authentication & Scraping Documentation

## Visão Geral

A API agora inclui:
- ✅ **Autenticação JWT** (JSON Web Tokens)
- ✅ **Sistema de Login e Refresh Token**
- ✅ **Controle de Acesso por Roles** (user, admin)
- ✅ **Endpoint de Scraping Protegido** (apenas admin)

---

## 🚀 Novos Endpoints

### Autenticação

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/v1/auth/login` | Login e obter tokens | Não |
| POST | `/api/v1/auth/refresh` | Renovar access token | Refresh Token |
| GET | `/api/v1/auth/me` | Informações do usuário | Access Token |
| POST | `/api/v1/auth/register` | Registrar novo usuário | Não |

### Scraping (Admin Only)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/v1/scraping/trigger` | Iniciar scraping | Admin |
| GET | `/api/v1/scraping/jobs` | Listar jobs | Admin |
| GET | `/api/v1/scraping/jobs/<job_id>` | Status do job | Admin |

---

## 📝 Usuários Padrão

Para testes e desenvolvimento:

```javascript
// Admin (pode fazer scraping)
{
  "username": "admin",
  "password": "admin123",
  "role": "admin"
}

// User regular (apenas consulta)
{
  "username": "user",
  "password": "user123",
  "role": "user"
}
```

---

## 🔑 1. Autenticação

### 1.1 Login

**Request:**
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "username": "admin",
    "role": "admin"
  },
  "message": "Login successful"
}
```

**Errors:**
- `400`: Credenciais faltando
- `401`: Credenciais inválidas

**Exemplo com curl:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

---

### 1.2 Refresh Token

Use o refresh token para obter um novo access token sem fazer login novamente.

**Request:**
```bash
POST /api/v1/auth/refresh
Authorization: Bearer <refresh_token>
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Token refreshed successfully"
}
```

**Exemplo com curl:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/refresh \
  -H "Authorization: Bearer <seu_refresh_token>"
```

---

### 1.3 Informações do Usuário

**Request:**
```bash
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "user": {
    "username": "admin",
    "role": "admin"
  }
}
```

**Exemplo com curl:**
```bash
curl http://localhost:5000/api/v1/auth/me \
  -H "Authorization: Bearer <seu_access_token>"
```

---

### 1.4 Registrar Usuário

**Request:**
```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "newuser",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "message": "User created successfully",
  "user": {
    "username": "newuser",
    "role": "user"
  }
}
```

---

## 🕷️ 2. Scraping (Admin Only)

### 2.1 Iniciar Scraping

**⚠️ Requer role `admin`**

**Request:**
```bash
POST /api/v1/scraping/trigger
Authorization: Bearer <admin_access_token>
Content-Type: application/json

{
  "url": "http://books.toscrape.com",  // opcional
  "pages": 3,                            // opcional, default: 2
  "format": "both",                      // opcional: json, csv, both
  "output": "books"                      // opcional, default: books
}
```

**Response (202 Accepted):**
```json
{
  "message": "Scraping job started",
  "job_id": "job_1",
  "parameters": {
    "url": "http://books.toscrape.com",
    "pages": 3,
    "format": "both",
    "output": "books"
  }
}
```

**Errors:**
- `400`: Parâmetros inválidos
- `401`: Token ausente ou inválido
- `403`: Usuário não é admin

**Exemplo com curl:**
```bash
# 1. Fazer login como admin
TOKEN=$(curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r '.access_token')

# 2. Iniciar scraping
curl -X POST http://localhost:5000/api/v1/scraping/trigger \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pages": 3,
    "format": "both",
    "output": "meus_livros"
  }'
```

---

### 2.2 Listar Jobs

**Request:**
```bash
GET /api/v1/scraping/jobs
Authorization: Bearer <admin_access_token>
```

**Response (200 OK):**
```json
{
  "jobs": [
    {
      "job_id": "job_1",
      "status": "completed",
      "url": "http://books.toscrape.com",
      "pages": 3
    },
    {
      "job_id": "job_2",
      "status": "running",
      "url": "http://books.toscrape.com",
      "pages": 5
    }
  ],
  "total": 2
}
```

**Exemplo com curl:**
```bash
curl http://localhost:5000/api/v1/scraping/jobs \
  -H "Authorization: Bearer $TOKEN"
```

---

### 2.3 Status do Job

**Request:**
```bash
GET /api/v1/scraping/jobs/<job_id>
Authorization: Bearer <admin_access_token>
```

**Response (200 OK) - Job Concluído:**
```json
{
  "job_id": "job_1",
  "status": "completed",
  "parameters": {
    "url": "http://books.toscrape.com",
    "pages": 3,
    "format": "both",
    "output": "books"
  },
  "results": {
    "books_count": 60,
    "files": [
      "data/output/books.json",
      "data/output/books.csv"
    ],
    "report": {
      "total_items": 60,
      "columns": ["title", "price", "rating", "in_stock", "url"]
    }
  }
}
```

**Response (200 OK) - Job em Andamento:**
```json
{
  "job_id": "job_2",
  "status": "running",
  "parameters": {
    "url": "http://books.toscrape.com",
    "pages": 5,
    "format": "json",
    "output": "books"
  }
}
```

**Exemplo com curl:**
```bash
curl http://localhost:5000/api/v1/scraping/jobs/job_1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔒 Segurança

### Configuração JWT

No arquivo `.env`:

```bash
# Gerar chave secreta segura
SECRET_KEY=sua_chave_super_secreta_aqui
JWT_SECRET_KEY=outra_chave_secreta_para_jwt

# Ou usar o mesmo
JWT_SECRET_KEY=$SECRET_KEY
```

**Gerar chave segura:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Expiração de Tokens

- **Access Token**: 1 hora
- **Refresh Token**: 30 dias

Configurado em `api/config.py`:
```python
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
```

---

## 📊 Fluxo Completo de Uso

### Cenário: Fazer scraping de 5 páginas

```bash
# 1. Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  > login_response.json

# 2. Extrair token
TOKEN=$(cat login_response.json | jq -r '.access_token')

# 3. Iniciar scraping
curl -X POST http://localhost:5000/api/v1/scraping/trigger \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"pages": 5, "format": "both"}' \
  > job_response.json

# 4. Extrair job_id
JOB_ID=$(cat job_response.json | jq -r '.job_id')

# 5. Verificar status (aguardar alguns segundos)
sleep 10
curl http://localhost:5000/api/v1/scraping/jobs/$JOB_ID \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.'

# 6. Listar todos os jobs
curl http://localhost:5000/api/v1/scraping/jobs \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.'
```

---

## 🐍 Exemplo Python

```python
import requests

BASE_URL = "http://localhost:5000/api/v1"

# 1. Login
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "admin", "password": "admin123"}
)
tokens = login_response.json()
access_token = tokens['access_token']

# 2. Headers com autenticação
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# 3. Iniciar scraping
scraping_response = requests.post(
    f"{BASE_URL}/scraping/trigger",
    json={
        "pages": 3,
        "format": "both",
        "output": "meus_livros"
    },
    headers=headers
)

job = scraping_response.json()
job_id = job['job_id']
print(f"Job iniciado: {job_id}")

# 4. Verificar status
import time
time.sleep(15)  # Aguardar scraping

status_response = requests.get(
    f"{BASE_URL}/scraping/jobs/{job_id}",
    headers=headers
)

status = status_response.json()
print(f"Status: {status['status']}")

if status['status'] == 'completed':
    print(f"Livros coletados: {status['results']['books_count']}")
    print(f"Arquivos: {status['results']['files']}")
```

---

## 🧪 Testes

Execute os testes:

```bash
# Todos os testes
pytest

# Apenas testes de autenticação
pytest tests/test_auth.py -v

# Apenas testes de scraping
pytest tests/test_scraping.py -v

# Com cobertura
pytest --cov=api --cov-report=html
```

---

## ❓ Erros Comuns

### 401 Unauthorized

```json
{
  "error": "Authorization required",
  "message": "Request does not contain an access token"
}
```

**Solução**: Adicione o header `Authorization: Bearer <token>`

### 403 Forbidden

```json
{
  "error": "Admin access required",
  "message": "You do not have permission to access this resource"
}
```

**Solução**: Use credenciais de admin (admin/admin123)

### 400 Bad Request

```json
{
  "error": "Invalid pages parameter",
  "message": "Pages must be an integer between 1 and 50"
}
```

**Solução**: Verifique os parâmetros enviados

---

## 🔄 Renovação de Token

Quando o access token expirar (após 1 hora):

```bash
# Use o refresh token para obter novo access token
curl -X POST http://localhost:5000/api/v1/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

---

## 📚 Recursos Adicionais

- **Postman Collection**: Importe os exemplos no Postman
- **Swagger**: Em breve (considere adicionar flask-swagger)
- **Logs**: Verifique `heroku logs` ou console local

---

## 🎯 Resumo de Endpoints

```
Autenticação:
  POST   /api/v1/auth/login       - Login
  POST   /api/v1/auth/refresh     - Refresh token
  GET    /api/v1/auth/me          - User info
  POST   /api/v1/auth/register    - Registrar

Scraping (Admin):
  POST   /api/v1/scraping/trigger - Iniciar scraping
  GET    /api/v1/scraping/jobs    - Listar jobs
  GET    /api/v1/scraping/jobs/:id - Status do job

Books (Existentes):
  GET    /api/v1/books            - Listar livros
  POST   /api/v1/books            - Criar livro
  GET    /api/v1/books/:id        - Buscar livro
  PUT    /api/v1/books/:id        - Atualizar livro
  DELETE /api/v1/books/:id        - Deletar livro
  GET    /api/v1/stats            - Estatísticas
```

---

**Versão da API**: 2.0.0  
**Última atualização**: 2025-11-27


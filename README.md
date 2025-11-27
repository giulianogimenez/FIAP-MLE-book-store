# FIAP MLE - Book Store Project

Projeto Python completo com três módulos principais:
1. **API REST** usando Flask com autenticação JWT
2. **Web Scraping** para coletar informações de livros
3. **Sistema de Autenticação** com controle de acesso por roles

## 📁 Estrutura do Projeto

```
FIAP-MLE-book-store/
├── api/                          # Módulo da API REST
│   ├── auth/                     # Sistema de autenticação
│   │   ├── models.py            # Usuários (carrega de CSV)
│   │   ├── routes.py            # Login, refresh, register
│   │   └── decorators.py        # Proteção de rotas (admin_required)
│   ├── controllers/
│   │   ├── book_controller.py   # Lógica de livros
│   │   └── scraping_controller.py # Lógica de scraping
│   ├── app.py                   # Aplicação Flask + JWT
│   ├── config.py                # Configurações
│   ├── routes.py                # Rotas de livros
│   └── scraping_routes.py       # Rotas de scraping
│
├── scraper/                      # Módulo de Web Scraping
│   ├── base_scraper.py          # Classe base
│   ├── book_scraper.py          # Scraper de livros
│   ├── data_processor.py        # Processamento (JSON/CSV)
│   └── main.py                  # CLI do scraper
│
├── data/
│   ├── users.csv                # Usuários da API
│   └── output/                  # Dados de scraping
│
├── tests/                       # Testes unitários
│   ├── test_api.py
│   ├── test_auth.py
│   ├── test_scraper.py
│   └── test_scraping.py
│
├── examples/                    # Exemplos de uso
│   ├── api_examples.py
│   ├── scraper_examples.py
│   └── auth_scraping_example.py
│
├── scripts/
│   └── create_user.py          # Gerenciar usuários
│
├── requirements.txt             # Dependências
├── run_api.py                  # Iniciar API
├── run_scraper.py              # Iniciar scraper
├── Procfile                    # Deploy Heroku
└── README.md                   # Este arquivo
```

## 🚀 Configuração do Ambiente

### 1. Criar ambiente virtual e instalar dependências

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar (macOS/Linux)
source venv/bin/activate

# Ativar (Windows)
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Iniciar a API

```bash
python run_api.py
```

A API estará disponível em: **http://localhost:5000**

**📖 Documentação Swagger:** http://localhost:5000/api/v1/docs

---

## 🔐 Autenticação e Login

### Usuários Padrão

A aplicação vem com dois usuários pré-configurados:

| Usuário | Senha | Role | Permissões |
|---------|-------|------|------------|
| `admin` | `admin123` | admin | Acesso completo + Scraping |
| `user` | `user123` | user | Apenas consulta de livros |

> ⚠️ **Importante:** Em produção, altere essas senhas!

### Como Fazer Login

#### 1. Login e Obter Token

**Request:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Response:**
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

#### 2. Usar o Token nas Requisições

Copie o `access_token` e use no header `Authorization`:

```bash
# Salvar token em variável
TOKEN="seu_access_token_aqui"

# Usar em requisições
curl http://localhost:5000/api/v1/books \
  -H "Authorization: Bearer $TOKEN"
```

#### 3. Exemplo Python

```python
import requests

# 1. Login
response = requests.post(
    "http://localhost:5000/api/v1/auth/login",
    json={
        "username": "admin",
        "password": "admin123"
    }
)

tokens = response.json()
access_token = tokens['access_token']

# 2. Usar token nas requisições
headers = {"Authorization": f"Bearer {access_token}"}

# 3. Fazer requisições autenticadas
books = requests.get(
    "http://localhost:5000/api/v1/books",
    headers=headers
)
print(books.json())
```

### Renovar Token (Refresh)

O access token expira em 1 hora. Use o refresh token para obter um novo:

```bash
curl -X POST http://localhost:5000/api/v1/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

---

## 📚 Documentação da API (Swagger)

### 🎯 Acesse a Documentação Interativa

A API possui documentação completa com Swagger/OpenAPI, disponível em:

**URL:** http://localhost:5000/api/v1/docs

Na documentação Swagger você pode:
- ✅ Ver todos os endpoints disponíveis
- ✅ Testar as requisições diretamente no navegador
- ✅ Ver exemplos de request/response
- ✅ Entender os parâmetros e schemas
- ✅ Autenticar com JWT e testar endpoints protegidos

### Como Usar o Swagger

1. **Acesse:** http://localhost:5000/api/v1/docs
2. **Fazer Login:**
   - Clique em "POST /api/v1/auth/login"
   - Clique em "Try it out"
   - Use: `{"username": "admin", "password": "admin123"}`
   - Execute e copie o `access_token`
3. **Autorizar:**
   - Clique no botão "Authorize" 🔒 (topo da página)
   - Digite: `Bearer seu_access_token_aqui`
   - Clique em "Authorize"
4. **Testar Endpoints:**
   - Agora você pode testar qualquer endpoint protegido!

---

## 📚 Endpoints da API

### Autenticação (Público)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/auth/login` | Login e obter tokens |
| POST | `/api/v1/auth/refresh` | Renovar access token |
| GET | `/api/v1/auth/me` | Informações do usuário logado |
| POST | `/api/v1/auth/register` | Registrar novo usuário |

### Books (Requer Token)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/books` | Listar livros (paginação, busca) |
| GET | `/api/v1/books/:id` | Buscar livro por ID |
| POST | `/api/v1/books` | Criar novo livro |
| PUT | `/api/v1/books/:id` | Atualizar livro |
| DELETE | `/api/v1/books/:id` | Deletar livro |
| GET | `/api/v1/stats` | Estatísticas da coleção |

### Scraping (Requer Admin)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/scraping/trigger` | Iniciar scraping ⚠️ |
| GET | `/api/v1/scraping/jobs` | Listar jobs de scraping ⚠️ |
| GET | `/api/v1/scraping/jobs/:id` | Status do job ⚠️ |

> ⚠️ = Requer role `admin`

---

## 🎯 Exemplos de Uso

### 1. Login e Listar Livros

```bash
# 1. Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  > login.json

# 2. Extrair token
TOKEN=$(cat login.json | jq -r '.access_token')

# 3. Listar livros
curl http://localhost:5000/api/v1/books \
  -H "Authorization: Bearer $TOKEN"
```

### 2. Criar Livro

```bash
curl -X POST http://localhost:5000/api/v1/books \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Machine Learning",
    "author": "Sebastian Raschka",
    "isbn": "978-1234567890",
    "price": 49.99,
    "category": "Technology"
  }'
```

### 3. Iniciar Scraping (Admin Only)

```bash
# Login como admin
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  > admin_login.json

ADMIN_TOKEN=$(cat admin_login.json | jq -r '.access_token')

# Iniciar scraping
curl -X POST http://localhost:5000/api/v1/scraping/trigger \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pages": 3,
    "format": "both",
    "output": "meus_livros"
  }'
```

**Response:**
```json
{
  "message": "Scraping job started",
  "job_id": "job_1",
  "parameters": {
    "url": "http://books.toscrape.com",
    "pages": 3,
    "format": "both",
    "output": "meus_livros"
  }
}
```

### 4. Verificar Status do Scraping

```bash
curl http://localhost:5000/api/v1/scraping/jobs/job_1 \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### 5. Exemplo Python Completo

```python
import requests
import time

BASE_URL = "http://localhost:5000/api/v1"

# 1. Login como admin
login = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "admin", "password": "admin123"}
).json()

token = login['access_token']
headers = {"Authorization": f"Bearer {token}"}

# 2. Iniciar scraping
job = requests.post(
    f"{BASE_URL}/scraping/trigger",
    json={"pages": 2, "format": "json"},
    headers=headers
).json()

print(f"Job iniciado: {job['job_id']}")

# 3. Aguardar e verificar status
time.sleep(10)
status = requests.get(
    f"{BASE_URL}/scraping/jobs/{job['job_id']}",
    headers=headers
).json()

if status['status'] == 'completed':
    print(f"✅ {status['results']['books_count']} livros coletados!")
    print(f"Arquivos: {status['results']['files']}")
```

**Ou use o exemplo pronto:**
```bash
python examples/auth_scraping_example.py
```

---

## 👥 Gerenciar Usuários

### Listar Usuários

```bash
python scripts/create_user.py list
```

### Criar Novo Usuário

```bash
# Usuário regular
python scripts/create_user.py create -u joao -p senha123

# Administrador
python scripts/create_user.py create -u maria -p senha456 -r admin
```

### Via API (Register)

```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "novousuario",
    "password": "senha123"
  }'
```

> Novos usuários são automaticamente salvos em `data/users.csv`

---

## 🕷️ Web Scraping (via CLI)

Além do endpoint da API, você pode usar o scraper diretamente:

```bash
# Scraping básico
python run_scraper.py

# Customizado
python run_scraper.py --pages 5 --format both --output livros

# Ajuda
python run_scraper.py --help
```

**Opções:**
- `--url`: URL base para scraping
- `--pages`: Número de páginas (1-50)
- `--format`: json, csv, ou both
- `--output`: Nome do arquivo de saída

---

## 🧪 Executar Testes

```bash
# Todos os testes
pytest

# Apenas autenticação
pytest tests/test_auth.py -v

# Apenas scraping
pytest tests/test_scraping.py -v

# Com cobertura
pytest --cov=api --cov=scraper --cov-report=html
```

---

## 📦 Dependências Principais

### API & Autenticação
- **Flask 3.0.0** - Framework web
- **Flask-JWT-Extended 4.5.3** - Autenticação JWT
- **Flask-CORS 4.0.0** - Suporte a CORS
- **Gunicorn 21.2.0** - Servidor de produção

### Web Scraping
- **requests 2.31.0** - Cliente HTTP
- **beautifulsoup4 4.12.2** - Parser HTML
- **lxml 4.9.3** - Parser rápido

### Processamento
- **pandas 2.1.3** - Manipulação de dados
- **numpy 1.26.2** - Computação numérica

---

## 🐳 Deploy com Docker

### Rodar com Docker

```bash
# Build e run
docker-compose up

# Apenas API
docker-compose up api

# Background
docker-compose up -d
```

### Configuração

O `docker-compose.yml` está configurado para rodar:
- API na porta 5000
- Scraper em background

---

## 🚀 Deploy no Heroku

### 1. Criar app no Heroku

```bash
heroku create seu-app-name
```

### 2. Configurar variáveis

```bash
heroku config:set FLASK_ENV=production
heroku config:set FLASK_DEBUG=False
heroku config:set JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

### 3. Deploy

```bash
git push heroku main
```

### 4. Verificar

```bash
heroku logs --tail
heroku open
```

---

## 🔒 Segurança

### Tokens JWT

- **Access Token**: Expira em 1 hora
- **Refresh Token**: Expira em 30 dias

### Configurar Chave Secreta

```bash
# Gerar chave segura
python -c "import secrets; print(secrets.token_hex(32))"

# Adicionar ao .env
JWT_SECRET_KEY=sua_chave_gerada_aqui
SECRET_KEY=outra_chave_segura
```

### Alterar Senhas Padrão

```bash
# Editar data/users.csv
# Ou recriar usuários

python scripts/create_user.py create -u admin -p nova_senha_forte -r admin
```

---

## 🛠️ Comandos Úteis

### Make Commands

```bash
make help          # Ver todos os comandos
make install       # Instalar dependências
make run-api       # Rodar API
make test          # Rodar testes
make clean         # Limpar temporários
```

### API

```bash
# Rodar API
python run_api.py

# Health check
curl http://localhost:5000/health

# Info da API
curl http://localhost:5000/api/v1
```

### Scraper

```bash
# CLI
python run_scraper.py --pages 3

# Exemplos
python examples/scraper_examples.py
```

---

## 📊 Fluxo Completo: Login → Scraping

```bash
#!/bin/bash

# 1. Login
echo "🔐 Fazendo login..."
curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  > login_response.json

TOKEN=$(cat login_response.json | jq -r '.access_token')
echo "✅ Token obtido!"

# 2. Iniciar scraping
echo "🕷️ Iniciando scraping..."
curl -s -X POST http://localhost:5000/api/v1/scraping/trigger \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"pages": 2, "format": "both"}' \
  > job_response.json

JOB_ID=$(cat job_response.json | jq -r '.job_id')
echo "✅ Job $JOB_ID iniciado!"

# 3. Aguardar conclusão
echo "⏳ Aguardando conclusão..."
sleep 15

# 4. Verificar resultado
curl -s http://localhost:5000/api/v1/scraping/jobs/$JOB_ID \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.'

echo "✅ Concluído! Verifique data/output/"
```

---

## 🐛 Troubleshooting

### Erro: Token expired

```bash
# Use o refresh token para obter novo access token
curl -X POST http://localhost:5000/api/v1/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

### Erro: 403 Forbidden (Admin required)

```bash
# Certifique-se de usar credenciais de admin
# username: admin, password: admin123
```

### Erro: Connection refused

```bash
# Certifique-se de que a API está rodando
python run_api.py
```

### Erro: Module not found

```bash
# Reinstalar dependências
pip install -r requirements.txt
```

---

## 📝 Estrutura de Dados

### CSV de Usuários (`data/users.csv`)

```csv
username,password_hash,role
admin,$2b$12$...,admin
user,$2b$12$...,user
```

### Dados de Scraping (`data/output/books.csv`)

```csv
title,price,rating,in_stock,url
"Book Title",19.99,5,True,"http://..."
```

---

## 🎓 Exemplos Prontos

### Python

```bash
# Exemplos da API
python examples/api_examples.py

# Exemplos do scraper
python examples/scraper_examples.py

# Exemplos de autenticação + scraping
python examples/auth_scraping_example.py
```

---

## 📚 Recursos Adicionais

### Documentação de Dependências

- [Flask](https://flask.palletsprojects.com/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Pandas](https://pandas.pydata.org/)

### Arquivos de Configuração

- `.env.example` - Variáveis de ambiente
- `Procfile` - Configuração Heroku
- `docker-compose.yml` - Configuração Docker
- `pyproject.toml` - Configuração do projeto

---

## 🎯 Quick Start

```bash
# 1. Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Rodar API
python run_api.py

# 3. Acessar documentação Swagger
# Abra no navegador: http://localhost:5000/api/v1/docs

# 4. Ou testar via cURL
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

---

## 📄 Licença

Este projeto é para fins educacionais - FIAP MLE.

## 👥 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Add NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

---

## 📞 Suporte

Para dúvidas ou problemas, abra uma [Issue](https://github.com/giulianogimenez/FIAP-MLE-book-store/issues).

---

**🚀 Versão:** 2.0.0  
**📅 Última atualização:** 27/11/2025

**✅ Pronto para usar! Faça login com `admin`/`admin123` e comece a desenvolver!**

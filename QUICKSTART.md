# 🚀 Quick Start - Começando em 5 Minutos

Este guia vai te ajudar a ter o projeto rodando em menos de 5 minutos!

## ⚡ Setup Rápido

### Opção 1: Setup Manual (Recomendado)

```bash
# 1. Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Criar arquivo .env
make env  # ou copiar manualmente

# Pronto! 🎉
```

### Opção 2: Usando Make (Mais Fácil)

```bash
# Setup completo automático
make dev

# Depois ative o ambiente:
source venv/bin/activate
make setup
make env
```

### Opção 3: Usando Docker

```bash
# Rodar API com Docker
docker-compose up api

# Ou rodar API + Scraper
docker-compose up
```

## 🎯 Primeiros Passos

### 1. Rodar a API (Terminal 1)

```bash
python run_api.py
```

Acesse: http://localhost:5000/health

### 2. Testar a API (Terminal 2)

```bash
# Método 1: Usando curl
curl http://localhost:5000/api/v1/books

# Método 2: Usando Python
python examples/api_examples.py

# Método 3: Usando Make
make api-test
```

### 3. Testar o Scraper

```bash
# Scraping básico
python run_scraper.py

# Com exemplos
python examples/scraper_examples.py

# Ou via Make
make scrape-demo
```

## 📚 Comandos Essenciais

### API

```bash
# Rodar API
python run_api.py

# Testar health
curl http://localhost:5000/health

# Listar livros
curl http://localhost:5000/api/v1/books

# Criar livro
curl -X POST http://localhost:5000/api/v1/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","author":"Author","isbn":"123","price":29.99}'
```

### Scraper

```bash
# Básico
python run_scraper.py

# Customizado
python run_scraper.py --pages 5 --format json --output meus_livros

# Ver ajuda
python run_scraper.py --help
```

### Testes

```bash
# Rodar todos os testes
pytest

# Com verbose
pytest -v

# Arquivo específico
pytest tests/test_api.py
```

### Make Commands

```bash
make help          # Ver todos os comandos
make install       # Instalar dependências
make run-api       # Rodar API
make run-scraper   # Rodar scraper
make test          # Rodar testes
make clean         # Limpar temporários
```

## 🎓 Tutoriais Rápidos

### Tutorial 1: Adicionar um Livro via API

```bash
# 1. Certifique-se de que a API está rodando
python run_api.py &

# 2. Criar livro
curl -X POST http://localhost:5000/api/v1/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Machine Learning",
    "author": "Sebastian Raschka",
    "isbn": "978-1234567890",
    "price": 49.99,
    "category": "Technology"
  }'

# 3. Verificar livro criado
curl http://localhost:5000/api/v1/books/3
```

### Tutorial 2: Fazer Scraping de 3 Páginas

```bash
# Scraping + Salvar em CSV e JSON
python run_scraper.py --pages 3 --format both --output livros_coletados

# Ver arquivos criados
ls -lh data/output/

# Ler CSV
cat data/output/livros_coletados.csv
```

### Tutorial 3: Testar com Python

```python
# Salvar como test_quick.py
import requests

# Testar API
response = requests.get('http://localhost:5000/api/v1/books')
print(f"Status: {response.status_code}")
print(f"Livros: {len(response.json()['books'])}")

# Criar livro
new_book = {
    "title": "Quick Test Book",
    "author": "Test Author",
    "isbn": "123",
    "price": 19.99
}
response = requests.post(
    'http://localhost:5000/api/v1/books',
    json=new_book
)
print(f"Livro criado: {response.json()}")
```

```bash
# Rodar
python test_quick.py
```

## 🔥 Comandos de Produtividade

### Ver estrutura do projeto
```bash
make tree
```

### Status do projeto
```bash
make status
```

### Limpar tudo
```bash
make clean
make clean-data
```

### Rodar exemplos
```bash
make examples-api      # Exemplos da API
make examples-scraper  # Exemplos do scraper
```

## 📖 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Health check |
| GET | `/api/v1/books` | Listar livros |
| GET | `/api/v1/books/:id` | Buscar livro |
| POST | `/api/v1/books` | Criar livro |
| PUT | `/api/v1/books/:id` | Atualizar livro |
| DELETE | `/api/v1/books/:id` | Deletar livro |
| GET | `/api/v1/stats` | Estatísticas |

## 🎯 Próximos Passos

1. ✅ API rodando → Teste os endpoints
2. ✅ Scraper funcionando → Colete alguns dados
3. 📝 Leia o [README.md](README.md) completo
4. 🔧 Customize o scraper para outros sites
5. 🚀 Adicione novos endpoints na API
6. 🧪 Escreva mais testes
7. 📦 Deploy em produção

## ❓ Problemas?

### API não inicia
```bash
# Verificar se a porta 5000 está livre
lsof -ti:5000 | xargs kill -9

# Tentar outra porta
export API_PORT=8000
python run_api.py
```

### Scraper com erro
```bash
# Verificar dependências
pip install beautifulsoup4 lxml requests

# Testar com menos páginas
python run_scraper.py --pages 1
```

### Testes falhando
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Rodar teste específico
pytest tests/test_api.py::test_health_endpoint -v
```

## 📚 Documentação Completa

- [README.md](README.md) - Documentação completa
- [SETUP.md](SETUP.md) - Guia de setup detalhado
- [CONTRIBUTING.md](CONTRIBUTING.md) - Como contribuir
- [Makefile](Makefile) - Comandos disponíveis

## 🎉 Pronto!

Agora você tem:
- ✅ Ambiente configurado
- ✅ API REST funcionando
- ✅ Web Scraper operacional
- ✅ Testes rodando

**Divirta-se codificando! 🚀**


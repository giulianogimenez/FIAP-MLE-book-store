# 🚀 Guia Rápido de Setup

## Passo a Passo para Configurar o Ambiente

### 1. Criar e Ativar o Ambiente Virtual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar (macOS/Linux)
source venv/bin/activate

# Ativar (Windows)
venv\Scripts\activate
```

### 2. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env (as configurações padrão já funcionam)
cat > .env << 'EOF'
# Flask Configuration
FLASK_APP=api.app
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000
API_HOST=0.0.0.0

# Database Configuration (if needed)
DATABASE_URL=sqlite:///bookstore.db

# Scraping Configuration
SCRAPING_DELAY=1
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
EOF
```

### 4. Testar a API

```bash
# Rodar a API
python run_api.py

# Em outro terminal, testar:
curl http://localhost:5000/health
curl http://localhost:5000/api/v1/books
```

### 5. Testar o Scraper

```bash
# Rodar scraper básico
python run_scraper.py

# Rodar com opções customizadas
python run_scraper.py --pages 3 --format both --output meus_livros
```

### 6. Executar Testes

```bash
# Rodar todos os testes
pytest

# Rodar com verbose
pytest -v

# Rodar com cobertura
pytest --cov=api --cov=scraper --cov-report=html
```

## 📝 Comandos Úteis

### API
```bash
# Testar criação de livro
curl -X POST http://localhost:5000/api/v1/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Novo Livro",
    "author": "Autor Teste",
    "isbn": "978-1234567890",
    "price": 39.99,
    "category": "Technology"
  }'

# Buscar livro por ID
curl http://localhost:5000/api/v1/books/1

# Atualizar livro
curl -X PUT http://localhost:5000/api/v1/books/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 29.99}'

# Deletar livro
curl -X DELETE http://localhost:5000/api/v1/books/1

# Ver estatísticas
curl http://localhost:5000/api/v1/stats
```

### Scraper
```bash
# Scraping de 5 páginas em JSON
python run_scraper.py --pages 5 --format json

# Scraping em CSV
python run_scraper.py --pages 3 --format csv --output books_export

# URL customizada
python run_scraper.py --url "https://example.com" --pages 2
```

## 🔍 Verificar Instalação

```bash
# Verificar Python
python --version  # Deve ser 3.8+

# Verificar pip
pip --version

# Verificar pacotes instalados
pip list | grep -E "(Flask|beautifulsoup|pandas|requests)"

# Listar estrutura do projeto
tree -L 2 -I 'venv|__pycache__|*.pyc'
```

## 🐛 Solução de Problemas Comuns

### Erro ao instalar lxml no macOS
```bash
brew install libxml2 libxslt
pip install lxml
```

### Porta 5000 já em uso
```bash
# Opção 1: Matar processo na porta 5000
lsof -ti:5000 | xargs kill -9

# Opção 2: Usar outra porta (editar .env)
echo "API_PORT=8000" >> .env
```

### Erro de permissão
```bash
# Usar ambiente virtual
source venv/bin/activate
pip install -r requirements.txt
```

### Módulos não encontrados
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

## ✅ Checklist de Verificação

- [ ] Python 3.8+ instalado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas (`requirements.txt`)
- [ ] Arquivo `.env` criado
- [ ] API funcionando (`http://localhost:5000/health`)
- [ ] Scraper executando sem erros
- [ ] Testes passando (`pytest`)

## 📚 Próximos Passos

1. Explore a API usando `curl` ou Postman
2. Modifique o scraper para outros sites
3. Adicione novos endpoints na API
4. Implemente persistência com banco de dados
5. Crie novos testes unitários

## 🆘 Ajuda

Se encontrar problemas:
1. Verifique se o ambiente virtual está ativado
2. Confirme que todas as dependências foram instaladas
3. Verifique os logs de erro
4. Consulte o README.md principal para documentação completa


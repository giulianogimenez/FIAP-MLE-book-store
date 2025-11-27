# FIAP MLE - Book Store Project

Projeto Python com dois módulos principais:
1. **API REST** usando Flask para gerenciamento de livros
2. **Data Scraping** para coletar informações de livros de websites

## 📁 Estrutura do Projeto

```
FIAP-MLE-book-store/
├── api/                          # Módulo da API REST
│   ├── __init__.py
│   ├── app.py                    # Aplicação Flask principal
│   ├── config.py                 # Configurações
│   ├── routes.py                 # Rotas da API
│   └── controllers/              # Lógica de negócio
│       ├── __init__.py
│       └── book_controller.py
│
├── scraper/                      # Módulo de Web Scraping
│   ├── __init__.py
│   ├── base_scraper.py          # Classe base para scrapers
│   ├── book_scraper.py          # Scraper de livros
│   ├── data_processor.py        # Processamento de dados
│   └── main.py                  # Script principal do scraper
│
├── tests/                        # Testes unitários
│   ├── __init__.py
│   ├── test_api.py
│   └── test_scraper.py
│
├── data/                         # Diretório para dados (criado automaticamente)
│   └── output/                   # Dados processados
│
├── .env.example                  # Exemplo de variáveis de ambiente
├── .gitignore                    # Arquivos ignorados pelo Git
├── requirements.txt              # Dependências do projeto
├── setup.py                      # Configuração do pacote
├── run_api.py                    # Script para rodar a API
├── run_scraper.py               # Script para rodar o scraper
└── README.md                     # Este arquivo
```

## 🚀 Configuração do Ambiente

### 1. Clone o repositório
```bash
cd FIAP-MLE-book-store
```

### 2. Crie um ambiente virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no macOS/Linux
source venv/bin/activate

# Ativar no Windows
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
# Copiar o arquivo de exemplo
cp .env.example .env

# Editar o .env com suas configurações
```

## 📚 Usando a API REST

### Iniciar o servidor
```bash
python run_api.py
```

A API estará disponível em: `http://localhost:5000`

### Endpoints Disponíveis

#### Health Check
```bash
GET http://localhost:5000/health
```

#### Listar todos os livros
```bash
GET http://localhost:5000/api/v1/books
GET http://localhost:5000/api/v1/books?page=1&limit=10&search=python
```

#### Buscar livro específico
```bash
GET http://localhost:5000/api/v1/books/1
```

#### Criar novo livro
```bash
POST http://localhost:5000/api/v1/books
Content-Type: application/json

{
  "title": "Python for Data Science",
  "author": "John Doe",
  "isbn": "978-1234567890",
  "price": 49.99,
  "category": "Technology"
}
```

#### Atualizar livro
```bash
PUT http://localhost:5000/api/v1/books/1
Content-Type: application/json

{
  "title": "Updated Title",
  "price": 39.99
}
```

#### Deletar livro
```bash
DELETE http://localhost:5000/api/v1/books/1
```

#### Estatísticas
```bash
GET http://localhost:5000/api/v1/stats
```

### Exemplo com curl
```bash
# Listar livros
curl http://localhost:5000/api/v1/books

# Criar livro
curl -X POST http://localhost:5000/api/v1/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Book","author":"Test Author","isbn":"123","price":29.99}'
```

## 🕷️ Usando o Web Scraper

### Executar scraping básico
```bash
python run_scraper.py
```

### Com opções personalizadas
```bash
# Scraping com mais páginas
python run_scraper.py --pages 5

# Especificar formato de saída
python run_scraper.py --format json --output books_data

# URL customizada
python run_scraper.py --url "http://books.toscrape.com" --pages 3
```

### Opções disponíveis
- `--url`: URL base para scraping (padrão: http://books.toscrape.com)
- `--pages`: Número de páginas para scraping (padrão: 2)
- `--output`: Nome do arquivo de saída sem extensão (padrão: books)
- `--format`: Formato de saída - json, csv, ou both (padrão: both)

### Dados gerados
Os dados serão salvos em `data/output/`:
- `books.json` - Dados em formato JSON
- `books.csv` - Dados em formato CSV

## 🧪 Executar Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=api --cov=scraper

# Executar testes específicos
pytest tests/test_api.py
pytest tests/test_scraper.py
```

## 📦 Dependências Principais

### API
- **Flask** - Framework web
- **Flask-CORS** - Suporte a CORS
- **Flask-RESTful** - Extensão para APIs REST

### Scraping
- **requests** - Cliente HTTP
- **BeautifulSoup4** - Parser HTML/XML
- **lxml** - Parser XML/HTML rápido
- **Selenium** - Automação de navegador (para sites dinâmicos)
- **Scrapy** - Framework de scraping avançado

### Processamento de Dados
- **pandas** - Manipulação de dados
- **numpy** - Computação numérica

## 🔧 Desenvolvimento

### Adicionar novas rotas na API
1. Edite `api/routes.py` para adicionar novos endpoints
2. Implemente a lógica em `api/controllers/`

### Criar novo scraper
1. Crie uma classe herdando de `BaseScraper`
2. Implemente os métodos `scrape()` e `parse_item()`

Exemplo:
```python
from scraper.base_scraper import BaseScraper

class MyCustomScraper(BaseScraper):
    def scrape(self, *args, **kwargs):
        # Sua lógica aqui
        pass
    
    def parse_item(self, element):
        # Parse do item
        pass
```

## 📝 Boas Práticas

1. **Scraping Responsável**
   - Use delays entre requisições
   - Respeite robots.txt
   - Não sobrecarregue servidores

2. **API**
   - Valide todos os inputs
   - Use códigos HTTP apropriados
   - Documente seus endpoints

3. **Código**
   - Mantenha o código limpo e documentado
   - Escreva testes para novas funcionalidades
   - Use type hints quando possível

## 🐛 Troubleshooting

### Erro de instalação de lxml
```bash
# macOS
brew install libxml2 libxslt
pip install lxml

# Ubuntu/Debian
sudo apt-get install libxml2-dev libxslt-dev
pip install lxml
```

### Porta 5000 já em uso
Altere a porta no `.env`:
```
API_PORT=8000
```

## 📄 Licença

Este projeto é para fins educacionais - FIAP MLE.

## 👥 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.

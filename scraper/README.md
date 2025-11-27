# 🕷️ Web Scraper - Book Store

Documentação do módulo de Web Scraping para coleta de dados de livros.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Estrutura](#estrutura)
- [Como Usar](#como-usar)
- [Configuração](#configuração)
- [Formatos de Saída](#formatos-de-saída)
- [Integração com API](#integração-com-api)

## Visão Geral

O módulo de scraping coleta dados de livros do site [books.toscrape.com](http://books.toscrape.com), incluindo:

- ✅ Título do livro
- ✅ Preço
- ✅ Disponibilidade (in stock)
- ✅ Rating (1-5 estrelas)
- ✅ URL do produto
- ✅ Imagem do livro (URL)

### Características

- **Scraping responsável**: Delay entre requisições
- **Configurável**: Número de páginas, formato de saída
- **Múltiplos formatos**: JSON, CSV ou ambos
- **Logging**: Rastreamento detalhado do processo
- **CLI**: Interface de linha de comando
- **API Integration**: Executar via endpoint REST

## Estrutura

```
scraper/
├── __init__.py
├── base_scraper.py      # Classe base abstrata
├── book_scraper.py      # Implementação para livros
├── data_processor.py    # Processamento e exportação
└── main.py             # CLI entry point
```

### Arquitetura

```python
BaseScraper (Abstract)
    ↓
BookScraper
    ↓
DataProcessor → Exportação (JSON/CSV)
```

## Como Usar

### Via CLI

#### Básico (padrão: 2 páginas, formato both)

```bash
python run_scraper.py
```

#### Customizado

```bash
# 5 páginas em JSON
python run_scraper.py --pages 5 --format json

# 3 páginas em CSV
python run_scraper.py --pages 3 --format csv

# Ambos os formatos
python run_scraper.py --pages 10 --format both --output meus_livros

# Com URL customizada
python run_scraper.py --url http://books.toscrape.com --pages 2
```

#### Ajuda

```bash
python run_scraper.py --help
```

**Output:**
```
usage: run_scraper.py [-h] [--url URL] [--pages PAGES] 
                      [--format FORMAT] [--output OUTPUT]

Web Scraper para livros

options:
  -h, --help           Mostrar ajuda
  --url URL            URL base (default: http://books.toscrape.com)
  --pages PAGES        Número de páginas (default: 2)
  --format FORMAT      Formato: json, csv, both (default: both)
  --output OUTPUT      Nome do arquivo (default: books)
```

### Via API (Requer Admin)

```bash
# Login como admin
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  > login.json

# Extrair token
TOKEN=$(cat login.json | jq -r '.access_token')

# Iniciar scraping
curl -X POST http://localhost:5000/api/v1/scraping/trigger \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pages": 3,
    "format": "json",
    "output": "meus_livros"
  }'
```

**Response:**
```json
{
  "job_id": "job_1",
  "message": "Scraping job started",
  "parameters": {
    "format": "json",
    "output": "meus_livros",
    "pages": 3,
    "url": "http://books.toscrape.com"
  }
}
```

### Verificar Status do Job

```bash
curl http://localhost:5000/api/v1/scraping/jobs/job_1 \
  -H "Authorization: Bearer $TOKEN"
```

### Via Python

```python
from scraper.book_scraper import BookScraper
from scraper.data_processor import DataProcessor

# Inicializar scraper
scraper = BookScraper(base_url="http://books.toscrape.com")

# Fazer scraping
books = scraper.scrape(num_pages=3)

# Processar dados
processor = DataProcessor(books)
processor.save_json("data/output/books.json")
processor.save_csv("data/output/books.csv")

print(f"✅ Coletados {len(books)} livros!")
```

## Configuração

### base_scraper.py

Classe base abstrata:

```python
class BaseScraper(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 ...'
        })
    
    @abstractmethod
    def scrape_page(self, url: str) -> List[Dict]:
        pass
    
    @abstractmethod
    def scrape(self, num_pages: int) -> List[Dict]:
        pass
```

### book_scraper.py

Implementação para livros:

```python
class BookScraper(BaseScraper):
    def scrape_page(self, url: str) -> List[Dict]:
        """Scrape uma página de livros"""
        response = self.session.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        books = []
        for article in soup.find_all('article', class_='product_pod'):
            book = {
                'title': article.h3.a['title'],
                'price': self._extract_price(article),
                'rating': self._extract_rating(article),
                'in_stock': self._check_availability(article),
                'url': urljoin(self.base_url, article.h3.a['href']),
                'image': urljoin(self.base_url, article.img['src'])
            }
            books.append(book)
        
        return books
    
    def scrape(self, num_pages: int = 2) -> List[Dict]:
        """Scrape múltiplas páginas"""
        all_books = []
        
        for page in range(1, num_pages + 1):
            url = f"{self.base_url}/catalogue/page-{page}.html"
            books = self.scrape_page(url)
            all_books.extend(books)
            
            # Delay responsável
            time.sleep(1)
        
        return all_books
```

### Seletores CSS

| Campo | Seletor |
|-------|---------|
| Title | `article.product_pod h3 a['title']` |
| Price | `article.product_pod .price_color` |
| Rating | `article.product_pod .star-rating['class']` |
| Availability | `article.product_pod .availability` |
| URL | `article.product_pod h3 a['href']` |
| Image | `article.product_pod img['src']` |

## Formatos de Saída

### JSON

```json
[
  {
    "title": "A Light in the Attic",
    "price": 51.77,
    "rating": 3,
    "in_stock": true,
    "url": "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "image": "http://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"
  },
  {
    "title": "Tipping the Velvet",
    "price": 53.74,
    "rating": 1,
    "in_stock": true,
    "url": "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
    "image": "http://books.toscrape.com/media/cache/26/0c/260c6ae16bce31c8f8c95daddd9f4a1c.jpg"
  }
]
```

### CSV

```csv
title,price,rating,in_stock,url,image
"A Light in the Attic",51.77,3,True,"http://...","http://..."
"Tipping the Velvet",53.74,1,True,"http://...","http://..."
```

### Localização dos Arquivos

```
data/output/
├── books_2025-11-27_20-30-45.json
└── books_2025-11-27_20-30-45.csv
```

Ou com nome customizado:

```
data/output/
├── meus_livros_2025-11-27_20-30-45.json
└── meus_livros_2025-11-27_20-30-45.csv
```

## Integração com API

### ScrapingController

```python
class ScrapingController:
    def __init__(self):
        self.jobs = {}
        self.job_counter = 0
    
    def trigger_scraping(self, params):
        job_id = f"job_{self.job_counter}"
        self.job_counter += 1
        
        # Simular job (em produção, use Celery/RQ)
        job = {
            'id': job_id,
            'status': 'running',
            'params': params,
            'started_at': datetime.now()
        }
        
        self.jobs[job_id] = job
        
        # Executar scraping (assíncrono em produção)
        self._run_scraping(job_id, params)
        
        return job_id
```

### Endpoints

#### POST /api/v1/scraping/trigger

```json
{
  "url": "http://books.toscrape.com",
  "pages": 3,
  "format": "both",
  "output": "books"
}
```

#### GET /api/v1/scraping/jobs/:id

```json
{
  "job_id": "job_1",
  "status": "completed",
  "started_at": "2025-11-27T20:30:45",
  "completed_at": "2025-11-27T20:31:15",
  "results": {
    "books_count": 60,
    "files": [
      "data/output/books_2025-11-27_20-30-45.json",
      "data/output/books_2025-11-27_20-30-45.csv"
    ]
  }
}
```

## DataProcessor

Processamento e exportação de dados:

```python
class DataProcessor:
    def __init__(self, data: List[Dict]):
        self.data = data
        self.df = pd.DataFrame(data)
    
    def save_json(self, filepath: str):
        """Salvar em JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def save_csv(self, filepath: str):
        """Salvar em CSV"""
        self.df.to_csv(filepath, index=False, encoding='utf-8')
    
    def get_statistics(self) -> Dict:
        """Estatísticas dos dados"""
        return {
            'total_books': len(self.data),
            'avg_price': self.df['price'].mean(),
            'rating_distribution': self.df['rating'].value_counts().to_dict()
        }
```

## Boas Práticas

### ✅ Implementado

- **User-Agent**: Headers customizados
- **Timeout**: 10 segundos por requisição
- **Delay**: 1 segundo entre páginas
- **Error Handling**: Try/except em requisições
- **Logging**: Rastreamento de progresso

### 📋 Recomendações

1. **Respeitar robots.txt**:
```python
from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url("http://books.toscrape.com/robots.txt")
rp.read()
can_fetch = rp.can_fetch("*", url)
```

2. **Implementar retry**:
```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(total=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
```

3. **Rate Limiting**:
```python
import time
from datetime import datetime

class RateLimiter:
    def __init__(self, max_requests=10, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def wait_if_needed(self):
        now = datetime.now()
        # Limpar requests antigas
        self.requests = [r for r in self.requests 
                        if (now - r).seconds < self.time_window]
        
        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0]).seconds
            time.sleep(sleep_time)
        
        self.requests.append(now)
```

## Troubleshooting

### Site mudou estrutura HTML

**Solução**: Atualizar seletores em `book_scraper.py`

### Timeout errors

**Solução**: Aumentar timeout ou verificar conexão

```python
response = self.session.get(url, timeout=30)  # Aumentar
```

### Dados vazios

**Diagnóstico**:
```python
print(f"Status Code: {response.status_code}")
print(f"Content: {response.text[:500]}")
```

---

**📖 Ver também:**
- [Quick Start](../docs/QUICK_START.md)
- [API Documentation](../api/README.md)
- [Examples](../examples/README.md)


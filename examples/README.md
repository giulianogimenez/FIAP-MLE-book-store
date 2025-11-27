# 📝 Exemplos de Uso

Exemplos práticos para usar a Book Store API.

## 📋 Arquivos Disponíveis

- `api_examples.py` - Exemplos de endpoints da API
- `auth_scraping_example.py` - Autenticação + Scraping completo
- `scraper_examples.py` - Uso direto do módulo scraper

## 🚀 Como Executar

### Pré-requisitos

```bash
# API deve estar rodando
python run_api.py

# Em outro terminal, executar exemplos
python examples/api_examples.py
```

## 📚 api_examples.py

Exemplos de uso dos endpoints da API.

### Executar

```bash
python examples/api_examples.py
```

### O que faz

1. ✅ Lista livros com paginação
2. ✅ Busca livros por ID
3. ✅ Cria novo livro
4. ✅ Atualiza livro existente
5. ✅ Deleta livro
6. ✅ Busca livros por título/categoria
7. ✅ Lista categorias
8. ✅ Obtém estatísticas

### Código de Exemplo

```python
import requests

BASE_URL = "http://localhost:5000/api/v1"

# 1. Listar livros
response = requests.get(f"{BASE_URL}/books")
print("Livros:", response.json())

# 2. Buscar por ID
book_id = 1
response = requests.get(f"{BASE_URL}/books/{book_id}")
print(f"Livro {book_id}:", response.json())

# 3. Criar livro
new_book = {
    "title": "Python para Data Science",
    "author": "Jake VanderPlas",
    "isbn": "978-1491912058",
    "price": 59.99,
    "category": "Technology"
}
response = requests.post(f"{BASE_URL}/books", json=new_book)
print("Livro criado:", response.json())

# 4. Buscar livros
response = requests.get(
    f"{BASE_URL}/books/search",
    params={"title": "Python", "category": "Technology"}
)
print("Busca:", response.json())

# 5. Listar categorias
response = requests.get(f"{BASE_URL}/categories")
print("Categorias:", response.json())

# 6. Estatísticas
response = requests.get(f"{BASE_URL}/stats")
print("Estatísticas:", response.json())
```

## 🔐 auth_scraping_example.py

Exemplo completo de autenticação e scraping.

### Executar

```bash
python examples/auth_scraping_example.py
```

### O que faz

1. ✅ Login como admin
2. ✅ Validação do token
3. ✅ Trigger de job de scraping
4. ✅ Monitoramento do status
5. ✅ Listar todos os jobs
6. ✅ Renovação de token
7. ✅ Teste de acesso negado (user comum)

### Fluxo Completo

```python
import requests
import time

BASE_URL = "http://localhost:5000/api/v1"

# 1. Login como admin
print("🔐 Fazendo login como admin...")
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "admin", "password": "admin123"}
)

if response.status_code == 200:
    data = response.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    print(f"✅ Login bem-sucedido! Usuário: {data['user']['username']}")
else:
    print(f"❌ Erro no login: {response.text}")
    exit(1)

# 2. Headers com autenticação
headers = {"Authorization": f"Bearer {access_token}"}

# 3. Verificar identidade
print("\n📋 Verificando informações do usuário...")
response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
print(f"Usuário: {response.json()}")

# 4. Iniciar scraping (apenas admin)
print("\n🕷️  Iniciando job de scraping...")
scraping_params = {
    "pages": 2,
    "format": "json",
    "output": "example_books"
}

response = requests.post(
    f"{BASE_URL}/scraping/trigger",
    json=scraping_params,
    headers=headers
)

if response.status_code == 200:
    job_data = response.json()
    job_id = job_data['job_id']
    print(f"✅ Job iniciado: {job_id}")
    print(f"Parâmetros: {job_data['parameters']}")
else:
    print(f"❌ Erro ao iniciar scraping: {response.text}")
    exit(1)

# 5. Monitorar status
print(f"\n⏳ Aguardando conclusão do job {job_id}...")
max_attempts = 20
attempt = 0

while attempt < max_attempts:
    response = requests.get(
        f"{BASE_URL}/scraping/jobs/{job_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        status_data = response.json()
        status = status_data['status']
        print(f"Status: {status}")
        
        if status == 'completed':
            print(f"\n✅ Job concluído!")
            print(f"Livros coletados: {status_data['results']['books_count']}")
            print(f"Arquivos: {status_data['results']['files']}")
            break
        elif status == 'failed':
            print(f"\n❌ Job falhou!")
            break
    
    time.sleep(2)
    attempt += 1

# 6. Listar todos os jobs
print("\n📊 Listando todos os jobs...")
response = requests.get(f"{BASE_URL}/scraping/jobs", headers=headers)
print(f"Total de jobs: {len(response.json()['jobs'])}")

# 7. Renovar token (exemplo)
print("\n🔄 Renovando access token...")
refresh_headers = {"Authorization": f"Bearer {refresh_token}"}
response = requests.post(
    f"{BASE_URL}/auth/refresh",
    headers=refresh_headers
)

if response.status_code == 200:
    new_token = response.json()['access_token']
    print("✅ Token renovado com sucesso!")
else:
    print(f"❌ Erro ao renovar token: {response.text}")

# 8. Teste com usuário sem permissão
print("\n🔒 Testando acesso sem permissão de admin...")
user_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "user", "password": "user123"}
)

if user_response.status_code == 200:
    user_token = user_response.json()['access_token']
    user_headers = {"Authorization": f"Bearer {user_token}"}
    
    # Tentar acessar endpoint admin
    response = requests.post(
        f"{BASE_URL}/scraping/trigger",
        json=scraping_params,
        headers=user_headers
    )
    
    if response.status_code == 403:
        print("✅ Acesso negado corretamente (403 Forbidden)")
        print(f"Mensagem: {response.json()['error']}")
    else:
        print("❌ Deveria ter negado acesso!")

print("\n✅ Exemplo completo executado!")
```

## 🕷️ scraper_examples.py

Uso direto do módulo de scraping (sem API).

### Executar

```bash
python examples/scraper_examples.py
```

### O que faz

1. ✅ Scraping básico de 2 páginas
2. ✅ Salvar em múltiplos formatos
3. ✅ Análise de dados coletados
4. ✅ Estatísticas

### Código

```python
from scraper.book_scraper import BookScraper
from scraper.data_processor import DataProcessor
import os

print("🕷️  Iniciando Web Scraper...")

# 1. Criar scraper
scraper = BookScraper(base_url="http://books.toscrape.com")

# 2. Fazer scraping
print("Coletando dados de 2 páginas...")
books = scraper.scrape(num_pages=2)
print(f"✅ Coletados {len(books)} livros!")

# 3. Processar dados
processor = DataProcessor(books)

# 4. Criar diretório de saída
os.makedirs("data/output", exist_ok=True)

# 5. Salvar em JSON
json_file = "data/output/example_books.json"
processor.save_json(json_file)
print(f"✅ Salvo em JSON: {json_file}")

# 6. Salvar em CSV
csv_file = "data/output/example_books.csv"
processor.save_csv(csv_file)
print(f"✅ Salvo em CSV: {csv_file}")

# 7. Mostrar estatísticas
stats = processor.get_statistics()
print("\n📊 Estatísticas:")
print(f"Total de livros: {stats['total_books']}")
print(f"Preço médio: £{stats['avg_price']:.2f}")
print(f"Distribuição de ratings: {stats['rating_distribution']}")

# 8. Mostrar primeiros 3 livros
print("\n📚 Primeiros 3 livros:")
for i, book in enumerate(books[:3], 1):
    print(f"\n{i}. {book['title']}")
    print(f"   Preço: £{book['price']}")
    print(f"   Rating: {book['rating']} estrelas")
    print(f"   Disponível: {'Sim' if book['in_stock'] else 'Não'}")
```

## 🎯 Casos de Uso

### Exemplo 1: Integração Completa

```python
import requests

# Setup
BASE_URL = "http://localhost:5000/api/v1"

# 1. Autenticar
auth_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "admin", "password": "admin123"}
)
token = auth_response.json()['access_token']
headers = {"Authorization": f"Bearer {token}"}

# 2. Executar scraping
scrape_response = requests.post(
    f"{BASE_URL}/scraping/trigger",
    json={"pages": 3, "format": "json"},
    headers=headers
)
job_id = scrape_response.json()['job_id']

# 3. Aguardar e verificar
import time
time.sleep(15)  # Aguardar processamento

status_response = requests.get(
    f"{BASE_URL}/scraping/jobs/{job_id}",
    headers=headers
)
status = status_response.json()

if status['status'] == 'completed':
    print(f"✅ Sucesso! {status['results']['books_count']} livros coletados")
```

### Exemplo 2: Busca Avançada

```python
# Buscar livros de Python em Technology
response = requests.get(
    f"{BASE_URL}/books/search",
    params={
        "title": "Python",
        "category": "Technology"
    },
    headers=headers
)

results = response.json()
print(f"Encontrados {results['total']} livros:")
for book in results['books']:
    print(f"- {book['title']} (£{book['price']})")
```

### Exemplo 3: Gerenciamento de Livros

```python
# CRUD completo
# 1. Criar
new_book = {
    "title": "Novo Livro",
    "author": "Autor",
    "isbn": "123-456",
    "price": 29.99,
    "category": "Technology"
}
create_response = requests.post(
    f"{BASE_URL}/books",
    json=new_book,
    headers=headers
)
book_id = create_response.json()['book']['id']

# 2. Ler
read_response = requests.get(
    f"{BASE_URL}/books/{book_id}",
    headers=headers
)

# 3. Atualizar
update_response = requests.put(
    f"{BASE_URL}/books/{book_id}",
    json={"price": 24.99},
    headers=headers
)

# 4. Deletar
delete_response = requests.delete(
    f"{BASE_URL}/books/{book_id}",
    headers=headers
)
```

## 📖 Documentação Adicional

- [Quick Start](../docs/QUICK_START.md)
- [Autenticação](../docs/AUTHENTICATION.md)
- [API Completa](../api/README.md)
- [Web Scraper](../scraper/README.md)

## 💡 Dicas

1. **Sempre verificar status code** antes de processar resposta
2. **Usar try/except** para tratamento de erros
3. **Implementar retry logic** para requests
4. **Fazer refresh de token** antes de expirar
5. **Validar dados** antes de enviar

---

**✅ Explore os exemplos e adapte para suas necessidades!**


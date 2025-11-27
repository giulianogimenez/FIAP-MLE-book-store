"""
Exemplos de uso da API usando Python requests
"""
import requests
import json

BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api/v1"


def test_health():
    """Testar health check"""
    response = requests.get(f"{BASE_URL}/health")
    print("✅ Health Check:")
    print(json.dumps(response.json(), indent=2))
    print()


def get_all_books():
    """Listar todos os livros"""
    response = requests.get(f"{API_URL}/books")
    print("📚 Todos os livros:")
    print(json.dumps(response.json(), indent=2))
    print()


def get_book_by_id(book_id):
    """Buscar livro por ID"""
    response = requests.get(f"{API_URL}/books/{book_id}")
    print(f"📖 Livro {book_id}:")
    print(json.dumps(response.json(), indent=2))
    print()


def create_book():
    """Criar novo livro"""
    new_book = {
        "title": "Deep Learning with Python",
        "author": "François Chollet",
        "isbn": "978-1617294433",
        "price": 54.99,
        "category": "Technology"
    }
    
    response = requests.post(
        f"{API_URL}/books",
        json=new_book,
        headers={"Content-Type": "application/json"}
    )
    print("➕ Criar livro:")
    print(json.dumps(response.json(), indent=2))
    print()
    return response.json().get('book', {}).get('id')


def update_book(book_id):
    """Atualizar livro"""
    updates = {
        "price": 44.99,
        "category": "Machine Learning"
    }
    
    response = requests.put(
        f"{API_URL}/books/{book_id}",
        json=updates,
        headers={"Content-Type": "application/json"}
    )
    print(f"✏️ Atualizar livro {book_id}:")
    print(json.dumps(response.json(), indent=2))
    print()


def search_books(search_term):
    """Buscar livros"""
    response = requests.get(
        f"{API_URL}/books",
        params={"search": search_term, "limit": 5}
    )
    print(f"🔍 Buscar '{search_term}':")
    print(json.dumps(response.json(), indent=2))
    print()


def get_stats():
    """Obter estatísticas"""
    response = requests.get(f"{API_URL}/stats")
    print("📊 Estatísticas:")
    print(json.dumps(response.json(), indent=2))
    print()


def delete_book(book_id):
    """Deletar livro"""
    response = requests.delete(f"{API_URL}/books/{book_id}")
    print(f"🗑️ Deletar livro {book_id}:")
    print(json.dumps(response.json(), indent=2))
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Exemplos de Uso da Book Store API")
    print("=" * 60)
    print()
    
    try:
        # Health check
        test_health()
        
        # Listar livros
        get_all_books()
        
        # Buscar livro específico
        get_book_by_id(1)
        
        # Criar novo livro
        new_book_id = create_book()
        
        # Atualizar livro
        if new_book_id:
            update_book(new_book_id)
        
        # Buscar livros
        search_books("python")
        
        # Estatísticas
        get_stats()
        
        # Deletar livro (opcional)
        # if new_book_id:
        #     delete_book(new_book_id)
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
        print("   Certifique-se de que a API está rodando:")
        print("   python run_api.py")
    except Exception as e:
        print(f"❌ Erro: {e}")


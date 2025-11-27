"""
Exemplos de uso do módulo de scraping
"""
import sys
sys.path.insert(0, '..')

from scraper.book_scraper import BookScraper
from scraper.data_processor import DataProcessor


def example_basic_scraping():
    """Exemplo básico de scraping"""
    print("=" * 60)
    print("📚 Exemplo 1: Scraping Básico")
    print("=" * 60)
    
    # Criar scraper
    scraper = BookScraper(base_url="http://books.toscrape.com", delay=0.5)
    
    # Scraping de 2 páginas
    print("🕷️ Iniciando scraping...")
    books = scraper.scrape(max_pages=2)
    
    print(f"✅ {len(books)} livros encontrados!")
    
    # Mostrar primeiros 3 livros
    print("\n📖 Primeiros 3 livros:")
    for i, book in enumerate(books[:3], 1):
        print(f"\n{i}. {book['title']}")
        print(f"   Preço: £{book['price']}")
        print(f"   Rating: {book['rating']}/5")
        print(f"   Em estoque: {'Sim' if book['in_stock'] else 'Não'}")
    
    scraper.close()
    return books


def example_save_data():
    """Exemplo de salvar dados"""
    print("\n" + "=" * 60)
    print("💾 Exemplo 2: Processar e Salvar Dados")
    print("=" * 60)
    
    # Criar scraper
    scraper = BookScraper(delay=0.5)
    
    # Scraping
    print("🕷️ Fazendo scraping...")
    books = scraper.scrape(max_pages=1)
    scraper.close()
    
    # Processar dados
    processor = DataProcessor(output_dir="../data/examples")
    
    # Limpar dados
    cleaned_books = processor.clean_data(books)
    print(f"🧹 Dados limpos: {len(cleaned_books)} livros válidos")
    
    # Salvar em JSON
    json_path = processor.save_to_json(cleaned_books, "books_example")
    print(f"💾 Salvo em JSON: {json_path}")
    
    # Salvar em CSV
    csv_path = processor.save_to_csv(cleaned_books, "books_example")
    print(f"💾 Salvo em CSV: {csv_path}")
    
    # Gerar relatório
    report = processor.generate_report(cleaned_books)
    print("\n📊 Relatório:")
    print(f"   Total de items: {report['total_items']}")
    print(f"   Colunas: {', '.join(report['columns'])}")


def example_detailed_scraping():
    """Exemplo de scraping detalhado de um livro"""
    print("\n" + "=" * 60)
    print("🔍 Exemplo 3: Scraping Detalhado de um Livro")
    print("=" * 60)
    
    # Criar scraper
    scraper = BookScraper(delay=0.5)
    
    # Primeiro, pegar lista de livros
    print("🕷️ Buscando lista de livros...")
    books = scraper.scrape(max_pages=1)
    
    if books:
        # Pegar detalhes do primeiro livro
        first_book_url = books[0]['url']
        print(f"\n📖 Buscando detalhes de: {books[0]['title']}")
        
        details = scraper.scrape_book_details(first_book_url)
        
        print(f"\n📝 Detalhes:")
        print(f"   Título: {details.get('title', 'N/A')}")
        print(f"   Descrição: {details.get('description', 'N/A')[:100]}...")
        
        if 'product_info' in details:
            print(f"\n   Informações do Produto:")
            for key, value in details['product_info'].items():
                print(f"      {key}: {value}")
    
    scraper.close()


def example_custom_scraper():
    """Exemplo de como criar um scraper customizado"""
    print("\n" + "=" * 60)
    print("🛠️ Exemplo 4: Scraper Customizado")
    print("=" * 60)
    
    code_example = '''
from scraper.base_scraper import BaseScraper

class CustomBookScraper(BaseScraper):
    """Scraper customizado para outro site"""
    
    def __init__(self, base_url, delay=1.0):
        super().__init__(delay)
        self.base_url = base_url
    
    def scrape(self, max_pages=1):
        """Implementar lógica de scraping"""
        all_items = []
        
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/page-{page}"
            soup = self.fetch_page(url)
            
            # Encontrar elementos (ajustar seletores)
            items = soup.find_all('div', class_='book-item')
            
            for item in items:
                parsed_item = self.parse_item(item)
                all_items.append(parsed_item)
        
        return all_items
    
    def parse_item(self, element):
        """Parser customizado"""
        return {
            'title': element.find('h2').text,
            'price': element.find('span', class_='price').text,
            'author': element.find('span', class_='author').text
        }

# Uso:
scraper = CustomBookScraper('https://exemplo.com')
books = scraper.scrape(max_pages=3)
scraper.close()
'''
    
    print("📝 Template de Scraper Customizado:")
    print(code_example)


def example_data_analysis():
    """Exemplo de análise de dados coletados"""
    print("\n" + "=" * 60)
    print("📊 Exemplo 5: Análise de Dados")
    print("=" * 60)
    
    # Criar scraper
    scraper = BookScraper(delay=0.5)
    
    # Scraping
    print("🕷️ Coletando dados...")
    books = scraper.scrape(max_pages=3)
    scraper.close()
    
    if not books:
        print("❌ Nenhum livro encontrado")
        return
    
    # Análises
    print(f"\n📈 Análises:")
    print(f"   Total de livros: {len(books)}")
    
    # Preço médio
    avg_price = sum(b['price'] for b in books) / len(books)
    print(f"   Preço médio: £{avg_price:.2f}")
    
    # Livro mais caro
    most_expensive = max(books, key=lambda x: x['price'])
    print(f"   Livro mais caro: {most_expensive['title']} (£{most_expensive['price']})")
    
    # Livro mais barato
    cheapest = min(books, key=lambda x: x['price'])
    print(f"   Livro mais barato: {cheapest['title']} (£{cheapest['price']})")
    
    # Distribuição de ratings
    ratings = {}
    for book in books:
        rating = book['rating']
        ratings[rating] = ratings.get(rating, 0) + 1
    
    print(f"\n   Distribuição de Ratings:")
    for rating in sorted(ratings.keys(), reverse=True):
        count = ratings[rating]
        bar = '█' * (count // 2)
        print(f"      {rating}⭐: {bar} ({count})")
    
    # Em estoque
    in_stock_count = sum(1 for b in books if b['in_stock'])
    print(f"\n   Em estoque: {in_stock_count}/{len(books)} ({in_stock_count/len(books)*100:.1f}%)")


if __name__ == "__main__":
    print("🚀 Exemplos de Uso do Módulo de Scraping")
    print()
    
    try:
        # Executar exemplos
        example_basic_scraping()
        example_save_data()
        example_detailed_scraping()
        example_custom_scraper()
        example_data_analysis()
        
        print("\n" + "=" * 60)
        print("✅ Todos os exemplos executados com sucesso!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro ao executar exemplos: {e}")
        import traceback
        traceback.print_exc()


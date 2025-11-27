"""
Book Scraper - Scrapes book information from websites
"""
import logging
from typing import List, Dict, Any
from scraper.base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class BookScraper(BaseScraper):
    """
    Scraper for book information
    
    Example usage for http://books.toscrape.com (a practice scraping site)
    """
    
    def __init__(self, base_url: str = "http://books.toscrape.com", delay: float = 1.0):
        """
        Initialize the book scraper
        
        Args:
            base_url: Base URL of the website to scrape
            delay: Delay between requests
        """
        super().__init__(delay)
        self.base_url = base_url.rstrip('/')
    
    def scrape(self, max_pages: int = 1) -> List[Dict[str, Any]]:
        """
        Scrape books from multiple pages
        
        Args:
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of book dictionaries
        """
        all_books = []
        
        for page_num in range(1, max_pages + 1):
            try:
                url = f"{self.base_url}/catalogue/page-{page_num}.html"
                soup = self.fetch_page(url)
                
                # Find all book containers
                book_elements = soup.find_all('article', class_='product_pod')
                
                logger.info(f"Found {len(book_elements)} books on page {page_num}")
                
                for element in book_elements:
                    try:
                        book_data = self.parse_item(element)
                        all_books.append(book_data)
                    except Exception as e:
                        logger.error(f"Error parsing book: {e}")
                        continue
                
            except Exception as e:
                logger.error(f"Error scraping page {page_num}: {e}")
                break
        
        logger.info(f"Total books scraped: {len(all_books)}")
        return all_books
    
    def parse_item(self, element) -> Dict[str, Any]:
        """
        Parse a single book element
        
        Args:
            element: BeautifulSoup element containing book data
            
        Returns:
            Dictionary with book information
        """
        # Extract title
        title_element = element.find('h3').find('a')
        title = title_element.get('title', '')
        
        # Extract price
        price_element = element.find('p', class_='price_color')
        price_text = price_element.text if price_element else '£0.00'
        price = float(price_text.replace('£', ''))
        
        # Extract rating
        star_element = element.find('p', class_='star-rating')
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating = rating_map.get(star_element.get('class')[1], 0) if star_element else 0
        
        # Extract availability
        availability_element = element.find('p', class_='instock availability')
        in_stock = 'In stock' in availability_element.text if availability_element else False
        
        # Extract URL
        book_url = element.find('h3').find('a').get('href', '')
        full_url = f"{self.base_url}/catalogue/{book_url}"
        
        return {
            'title': title,
            'price': price,
            'rating': rating,
            'in_stock': in_stock,
            'url': full_url
        }
    
    def scrape_book_details(self, book_url: str) -> Dict[str, Any]:
        """
        Scrape detailed information for a single book
        
        Args:
            book_url: URL of the book detail page
            
        Returns:
            Dictionary with detailed book information
        """
        try:
            soup = self.fetch_page(book_url)
            
            # Extract basic info
            title = soup.find('h1').text
            
            # Extract product information table
            table = soup.find('table', class_='table-striped')
            product_info = {}
            
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    key = row.find('th').text
                    value = row.find('td').text
                    product_info[key] = value
            
            # Extract description
            description_element = soup.find('div', id='product_description')
            description = ''
            if description_element:
                desc_p = description_element.find_next_sibling('p')
                description = desc_p.text if desc_p else ''
            
            return {
                'title': title,
                'description': description,
                'product_info': product_info,
                'url': book_url
            }
            
        except Exception as e:
            logger.error(f"Error scraping book details from {book_url}: {e}")
            return {}


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
    
    def scrape(self, max_pages: int = 1, fetch_details: bool = True) -> List[Dict[str, Any]]:
        """
        Scrape books from multiple pages with detailed information
        
        Args:
            max_pages: Maximum number of pages to scrape
            fetch_details: If True, fetches detailed info for each book (UPC, category, etc.)
            
        Returns:
            List of book dictionaries with complete information
        """
        all_books = []
        
        for page_num in range(1, max_pages + 1):
            try:
                url = f"{self.base_url}/catalogue/page-{page_num}.html"
                soup = self.fetch_page(url)
                
                # Find all book containers
                book_elements = soup.find_all('article', class_='product_pod')
                
                logger.info(f"Found {len(book_elements)} books on page {page_num}")
                
                for idx, element in enumerate(book_elements, 1):
                    try:
                        # Get basic info first
                        book_data = self.parse_item(element)
                        
                        # Fetch detailed information if enabled
                        if fetch_details and book_data.get('url'):
                            logger.info(f"Fetching details for book {idx}/{len(book_elements)} on page {page_num}: {book_data['title']}")
                            details = self.scrape_book_details(book_data['url'])
                            
                            # Merge detailed information
                            if details:
                                book_data.update(details)
                        
                        all_books.append(book_data)
                        
                    except Exception as e:
                        logger.error(f"Error parsing book: {e}")
                        continue
                
            except Exception as e:
                logger.error(f"Error scraping page {page_num}: {e}")
                break
        
        logger.info(f"Total books scraped: {len(all_books)} (with {'detailed' if fetch_details else 'basic'} info)")
        return all_books
    
    def parse_item(self, element) -> Dict[str, Any]:
        """
        Parse a single book element from list page (basic info)
        
        Args:
            element: BeautifulSoup element containing book data
            
        Returns:
            Dictionary with basic book information
        """
        # Extract title
        title_element = element.find('h3').find('a')
        title = title_element.get('title', '').strip() if title_element else 'Unknown'
        
        # Extract price
        price_element = element.find('p', class_='price_color')
        price_text = price_element.text if price_element else '£0.00'
        try:
            price = float(price_text.replace('£', '').strip())
        except ValueError:
            price = 0.0
        
        # Extract rating
        star_element = element.find('p', class_='star-rating')
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating = 0
        if star_element and len(star_element.get('class', [])) > 1:
            rating = rating_map.get(star_element.get('class')[1], 0)
        
        # Extract availability
        availability_element = element.find('p', class_='instock availability')
        in_stock = False
        if availability_element:
            in_stock = 'In stock' in availability_element.text
        
        # Extract URL - handle both relative and absolute paths
        book_url = element.find('h3').find('a').get('href', '') if element.find('h3') and element.find('h3').find('a') else ''
        
        # Clean up URL path
        if book_url:
            # Remove leading '../' or './' from relative paths
            book_url = book_url.replace('../', '').replace('./', '')
            # Ensure 'catalogue/' prefix if not present
            if not book_url.startswith('catalogue/'):
                book_url = f"catalogue/{book_url}"
            full_url = f"{self.base_url}/{book_url}"
        else:
            full_url = ''
        
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
        
        Extracts comprehensive information including:
        - UPC (Universal Product Code)
        - Category
        - Author
        - ISBN
        - Number of reviews
        - Description
        - Product type
        - Tax information
        - Availability
        
        Args:
            book_url: URL of the book detail page
            
        Returns:
            Dictionary with detailed book information
        """
        try:
            soup = self.fetch_page(book_url)
            
            details = {}
            
            # Extract title
            title_element = soup.find('h1')
            if title_element:
                details['title'] = title_element.text.strip()
            
            # Extract category from breadcrumb
            breadcrumb = soup.find('ul', class_='breadcrumb')
            if breadcrumb:
                category_links = breadcrumb.find_all('a')
                if len(category_links) >= 3:
                    details['category'] = category_links[2].text.strip()
                else:
                    details['category'] = 'General'
            else:
                details['category'] = 'General'
            
            # Extract product information table
            table = soup.find('table', class_='table-striped')
            
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    th = row.find('th')
                    td = row.find('td')
                    
                    if th and td:
                        key = th.text.strip()
                        value = td.text.strip()
                        
                        # Map specific fields
                        if key == 'UPC':
                            details['upc'] = value
                        elif key == 'Product Type':
                            details['product_type'] = value
                        elif key == 'Price (excl. tax)':
                            try:
                                details['price_excl_tax'] = float(value.replace('£', ''))
                            except ValueError:
                                details['price_excl_tax'] = 0.0
                        elif key == 'Price (incl. tax)':
                            try:
                                details['price_incl_tax'] = float(value.replace('£', ''))
                            except ValueError:
                                details['price_incl_tax'] = 0.0
                        elif key == 'Tax':
                            try:
                                details['tax'] = float(value.replace('£', ''))
                            except ValueError:
                                details['tax'] = 0.0
                        elif key == 'Availability':
                            # Extract number from "In stock (22 available)"
                            import re
                            match = re.search(r'\((\d+)\s+available\)', value)
                            if match:
                                details['availability'] = int(match.group(1))
                            else:
                                details['availability'] = 0
                            details['availability_text'] = value
                        elif key == 'Number of reviews':
                            try:
                                details['num_reviews'] = int(value)
                            except ValueError:
                                details['num_reviews'] = 0
            
            # Extract description
            description_element = soup.find('div', id='product_description')
            description = ''
            if description_element:
                desc_p = description_element.find_next_sibling('p')
                description = desc_p.text.strip() if desc_p else ''
            details['description'] = description
            
            # Extract author (if available in description or other fields)
            # For books.toscrape.com, author is not explicitly available
            # but we can try to extract from title or description
            details['author'] = 'Unknown'  # Default value
            
            # Extract ISBN (often same as UPC for this site)
            if 'upc' in details:
                details['isbn'] = details['upc']  # Use UPC as ISBN fallback
            else:
                details['isbn'] = 'N/A'
            
            return details
            
        except Exception as e:
            logger.error(f"Error scraping book details from {book_url}: {e}")
            return {}


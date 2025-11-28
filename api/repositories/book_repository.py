"""
Book Repository - Data access layer for books

Follows Single Responsibility Principle (SRP):
- Responsible ONLY for data persistence and retrieval
"""
import json
import os
import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


class BookRepository:
    """
    Repository for book data access
    
    Separates data access from business logic (SRP)
    Allows easy swapping of data sources (DIP)
    """
    
    def __init__(self, data_file: str = 'data/output/books.json'):
        """
        Initialize repository with data source
        
        Args:
            data_file: Path to JSON file containing books
        """
        self.data_file = data_file
        self._books_cache: Optional[List[Dict[str, Any]]] = None
    
    def find_all(self) -> List[Dict[str, Any]]:
        """
        Retrieve all books from data source
        
        Returns:
            List of book dictionaries
        """
        if self._books_cache is None:
            self._load_books()
        
        return self._books_cache or []
    
    def find_by_id(self, book_id: int) -> Optional[Dict[str, Any]]:
        """
        Find a specific book by ID
        
        Args:
            book_id: Book identifier
        
        Returns:
            Book dictionary or None if not found
        """
        books = self.find_all()
        return next((book for book in books if book.get('id') == book_id), None)
    
    def count(self) -> int:
        """
        Count total number of books
        
        Returns:
            Total book count
        """
        return len(self.find_all())
    
    def reload(self) -> None:
        """
        Force reload of books from data source
        
        Useful after scraping operations that update the data file
        """
        self._books_cache = None
        self._load_books()
    
    def _load_books(self) -> None:
        """
        Load books from JSON file (private method)
        
        Uses default books if file doesn't exist
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self._books_cache = json.load(f)
                logger.info(f"Loaded {len(self._books_cache)} books from {self.data_file}")
            else:
                logger.warning(f"Data file {self.data_file} not found, using default books")
                self._books_cache = self._get_default_books()
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {self.data_file}: {e}")
            self._books_cache = self._get_default_books()
        except Exception as e:
            logger.error(f"Error loading books from {self.data_file}: {e}")
            self._books_cache = self._get_default_books()
    
    def _get_default_books(self) -> List[Dict[str, Any]]:
        """
        Get default books for demo purposes
        
        Returns:
            List of default book dictionaries
        """
        return [
            {
                'id': 1,
                'title': 'Python Machine Learning',
                'author': 'Sebastian Raschka',
                'isbn': '978-1789955750',
                'price': 44.99,
                'category': 'Technology'
            },
            {
                'id': 2,
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'isbn': '978-0132350884',
                'price': 39.99,
                'category': 'Technology'
            }
        ]


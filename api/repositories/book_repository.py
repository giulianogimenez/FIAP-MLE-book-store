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
        self._last_modified: Optional[float] = None  # Track file modification time
    
    def find_all(self) -> List[Dict[str, Any]]:
        """
        Retrieve all books from data source
        
        Automatically reloads if the data file has been modified since last load.
        This ensures fresh data after scraping operations.
        
        Returns:
            List of book dictionaries
        """
        # Check if file was modified since last load
        needs_reload = False
        
        if os.path.exists(self.data_file):
            current_mtime = os.path.getmtime(self.data_file)
            if self._last_modified is None or current_mtime > self._last_modified:
                needs_reload = True
                logger.info(f"Data file modified, reloading books from {self.data_file}")
        
        if self._books_cache is None or needs_reload:
            self._load_books()
        
        return self._books_cache or []
    
    def find_by_id(self, book_id: str) -> Optional[Dict[str, Any]]:
        """
        Find a specific book by ID (UUID4)
        
        Args:
            book_id: Book identifier (UUID4 string)
        
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
        
        Useful after scraping operations that update the data file.
        Resets cache and modification time to force fresh load.
        """
        self._books_cache = None
        self._last_modified = None
        self._load_books()
    
    def _load_books(self) -> None:
        """
        Load books from JSON file (private method)
        
        Uses default books if file doesn't exist.
        Records file modification time for auto-reload detection.
        """
        try:
            if os.path.exists(self.data_file):
                # Record modification time BEFORE loading
                self._last_modified = os.path.getmtime(self.data_file)
                
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self._books_cache = json.load(f)
                logger.info(f"Loaded {len(self._books_cache)} books from {self.data_file}")
            else:
                logger.warning(f"Data file {self.data_file} not found, using default books")
                self._books_cache = self._get_default_books()
                self._last_modified = None
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {self.data_file}: {e}")
            self._books_cache = self._get_default_books()
            self._last_modified = None
        except Exception as e:
            logger.error(f"Error loading books from {self.data_file}: {e}")
            self._books_cache = self._get_default_books()
            self._last_modified = None
    
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


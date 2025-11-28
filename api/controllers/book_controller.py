"""
Book Controller - Business logic for book operations

Follows SOLID principles:
- SRP: Responsible ONLY for business logic
- DIP: Depends on BookRepository abstraction, not concrete data source
- OCP: Extensible without modification

Read-Only API: No create/update/delete methods (handled by scraping only)
"""
from typing import Dict, Any, List
from api.repositories.book_repository import BookRepository


class BookController:
    """
    Controller for book-related business logic
    
    Responsibilities:
    - Pagination logic
    - Search and filtering
    - Statistics calculation
    - Data transformation for API responses
    """
    
    def __init__(self, repository: BookRepository):
        """
        Initialize controller with repository (Dependency Injection)
        
        Args:
            repository: BookRepository instance for data access
        """
        self.repository = repository
    
    def get_all_books(self, page: int = 1, limit: int = 10, search: str = '') -> Dict[str, Any]:
        """
        Get all books with pagination and search
        
        Args:
            page: Page number (1-indexed)
            limit: Books per page
            search: Search term for title/author
        
        Returns:
            Dictionary with paginated books and metadata
        """
        all_books = self.repository.find_all()
        filtered_books = all_books
        
        # Apply search filter
        if search:
            search_lower = search.lower()
            filtered_books = [
                book for book in all_books
                if search_lower in book.get('title', '').lower() or 
                   search_lower in book.get('author', '').lower()
            ]
        
        # Calculate pagination
        start = (page - 1) * limit
        end = start + limit
        paginated_books = filtered_books[start:end]
        
        return {
            'books': paginated_books,
            'total': len(filtered_books),
            'page': page,
            'limit': limit,
            'total_pages': (len(filtered_books) + limit - 1) // limit
        }
    
    def get_book_by_id(self, book_id: int) -> Dict[str, Any]:
        """
        Get a specific book by ID
        
        Args:
            book_id: Book identifier
        
        Returns:
            Dictionary with book or error message
        """
        book = self.repository.find_by_id(book_id)
        
        if not book:
            return {'error': 'Book not found'}
        
        return {'book': book}
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Calculate statistics about the book collection
        
        Returns:
            Dictionary with statistics (total, average price, categories)
        """
        books = self.repository.find_all()
        
        if not books:
            return {
                'total_books': 0,
                'average_price': 0,
                'categories': {}
            }
        
        total = len(books)
        avg_price = sum(book.get('price', 0) for book in books) / total
        
        # Count books per category
        categories: Dict[str, int] = {}
        for book in books:
            category = book.get('category', 'General')
            categories[category] = categories.get(category, 0) + 1
        
        return {
            'total_books': total,
            'average_price': round(avg_price, 2),
            'categories': categories
        }
    
    def get_categories(self) -> Dict[str, Any]:
        """
        Get all unique book categories with book counts
        
        Returns:
            Dictionary with category list and total count
        """
        books = self.repository.find_all()
        
        if not books:
            return {
                'categories': [],
                'total': 0
            }
        
        # Extract and count categories
        category_counts: Dict[str, int] = {}
        for book in books:
            category = book.get('category', 'General')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Build sorted category details
        category_details = sorted([
            {'name': cat, 'count': count}
            for cat, count in category_counts.items()
        ], key=lambda x: x['name'])
        
        return {
            'categories': category_details,
            'total': len(category_details)
        }
    
    def search_books(self, title: str = None, category: str = None) -> Dict[str, Any]:
        """
        Search books by title and/or category
        
        Args:
            title: Partial title search (case-insensitive)
            category: Exact category match (case-insensitive)
        
        Returns:
            Dictionary with filtered books and count
        """
        books = self.repository.find_all()
        filtered_books = books
        
        # Filter by title (partial match)
        if title:
            title_lower = title.lower()
            filtered_books = [
                book for book in filtered_books
                if title_lower in book.get('title', '').lower()
            ]
        
        # Filter by category (exact match)
        if category:
            category_lower = category.lower()
            filtered_books = [
                book for book in filtered_books
                if book.get('category', 'General').lower() == category_lower
            ]
        
        return {
            'books': filtered_books,
            'total': len(filtered_books)
        }
    
    def reload_books(self) -> None:
        """
        Reload books from data source
        
        Useful after scraping operations that update the data file
        """
        self.repository.reload()

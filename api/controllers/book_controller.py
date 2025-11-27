"""
Book Controller - Business logic for book operations
"""


class BookController:
    """
    Controller for book-related operations
    """
    
    def __init__(self):
        # Simulated in-memory database
        self.books = [
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
        self.next_id = 3
    
    def get_all_books(self, page=1, limit=10, search=''):
        """
        Get all books with pagination and search
        """
        filtered_books = self.books
        
        if search:
            search_lower = search.lower()
            filtered_books = [
                book for book in self.books
                if search_lower in book['title'].lower() or 
                   search_lower in book['author'].lower()
            ]
        
        # Pagination
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
    
    def get_book_by_id(self, book_id):
        """
        Get a specific book by ID
        """
        book = next((b for b in self.books if b['id'] == book_id), None)
        if not book:
            return {'error': 'Book not found'}
        return {'book': book}
    
    def create_book(self, data):
        """
        Create a new book
        """
        required_fields = ['title', 'author', 'isbn', 'price']
        for field in required_fields:
            if field not in data:
                return {'error': f'Missing required field: {field}'}
        
        new_book = {
            'id': self.next_id,
            'title': data['title'],
            'author': data['author'],
            'isbn': data['isbn'],
            'price': float(data['price']),
            'category': data.get('category', 'General')
        }
        
        self.books.append(new_book)
        self.next_id += 1
        
        return {'message': 'Book created successfully', 'book': new_book}
    
    def update_book(self, book_id, data):
        """
        Update an existing book
        """
        book = next((b for b in self.books if b['id'] == book_id), None)
        if not book:
            return {'error': 'Book not found'}
        
        # Update fields
        if 'title' in data:
            book['title'] = data['title']
        if 'author' in data:
            book['author'] = data['author']
        if 'isbn' in data:
            book['isbn'] = data['isbn']
        if 'price' in data:
            book['price'] = float(data['price'])
        if 'category' in data:
            book['category'] = data['category']
        
        return {'message': 'Book updated successfully', 'book': book}
    
    def delete_book(self, book_id):
        """
        Delete a book
        """
        book = next((b for b in self.books if b['id'] == book_id), None)
        if not book:
            return {'error': 'Book not found'}
        
        self.books.remove(book)
        return {'message': 'Book deleted successfully'}
    
    def get_statistics(self):
        """
        Get statistics about the book collection
        """
        if not self.books:
            return {
                'total_books': 0,
                'average_price': 0,
                'categories': {}
            }
        
        total = len(self.books)
        avg_price = sum(b['price'] for b in self.books) / total
        
        categories = {}
        for book in self.books:
            cat = book.get('category', 'General')
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'total_books': total,
            'average_price': round(avg_price, 2),
            'categories': categories
        }
    
    def get_categories(self):
        """
        Get all unique book categories
        """
        if not self.books:
            return {
                'categories': [],
                'total': 0
            }
        
        # Extract unique categories
        categories = set()
        for book in self.books:
            cat = book.get('category', 'General')
            categories.add(cat)
        
        # Sort categories alphabetically
        sorted_categories = sorted(list(categories))
        
        # Count books per category
        category_details = []
        for cat in sorted_categories:
            count = sum(1 for book in self.books if book.get('category', 'General') == cat)
            category_details.append({
                'name': cat,
                'count': count
            })
        
        return {
            'categories': category_details,
            'total': len(sorted_categories)
        }
    
    def search_books(self, title=None, category=None):
        """
        Search books by title and/or category
        """
        filtered_books = self.books
        
        # Filter by title if provided
        if title:
            title_lower = title.lower()
            filtered_books = [
                book for book in filtered_books
                if title_lower in book['title'].lower()
            ]
        
        # Filter by category if provided
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


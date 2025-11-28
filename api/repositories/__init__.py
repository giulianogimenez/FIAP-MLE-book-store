"""
Repositories module - Data access layer

Following SOLID principles:
- Single Responsibility: Each repository handles one data type
- Dependency Inversion: Controllers depend on repositories, not concrete data sources
"""
from api.repositories.book_repository import BookRepository

__all__ = ['BookRepository']


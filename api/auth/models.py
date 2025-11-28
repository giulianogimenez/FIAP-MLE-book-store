"""
User models for authentication

Follows SOLID principles:
- SRP: Separate User model from UserRepository
- DIP: Repository can be injected where needed
"""
import os
import csv
import logging
from pathlib import Path
from typing import Optional, List, Dict
from werkzeug.security import generate_password_hash, check_password_hash

logger = logging.getLogger(__name__)


class User:
    """
    User model
    
    Responsibilities:
    - Represent user data
    - Verify passwords
    - Convert to dict for API responses
    """
    
    def __init__(self, username: str, password_hash: str, role: str = 'user'):
        """
        Initialize user
        
        Args:
            username: User's unique identifier
            password_hash: Hashed password
            role: User role (user or admin)
        """
        self.username = username
        self.password_hash = password_hash
        self.role = role
    
    def check_password(self, password: str) -> bool:
        """
        Verify password against stored hash
        
        Args:
            password: Plain text password to verify
        
        Returns:
            True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self) -> Dict[str, str]:
        """
        Convert user to dictionary (exclude sensitive data)
        
        Returns:
            Dictionary with username and role
        """
        return {
            'username': self.username,
            'role': self.role
        }


class UserRepository:
    """
    User repository for data access
    
    Responsibilities:
    - Load users from CSV
    - Save users to CSV
    - CRUD operations for users
    
    In production, replace CSV with proper database
    """
    
    def __init__(self, csv_file: str = 'data/users.csv'):
        """
        Initialize repository with data source
        
        Args:
            csv_file: Path to CSV file containing users
        """
        self.csv_file = csv_file
        self.users: Dict[str, User] = {}
        
        # Load users from CSV or create defaults
        if os.path.exists(csv_file):
            self._load_from_csv()
        else:
            logger.info(f"User file {csv_file} not found, creating default users")
            self._create_default_users()
            self._save_to_csv()
    
    def _load_from_csv(self) -> None:
        """
        Load users from CSV file (private method)
        """
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    username = row['username']
                    password_hash = row['password_hash']
                    role = row.get('role', 'user')
                    
                    self.users[username] = User(
                        username=username,
                        password_hash=password_hash,
                        role=role
                    )
            
            logger.info(f"Loaded {len(self.users)} users from {self.csv_file}")
            
        except Exception as e:
            logger.error(f"Error loading users from CSV: {e}")
            logger.info("Creating default users")
            self._create_default_users()
    
    def _create_default_users(self) -> None:
        """
        Create default users for demo purposes (private method)
        """
        self.users = {
            'admin': User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            ),
            'user': User(
                username='user',
                password_hash=generate_password_hash('user123'),
                role='user'
            )
        }
        logger.info("Created default admin and user accounts")
    
    def _save_to_csv(self) -> None:
        """
        Save users to CSV file (private method)
        """
        try:
            # Create directory if it doesn't exist
            Path(self.csv_file).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.csv_file, 'w', encoding='utf-8', newline='') as f:
                fieldnames = ['username', 'password_hash', 'role']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                for user in self.users.values():
                    writer.writerow({
                        'username': user.username,
                        'password_hash': user.password_hash,
                        'role': user.role
                    })
            
            logger.info(f"Saved {len(self.users)} users to {self.csv_file}")
            
        except Exception as e:
            logger.error(f"Error saving users to CSV: {e}")
    
    def find_by_username(self, username: str) -> Optional[User]:
        """
        Find user by username
        
        Args:
            username: Username to search for
        
        Returns:
            User object or None if not found
        """
        return self.users.get(username)
    
    def create_user(self, username: str, password: str, role: str = 'user') -> Optional[User]:
        """
        Create new user and persist to CSV
        
        Args:
            username: Unique username
            password: Plain text password (will be hashed)
            role: User role (default: 'user')
        
        Returns:
            Created User object or None if username already exists
        """
        if username in self.users:
            logger.warning(f"Attempted to create duplicate user: {username}")
            return None
        
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role=role
        )
        self.users[username] = user
        
        # Persist to CSV
        self._save_to_csv()
        
        logger.info(f"Created new user: {username} (role: {role})")
        return user
    
    def user_exists(self, username: str) -> bool:
        """
        Check if user exists
        
        Args:
            username: Username to check
        
        Returns:
            True if user exists, False otherwise
        """
        return username in self.users
    
    def list_users(self) -> List[Dict[str, str]]:
        """
        List all users (excluding sensitive data)
        
        Returns:
            List of user dictionaries
        """
        return [user.to_dict() for user in self.users.values()]
    
    def delete_user(self, username: str) -> bool:
        """
        Delete user and persist changes
        
        Args:
            username: Username to delete
        
        Returns:
            True if deleted, False if user not found
        """
        if username in self.users:
            del self.users[username]
            self._save_to_csv()
            logger.info(f"Deleted user: {username}")
            return True
        
        logger.warning(f"Attempted to delete non-existent user: {username}")
        return False

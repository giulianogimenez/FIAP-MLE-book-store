"""
User models for authentication
In a real application, this would use a database
"""
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """User model"""
    
    def __init__(self, username, password_hash, role='user'):
        self.username = username
        self.password_hash = password_hash
        self.role = role
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'username': self.username,
            'role': self.role
        }


class UserRepository:
    """
    In-memory user repository
    In production, this should use a real database
    """
    
    def __init__(self):
        # Create default users for demo
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
    
    def find_by_username(self, username):
        """Find user by username"""
        return self.users.get(username)
    
    def create_user(self, username, password, role='user'):
        """Create new user"""
        if username in self.users:
            return None
        
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role=role
        )
        self.users[username] = user
        return user
    
    def user_exists(self, username):
        """Check if user exists"""
        return username in self.users


# Global instance (in production, use dependency injection)
user_repository = UserRepository()


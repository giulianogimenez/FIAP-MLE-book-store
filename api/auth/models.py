"""
User models for authentication
Users can be loaded from CSV file or created dynamically
"""
import os
import csv
from pathlib import Path
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
    User repository that can load users from CSV
    In production, this should use a real database
    """
    
    def __init__(self, csv_file='data/users.csv'):
        self.users = {}
        self.csv_file = csv_file
        
        # Try to load users from CSV
        if os.path.exists(csv_file):
            self._load_from_csv(csv_file)
        else:
            # Create default users if CSV doesn't exist
            self._create_default_users()
            # Save to CSV
            self._save_to_csv()
    
    def _load_from_csv(self, csv_file):
        """Load users from CSV file"""
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
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
        except Exception as e:
            print(f"Error loading users from CSV: {e}")
            self._create_default_users()
    
    def _create_default_users(self):
        """Create default users for demo"""
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
    
    def _save_to_csv(self):
        """Save users to CSV file"""
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
        except Exception as e:
            print(f"Error saving users to CSV: {e}")
    
    def find_by_username(self, username):
        """Find user by username"""
        return self.users.get(username)
    
    def create_user(self, username, password, role='user'):
        """Create new user and save to CSV"""
        if username in self.users:
            return None
        
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role=role
        )
        self.users[username] = user
        
        # Save to CSV
        self._save_to_csv()
        
        return user
    
    def user_exists(self, username):
        """Check if user exists"""
        return username in self.users
    
    def list_users(self):
        """List all users"""
        return [user.to_dict() for user in self.users.values()]
    
    def delete_user(self, username):
        """Delete user"""
        if username in self.users:
            del self.users[username]
            self._save_to_csv()
            return True
        return False


# Global instance (in production, use dependency injection)
user_repository = UserRepository()


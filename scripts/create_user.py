#!/usr/bin/env python
"""
Script to create new users in the CSV file
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.security import generate_password_hash
import csv
from pathlib import Path


def create_user(username, password, role='user'):
    """
    Create a new user and add to CSV
    
    Args:
        username: Username
        password: Plain text password (will be hashed)
        role: User role (user or admin)
    """
    csv_file = 'data/users.csv'
    
    # Create directory if needed
    Path(csv_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Check if file exists and if user already exists
    existing_users = set()
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_users.add(row['username'])
    
    if username in existing_users:
        print(f"❌ User '{username}' already exists!")
        return False
    
    # Hash password
    password_hash = generate_password_hash(password)
    
    # Add user to CSV
    file_exists = os.path.exists(csv_file)
    with open(csv_file, 'a', encoding='utf-8', newline='') as f:
        fieldnames = ['username', 'password_hash', 'role']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists or os.path.getsize(csv_file) == 0:
            writer.writeheader()
        
        writer.writerow({
            'username': username,
            'password_hash': password_hash,
            'role': role
        })
    
    print(f"✅ User '{username}' created successfully!")
    print(f"   Role: {role}")
    return True


def list_users():
    """List all users from CSV"""
    csv_file = 'data/users.csv'
    
    if not os.path.exists(csv_file):
        print("❌ No users file found!")
        return
    
    print("\n👥 Users:")
    print("-" * 40)
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"   {row['username']:20s} - {row['role']}")
    print("-" * 40)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage users in CSV file')
    parser.add_argument('action', choices=['create', 'list'], help='Action to perform')
    parser.add_argument('--username', '-u', help='Username')
    parser.add_argument('--password', '-p', help='Password')
    parser.add_argument('--role', '-r', default='user', choices=['user', 'admin'], 
                       help='User role (default: user)')
    
    args = parser.parse_args()
    
    if args.action == 'create':
        if not args.username or not args.password:
            print("❌ Username and password are required!")
            print("\nUsage:")
            print("  python scripts/create_user.py create -u username -p password [-r role]")
            sys.exit(1)
        
        create_user(args.username, args.password, args.role)
    
    elif args.action == 'list':
        list_users()


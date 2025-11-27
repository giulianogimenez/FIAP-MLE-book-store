#!/usr/bin/env python
"""
Script to run the Flask API
"""
from api.app import create_app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting Book Store API...")
    print(f"📍 API available at: http://localhost:5000")
    print(f"🏥 Health check: http://localhost:5000/health")
    print(f"📚 Books endpoint: http://localhost:5000/api/v1/books")
    app.run(host='0.0.0.0', port=5000, debug=True)


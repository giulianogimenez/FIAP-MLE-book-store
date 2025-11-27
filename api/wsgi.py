"""
WSGI entry point for production servers (Gunicorn, etc.)
"""
import os
from api.app import create_app

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


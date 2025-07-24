"""
Flask User Management API - Refactored Version
Clean, secure, and production-ready user management system
"""

import os
import logging
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def create_app():
    """Application factory pattern for creating Flask app"""
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    
    # Initialize in-memory database if not in testing mode
    if not app.config.get('TESTING', False):
        from models.db import init_db
        init_db()
    
    # Register blueprints
    from routes.user_routes import user_bp
    app.register_blueprint(user_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

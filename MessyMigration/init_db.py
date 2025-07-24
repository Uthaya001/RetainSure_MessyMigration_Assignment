"""
Database Initialization Script
Run this script to initialize the in-memory database
"""

import os
import sys
from models.db import init_db

def main():
    """Initialize the database"""
    try:
        print("Initializing in-memory database...")
        init_db()
        print("Database initialized successfully!")
            
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()

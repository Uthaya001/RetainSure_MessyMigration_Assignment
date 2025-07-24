"""
Database Module
Handles all database operations using in-memory storage
"""

import logging
from datetime import datetime
import os

# Simple in-memory storage for demonstration
users_data = []
user_id_counter = 1

class DatabaseManager:
    """Database manager for in-memory operations"""
    
    def __init__(self, db_url=None):
        # No database connection needed for in-memory storage
        pass
    
    def get_all_users(self):
        """Get all users from memory"""
        try:
            # Return copy of users without password_hash for security
            return [
                {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'created_at': user['created_at']
                }
                for user in sorted(users_data, key=lambda x: x['created_at'], reverse=True)
            ]
        except Exception as e:
            logging.error(f"Error in get_all_users: {str(e)}")
            raise
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            for user in users_data:
                if user['id'] == int(user_id):
                    return user
            return None
        except Exception as e:
            logging.error(f"Error in get_user_by_id: {str(e)}")
            raise
    
    def get_user_by_email(self, email):
        """Get user by email"""
        try:
            for user in users_data:
                if user['email'] == email:
                    return user
            return None
        except Exception as e:
            logging.error(f"Error in get_user_by_email: {str(e)}")
            raise
    
    def create_user(self, name, email, password_hash):
        """Create a new user"""
        global user_id_counter
        try:
            new_user = {
                'id': user_id_counter,
                'name': name,
                'email': email,
                'password_hash': password_hash,
                'created_at': datetime.now()
            }
            users_data.append(new_user)
            user_id_counter += 1
            return new_user['id']
        except Exception as e:
            logging.error(f"Error in create_user: {str(e)}")
            raise
    
    def update_user(self, user_id, user_data):
        """Update user with provided data"""
        try:
            for user in users_data:
                if user['id'] == int(user_id):
                    for key, value in user_data.items():
                        if key in ['name', 'email', 'password_hash']:
                            user[key] = value
                    return
        except Exception as e:
            logging.error(f"Error in update_user: {str(e)}")
            raise
    
    def delete_user(self, user_id):
        """Delete user by ID"""
        try:
            global users_data
            initial_count = len(users_data)
            users_data = [user for user in users_data if user['id'] != int(user_id)]
            return len(users_data) < initial_count
        except Exception as e:
            logging.error(f"Error in delete_user: {str(e)}")
            raise
    
    def search_users_by_name(self, name):
        """Search users by name (case-insensitive)"""
        try:
            search_term = name.lower()
            matching_users = [
                user for user in users_data 
                if search_term in user['name'].lower()
            ]
            return sorted(matching_users, key=lambda x: x['name'])
        except Exception as e:
            logging.error(f"Error in search_users_by_name: {str(e)}")
            raise

def init_db(db_url=None):
    """Initialize the in-memory database"""
    try:
        global users_data, user_id_counter
        users_data = []
        user_id_counter = 1
        logging.info("In-memory database initialized")
        
    except Exception as e:
        logging.error(f"Error initializing database: {str(e)}")
        raise

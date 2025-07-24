"""
User Service Module
Contains all business logic for user operations
"""

from models.db import DatabaseManager
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import re
import os

class UserService:
    """Service class for user-related business logic"""
    
    def __init__(self):
        db_url = os.environ.get('DATABASE_URL')
        self.db = DatabaseManager(db_url)
    
    def get_all_users(self):
        """Retrieve all users (excluding password hashes)"""
        try:
            users = self.db.get_all_users()
            # Remove password hashes from response
            safe_users = []
            for user in users:
                safe_user = {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'created_at': user['created_at']
                }
                safe_users.append(safe_user)
            return safe_users
        except Exception as e:
            logging.error(f"Error in get_all_users: {str(e)}")
            raise
    
    def create_user(self, user_data):
        """Create a new user with secure password hashing"""
        try:
            # Check if email already exists
            if self.db.get_user_by_email(user_data['email']):
                return {
                    "success": False,
                    "message": "Email already exists"
                }
            
            # Hash the password
            password_hash = generate_password_hash(user_data['password'])
            
            # Create user in database
            user_id = self.db.create_user(
                name=user_data['name'],
                email=user_data['email'],
                password_hash=password_hash
            )
            
            # Return created user (without password hash)
            user = self.db.get_user_by_id(user_id)
            if not user:
                return {
                    "success": False,
                    "message": "Failed to retrieve created user"
                }
            safe_user = {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'created_at': user['created_at']
            }
            
            return {
                "success": True,
                "user": safe_user
            }
            
        except Exception as e:
            logging.error(f"Error in create_user: {str(e)}")
            return {
                "success": False,
                "message": "Failed to create user"
            }
    
    def update_user(self, user_id, user_data):
        """Update an existing user"""
        try:
            # Check if user exists
            existing_user = self.db.get_user_by_id(user_id)
            if not existing_user:
                return {
                    "success": False,
                    "message": "User not found"
                }
            
            # If email is being updated, check for duplicates
            if 'email' in user_data and user_data['email'] != existing_user['email']:
                if self.db.get_user_by_email(user_data['email']):
                    return {
                        "success": False,
                        "message": "Email already exists"
                    }
            
            # Hash password if it's being updated
            if 'password' in user_data:
                user_data['password_hash'] = generate_password_hash(user_data['password'])
                del user_data['password']
            
            # Update user in database
            self.db.update_user(user_id, user_data)
            
            # Return updated user (without password hash)
            updated_user = self.db.get_user_by_id(user_id)
            if not updated_user:
                return {
                    "success": False,
                    "message": "Failed to retrieve updated user"
                }
            safe_user = {
                'id': updated_user['id'],
                'name': updated_user['name'],
                'email': updated_user['email'],
                'created_at': updated_user['created_at']
            }
            
            return {
                "success": True,
                "user": safe_user
            }
            
        except Exception as e:
            logging.error(f"Error in update_user: {str(e)}")
            return {
                "success": False,
                "message": "Failed to update user"
            }
    
    def delete_user(self, user_id):
        """Delete a user"""
        try:
            # Check if user exists
            if not self.db.get_user_by_id(user_id):
                return {
                    "success": False,
                    "message": "User not found"
                }
            
            # Delete user
            self.db.delete_user(user_id)
            
            return {
                "success": True,
                "message": "User deleted successfully"
            }
            
        except Exception as e:
            logging.error(f"Error in delete_user: {str(e)}")
            return {
                "success": False,
                "message": "Failed to delete user"
            }
    
    def authenticate_user(self, email, password):
        """Authenticate a user login"""
        try:
            # Get user by email
            user = self.db.get_user_by_email(email)
            if not user:
                return {
                    "success": False,
                    "message": "Invalid credentials"
                }
            
            # Check password
            if check_password_hash(user['password_hash'], password):
                # Return user data (without password hash)
                safe_user = {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'created_at': user['created_at']
                }
                return {
                    "success": True,
                    "user": safe_user
                }
            else:
                return {
                    "success": False,
                    "message": "Invalid credentials"
                }
                
        except Exception as e:
            logging.error(f"Error in authenticate_user: {str(e)}")
            return {
                "success": False,
                "message": "Authentication failed"
            }
    
    def search_users_by_name(self, name):
        """Search users by name (case-insensitive)"""
        try:
            users = self.db.search_users_by_name(name)
            # Remove password hashes from response
            safe_users = []
            for user in users:
                safe_user = {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'created_at': user['created_at']
                }
                safe_users.append(safe_user)
            return safe_users
        except Exception as e:
            logging.error(f"Error in search_users_by_name: {str(e)}")
            raise

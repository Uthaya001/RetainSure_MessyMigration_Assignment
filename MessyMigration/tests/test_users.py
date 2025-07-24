"""
Unit Tests for User Management API
Tests for the main user endpoints and functionality
"""

import pytest
import json
import os
import tempfile
from app import create_app
from models.db import init_db

class TestUserAPI:
    """Test class for User API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client with temporary database"""
        # Create temporary database file
        db_fd, db_path = tempfile.mkstemp()
        
        # Store original environment variable
        original_db_path = os.environ.get('DATABASE_PATH')
        
        try:
            # Set environment first
            os.environ['DATABASE_PATH'] = db_path
            
            # Initialize test database
            init_db(db_path)
            
            # Set up test app
            app = create_app()
            app.config['TESTING'] = True
            
            with app.test_client() as client:
                yield client
        
        finally:
            # Clean up
            os.close(db_fd)
            if os.path.exists(db_path):
                os.unlink(db_path)
            
            # Restore original environment variable
            if original_db_path:
                os.environ['DATABASE_PATH'] = original_db_path
            elif 'DATABASE_PATH' in os.environ:
                del os.environ['DATABASE_PATH']
    
    def test_get_users_empty(self, client):
        """Test GET /users with empty database"""
        response = client.get('/users')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
    
    def test_create_user_valid(self, client):
        """Test POST /users with valid data"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        }
        
        response = client.post('/users', 
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == user_data['name']
        assert data['email'] == user_data['email']
        assert 'password' not in data  # Password should not be returned
        assert 'id' in data
        assert 'created_at' in data
    
    def test_create_user_invalid_email(self, client):
        """Test POST /users with invalid email"""
        user_data = {
            "name": "John Doe",
            "email": "invalid-email",
            "password": "password123"
        }
        
        response = client.post('/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid email format' in data['error']
    
    def test_create_user_missing_fields(self, client):
        """Test POST /users with missing required fields"""
        user_data = {
            "name": "John Doe"
            # Missing email and password
        }
        
        response = client.post('/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_user_weak_password(self, client):
        """Test POST /users with weak password"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "123"  # Too short
        }
        
        response = client.post('/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Password must be at least 6 characters' in data['error']
    
    def test_get_users_with_data(self, client):
        """Test GET /users after creating users"""
        # Create a user first
        user_data = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password": "password123"
        }
        
        client.post('/users',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Get all users
        response = client.get('/users')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['name'] == user_data['name']
        assert data[0]['email'] == user_data['email']
        assert 'password' not in data[0]
    
    def test_search_users_by_name(self, client):
        """Test GET /search?name=xyz"""
        # Create test users
        users = [
            {"name": "John Smith", "email": "john@example.com", "password": "password123"},
            {"name": "Jane Doe", "email": "jane@example.com", "password": "password123"},
            {"name": "Bob Johnson", "email": "bob@example.com", "password": "password123"}
        ]
        
        for user in users:
            client.post('/users',
                       data=json.dumps(user),
                       content_type='application/json')
        
        # Search for "John"
        response = client.get('/search?name=John')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2  # John Smith and Bob Johnson
        
        # Search for "Jane"
        response = client.get('/search?name=Jane')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['name'] == "Jane Doe"
    
    def test_search_users_missing_parameter(self, client):
        """Test GET /search without name parameter"""
        response = client.get('/search')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Name parameter is required' in data['error']
    
    def test_login_valid_credentials(self, client):
        """Test POST /login with valid credentials"""
        # Create a user first
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
        
        client.post('/users',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Test login
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = client.post('/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Login successful'
        assert 'user' in data
        assert data['user']['email'] == login_data['email']
    
    def test_login_invalid_credentials(self, client):
        """Test POST /login with invalid credentials"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post('/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid credentials' in data['error']
    
    def test_update_user(self, client):
        """Test PUT /user/<id> endpoint"""
        # Create a user first
        user_data = {
            "name": "Original Name",
            "email": "original@example.com",
            "password": "password123"
        }
        
        response = client.post('/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        user = json.loads(response.data)
        user_id = user['id']
        
        # Update the user
        update_data = {
            "name": "Updated Name"
        }
        
        response = client.put(f'/user/{user_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == "Updated Name"
        assert data['email'] == user_data['email']  # Email should remain unchanged
    
    def test_update_nonexistent_user(self, client):
        """Test PUT /user/<id> with non-existent user"""
        update_data = {
            "name": "Updated Name"
        }
        
        response = client.put('/user/999',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'User not found' in data['error']
    
    def test_delete_user(self, client):
        """Test DELETE /user/<id> endpoint"""
        # Create a user first
        user_data = {
            "name": "To Delete",
            "email": "delete@example.com",
            "password": "password123"
        }
        
        response = client.post('/users',
                              data=json.dumps(user_data),
                              content_type='application/json')
        user = json.loads(response.data)
        user_id = user['id']
        
        # Delete the user
        response = client.delete(f'/user/{user_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'deleted successfully' in data['message']
        
        # Verify user is deleted
        response = client.get('/users')
        users = json.loads(response.data)
        assert len(users) == 0
    
    def test_delete_nonexistent_user(self, client):
        """Test DELETE /user/<id> with non-existent user"""
        response = client.delete('/user/999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'User not found' in data['error']

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

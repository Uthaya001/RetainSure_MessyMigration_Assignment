"""
User Routes Module
Handles all user-related HTTP endpoints
"""

from flask import Blueprint, request, jsonify
from services.user_service import UserService
from utils.validation import validate_user_data, validate_login_data
import logging

user_bp = Blueprint('users', __name__)
user_service = UserService()

@user_bp.route('/', methods=['GET'])
def home():
    """Root endpoint - API information"""
    return jsonify({
        "message": "User Management API - Refactored",
        "version": "1.0.0",
        "endpoints": {
            "GET /users": "List all users",
            "POST /users": "Create a new user",
            "PUT /user/<id>": "Update a user",
            "DELETE /user/<id>": "Delete a user",
            "POST /login": "User authentication",
            "GET /search?name=xyz": "Search users by name"
        }
    }), 200

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = user_service.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        logging.error(f"Error fetching users: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json(force=True)
        print("Received user data:", data)  # For debugging

        # Validate input data
        validation_result = validate_user_data(data)
        if not validation_result["valid"]:
            return jsonify({"error": validation_result["message"]}), 400

        # Create user
        result = user_service.create_user(data)
        if result["success"]:
            return jsonify(result["user"]), 201
        else:
            return jsonify({"error": result["message"]}), 400

    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    try:
        data = request.get_json(force=True)

        # Validate input data (partial for update)
        validation_result = validate_user_data(data, partial=True)
        if not validation_result["valid"]:
            return jsonify({"error": validation_result["message"]}), 400

        # Update user
        result = user_service.update_user(user_id, data)
        if result["success"]:
            return jsonify(result["user"]), 200
        elif result["message"] == "User not found":
            return jsonify({"error": "User not found"}), 404
        else:
            return jsonify({"error": result["message"]}), 400

    except Exception as e:
        logging.error(f"Error updating user {user_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        result = user_service.delete_user(user_id)
        if result["success"]:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        logging.error(f"Error deleting user {user_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json(force=True)

        # Validate login data
        validation_result = validate_login_data(data)
        if not validation_result["valid"]:
            return jsonify({"error": validation_result["message"]}), 400

        # Authenticate
        result = user_service.authenticate_user(data.get('email'), data.get('password'))
        if result["success"]:
            return jsonify({
                "message": "Login successful",
                "user": result["user"]
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@user_bp.route('/search', methods=['GET'])
def search_users():
    """Search users by name"""
    try:
        name = request.args.get('name')
        if not name:
            return jsonify({"error": "Name parameter is required"}), 400

        name = name.strip()
        if len(name) < 1:
            return jsonify({"error": "Search term must be at least 1 character"}), 400

        users = user_service.search_users_by_name(name)
        return jsonify(users), 200

    except Exception as e:
        logging.error(f"Error searching users: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

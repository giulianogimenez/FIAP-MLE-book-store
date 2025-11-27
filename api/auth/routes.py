"""
Authentication routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from api.auth.models import user_repository

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint
    
    Request body:
        {
            "username": "admin",
            "password": "admin123"
        }
    
    Response:
        {
            "access_token": "eyJ...",
            "refresh_token": "eyJ...",
            "user": {
                "username": "admin",
                "role": "admin"
            }
        }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Missing request body'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({
            'error': 'Missing credentials',
            'message': 'Username and password are required'
        }), 400
    
    # Find user
    user = user_repository.find_by_username(username)
    
    if not user or not user.check_password(password):
        return jsonify({
            'error': 'Invalid credentials',
            'message': 'Username or password is incorrect'
        }), 401
    
    # Create tokens with additional claims
    additional_claims = {
        'role': user.role
    }
    
    access_token = create_access_token(
        identity=username,
        additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(
        identity=username,
        additional_claims=additional_claims
    )
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict(),
        'message': 'Login successful'
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh token endpoint
    
    Headers:
        Authorization: Bearer <refresh_token>
    
    Response:
        {
            "access_token": "eyJ..."
        }
    """
    current_user = get_jwt_identity()
    claims = get_jwt()
    
    # Get user to include updated role
    user = user_repository.find_by_username(current_user)
    
    if not user:
        return jsonify({
            'error': 'User not found',
            'message': 'User does not exist'
        }), 404
    
    # Create new access token with current role
    additional_claims = {
        'role': user.role
    }
    
    access_token = create_access_token(
        identity=current_user,
        additional_claims=additional_claims
    )
    
    return jsonify({
        'access_token': access_token,
        'message': 'Token refreshed successfully'
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user info
    
    Headers:
        Authorization: Bearer <access_token>
    
    Response:
        {
            "username": "admin",
            "role": "admin"
        }
    """
    current_user = get_jwt_identity()
    claims = get_jwt()
    
    user = user_repository.find_by_username(current_user)
    
    if not user:
        return jsonify({
            'error': 'User not found'
        }), 404
    
    return jsonify({
        'user': user.to_dict()
    }), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register new user (demo only - in production, restrict this)
    
    Request body:
        {
            "username": "newuser",
            "password": "password123"
        }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Missing request body'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({
            'error': 'Missing data',
            'message': 'Username and password are required'
        }), 400
    
    # Check if user exists
    if user_repository.user_exists(username):
        return jsonify({
            'error': 'User already exists',
            'message': f'Username "{username}" is already taken'
        }), 409
    
    # Create user
    user = user_repository.create_user(username, password, role='user')
    
    if not user:
        return jsonify({
            'error': 'Failed to create user'
        }), 500
    
    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201


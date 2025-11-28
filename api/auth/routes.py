"""
Authentication routes

Follows Dependency Inversion Principle (DIP):
- Routes depend on UserRepository abstraction
- Repository instance is created here (can be injected from app.py in future)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from api.auth.models import UserRepository

auth_bp = Blueprint('auth', __name__)

# Dependency Injection: Create repository instance
# In production, inject this from app factory
user_repository = UserRepository(csv_file='data/users.csv')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login e obter tokens JWT
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        description: Credenciais de login
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: admin
              description: Nome de usuário (admin ou user)
            password:
              type: string
              example: admin123
              description: Senha do usuário
    responses:
      200:
        description: Login realizado com sucesso
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: Token de acesso JWT (válido por 1 hora)
            refresh_token:
              type: string
              description: Token de renovação (válido por 30 dias)
            user:
              type: object
              properties:
                username:
                  type: string
                role:
                  type: string
                  enum:
                    - user
                    - admin
            message:
              type: string
              example: Login successful
      400:
        description: Credenciais faltando
        schema:
          type: object
          properties:
            error:
              type: string
            message:
              type: string
      401:
        description: Credenciais inválidas
        schema:
          type: object
          properties:
            error:
              type: string
              example: Invalid credentials
            message:
              type: string
              example: Username or password is incorrect
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
    Renovar access token usando refresh token
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer {refresh_token}
        default: Bearer your_refresh_token_here
    responses:
      200:
        description: Token renovado com sucesso
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: Novo token de acesso
            message:
              type: string
              example: Token refreshed successfully
      401:
        description: Token inválido ou expirado
      404:
        description: Usuário não encontrado
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
    Obter informações do usuário logado
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer {access_token}
        default: Bearer your_access_token_here
    responses:
      200:
        description: Informações do usuário
        schema:
          type: object
          properties:
            user:
              type: object
              properties:
                username:
                  type: string
                  example: admin
                role:
                  type: string
                  example: admin
                  enum:
                    - user
                    - admin
      401:
        description: Não autorizado
      404:
        description: Usuário não encontrado
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
    Registrar novo usuário
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        description: Dados do novo usuário
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: novousuario
              description: Nome de usuário (único)
            password:
              type: string
              example: senha123
              description: Senha do usuário
    responses:
      201:
        description: Usuário criado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: User created successfully
            user:
              type: object
              properties:
                username:
                  type: string
                role:
                  type: string
                  example: user
      400:
        description: Dados inválidos
      409:
        description: Usuário já existe
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


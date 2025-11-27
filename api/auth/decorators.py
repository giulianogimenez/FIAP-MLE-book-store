"""
JWT decorators for authentication and authorization
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def admin_required():
    """
    Decorator to require admin role
    Use after @jwt_required()
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            
            if claims.get('role') != 'admin':
                return jsonify({
                    'error': 'Admin access required',
                    'message': 'You do not have permission to access this resource'
                }), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def role_required(required_role):
    """
    Decorator to require specific role
    Use after @jwt_required()
    
    Args:
        required_role: Role required to access the endpoint
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            
            user_role = claims.get('role')
            if user_role != required_role and user_role != 'admin':
                return jsonify({
                    'error': 'Insufficient permissions',
                    'message': f'Role "{required_role}" is required'
                }), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper


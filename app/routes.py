from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime
from flask_bcrypt import Bcrypt
import re
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
)

bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)

# Dummy user data for testing
USERS_DB = {
    "user@example.com": {
        "password": bcrypt.generate_password_hash("password123").decode('utf-8'),
        "name": "John Doe"
    }
}

# Email validation regex
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({"message": "Missing request data"}), 400
    
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    
    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({"message": "Email and password must be strings"}), 400
    
    if not re.match(EMAIL_REGEX, email):
        return jsonify({"message": "Invalid email format"}), 400

    user = USERS_DB.get(email)
    if user and bcrypt.check_password_hash(user['password'], password):
        # Generate JWT Token
        access_token = create_access_token(identity={"email": email, "name": user["name"]})
        refresh_token = create_refresh_token(identity={"email": email, "name": user["name"]})

        return jsonify({
            "message": "Login successful!",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {"email": email, "name": user["name"]}
        }), 200
    return jsonify({"message": "Invalid email or password"}), 401

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()

    return jsonify({
        "message": "Access granted",
        "user": current_user
    }), 200

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Requires a refresh token
def refresh():
    current_user = get_jwt_identity()
    # Create a new access token
    access_token = create_access_token(identity=current_user)
    return jsonify({
        "access_token": access_token
    }), 200
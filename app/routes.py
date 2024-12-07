from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)

# Dummy user data for testing
USERS_DB = {
    "user@example.com": {
        "password": bcrypt.generate_password_hash("password123").decode('utf-8'),
        "name": "John Doe"
    }
}

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = USERS_DB.get(email)
    if user and bcrypt.check_password_hash(user['password'], password):
        # Generate JWT Token
        token = jwt.encode({
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            "message": "Login successful!",
            "token": token,
            "user": {"email": email, "name": user["name"]}
        }), 200
    return jsonify({"message": "Invalid email or password"}), 401

@auth.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing"}), 401

    try:
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({"message": "Access granted", "user": decoded})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

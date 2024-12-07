from flask_cors import CORS
from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'your_jwt_secret_key')

    from .routes import auth
    app.register_blueprint(auth, url_prefix='/api/auth')

    return app

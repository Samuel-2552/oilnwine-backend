from flask_cors import CORS
from flask import Flask
import os
from flask_jwt_extended import JWTManager

from config import Config

def create_app(config_name="development"):
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Load configuration from config.py
    # app.config.from_object(f"config.{config_name.capitalize()}Config")

    app.config.from_object(Config)  # Load config

    # Initialize Flask-JWT-Extended
    JWTManager(app)

    # Register Blueprints
    from .routes import auth
    app.register_blueprint(auth, url_prefix='/api/auth')

    return app


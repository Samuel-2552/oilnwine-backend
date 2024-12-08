import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", None)  # Expecting this to be set in env
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', None)  # Expecting this to be set in env
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '180'))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', '3600'))
    
    # Ensure JWT_ACCESS_TOKEN_EXPIRES is an integer
    try:
        JWT_ACCESS_TOKEN_EXPIRES = int(JWT_ACCESS_TOKEN_EXPIRES)
    except ValueError:
        raise ValueError(f"Invalid value for JWT_ACCESS_TOKEN_EXPIRES: {JWT_ACCESS_TOKEN_EXPIRES}")
    
    DEBUG = False

    # Ensure that the essential keys are set
    if SECRET_KEY is None:
        raise ValueError("SECRET_KEY must be set in the environment variables.")
    
    if JWT_SECRET_KEY is None:
        raise ValueError("JWT_SECRET_KEY must be set in the environment variables.")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

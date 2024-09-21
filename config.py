import os
from dotenv import load_dotenv

# Load environment variables from credentials.env
load_dotenv('.env')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    
    # MongoDB Configuration
    MONGO_USER = os.environ.get('MONGO_USER')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    MONGO_DB = os.environ.get('MONGO_DB')
    MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION')
    MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')  # Default to localhost
    MONGO_PORT = os.environ.get('MONGO_PORT', 27017)         # Default MongoDB port
    
    # Construct MongoDB URI
    MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/?retryWrites=true&w=majority&appName=web-chat-app"

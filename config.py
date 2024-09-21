import os
from dotenv import load_dotenv

# Load environment variables from credentials.env
load_dotenv('credentials.env')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    # Add other configuration variables as needed, e.g.:
    # DATABASE_URI = os.environ.get('DATABASE_URI')

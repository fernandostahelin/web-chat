import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gunicorn configuration
bind = f"{os.getenv('FLASK_HOST', '0.0.0.0')}:{os.getenv('FLASK_PORT', '8000')}"
workers = 1
worker_class = 'eventlet'
wsgi_app = 'run:socketio'  # Changed from 'run:app' to 'run:socketio'

# Enable threading
threads = 4

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
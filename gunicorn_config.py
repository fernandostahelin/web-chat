import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gunicorn configuration
bind = f"{os.getenv('FLASK_HOST', '0.0.0.0')}:{os.getenv('FLASK_PORT', '5000')}"
workers = 1
worker_class = 'eventlet'
wsgi_app = 'run:app'

# Enable threading
threads = 4

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
import os
from dotenv import load_dotenv


load_dotenv()


bind = f"{os.getenv('FLASK_HOST', '0.0.0.0')}:{os.getenv('FLASK_PORT', '8000')}"
workers = 1
worker_class = 'eventlet'
threads = 4


accesslog = '-'
errorlog = '-'
loglevel = 'info'
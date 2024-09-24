import logging
import os

from dotenv import load_dotenv

from app.app import app, socketio

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

try:
    logger.info("Successfully imported app and socketio")
except Exception as e:
    logger.error(f"Error importing app: {e}", exc_info=True)
    raise

# Expose the SocketIO instance for Gunicorn
# No need for socketio.run() here when using Gunicorn

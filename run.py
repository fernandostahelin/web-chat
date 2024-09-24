eventlet.monkey_patch()

import logging
import os

import eventlet
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

if __name__ == "__main__":
    try:
        host: str = os.getenv("FLASK_HOST", "0.0.0.0")
        port: int = int(os.getenv("FLASK_PORT", 5000))

        logger.info(f"Starting SocketIO server on {host}:{port}...")
        socketio.run(app, host=host, port=port)
    except Exception as e:
        logger.error(f"Error running the app: {e}", exc_info=True)

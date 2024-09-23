import eventlet

eventlet.monkey_patch()

import logging

logging.getLogger("engineio").setLevel(logging.DEBUG)
logging.getLogger("socketio").setLevel(logging.DEBUG)
import os
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

try:
    from app.app import app, socketio

    logger.info("Successfully imported app and socketio")
except Exception as e:
    logger.error(f"Error importing app: {e}", exc_info=True)
    raise

if __name__ == "__main__":
    try:
        host = os.getenv("FLASK_HOST", "127.0.0.1")
        port = int(os.getenv("FLASK_PORT", 5000))

        logger.info(f"Starting SocketIO server on {host}:{port}...")
        socketio.run(app, host=host, port=port, debug=True, use_reloader=False)
    except Exception as e:
        logger.error(f"Error running the app: {e}", exc_info=True)

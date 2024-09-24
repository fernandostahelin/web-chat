import logging
import uuid  # For generating unique session IDs if needed
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from flask import Flask, render_template, request
from flask_socketio import SocketIO  # Import request from flask_socketio
from flask_socketio import emit
from pymongo import MongoClient
from pymongo import collection as pymongo_collection  # Import specific types
from pymongo import database
from pymongo.errors import ServerSelectionTimeoutError

from config import Config

# Configure Logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG for detailed logs
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SocketIO with specific parameters
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")


# Add a route for the homepage
@app.route("/")
def index() -> str:
    return render_template("index.html")


client: Optional[MongoClient] = None
db: Optional[database.Database] = None  # Use the specific type for database
collection: Optional[pymongo_collection.Collection] = (
    None  # Use the specific type for collection
)


def get_db() -> Optional[pymongo_collection.Collection]:  # Update return type
    global client, db, collection
    if client is None:
        try:
            client = MongoClient(Config.MONGO_URI)
            client.admin.command("ping")
            logger.info("Successfully connected to MongoDB Atlas!")
            db_name: Optional[str] = Config.MONGO_DB
            collection_name: Optional[str] = Config.MONGO_COLLECTION
            if db_name and collection_name:
                db = client[db_name]
                collection = db[collection_name]
            else:
                logger.error(
                    "Database or collection name is not set\
                          in the configuration."
                )
        except ServerSelectionTimeoutError:
            logger.error(
                "Unable to connect to MongoDB Atlas.\
                    Will retry on next request."
            )
    return collection


@app.before_request
def before_request() -> None:
    get_db()


connected_users: Dict[str, str] = {}


# Move SocketIO initialization here, after all routes are defined
@socketio.on("connect")
def handle_connect() -> None:
    session_id = str(uuid.uuid4())
    connected_users[request.sid] = session_id  # request.sid is now recognized
    logger.info(f"User connected: {session_id}")
    # Send the session ID to the client
    emit('session', {'session_id': session_id})


@socketio.on("disconnect")
def handle_disconnect() -> None:
    session_id = connected_users.pop(
        request.sid, None
    )  # request.sid is now recognized
    logger.info(f"User disconnected: {session_id}")


@socketio.on("message")
def handle_message(message: Dict[str, Any]) -> None:
    """
    Handle incoming text messages.
    Expects a dictionary with 'text' and 'id'.
    """
    text: Optional[str] = message.get("text")
    message_id: Optional[str] = message.get(
        "id"
    )  # Unique identifier for the message

    if not text:
        logger.warning("Received empty text message.")
        return  # Optionally handle empty messages

    # Generate current UTC timestamp in ISO 8601 format
    timestamp: str = datetime.now(timezone.utc).isoformat()

    # Retrieve the session_id for the current user
    session_id: str = connected_users.get(
        request.sid, "anonymous"
    )  # request.sid is now recognized

    # Prepare the message document
    message_doc: Dict[str, Any] = {
        "message_id": message_id,
        "session_id": session_id,
        "message_type": "text",
        "content": text,
        "timestamp": timestamp,
    }

    try:
        collection = get_db()
        if collection:
            collection.insert_one(message_doc)
            logger.debug(f"Inserted message into MongoDB: {message_doc}")
    except Exception as e:
        logger.error(f"Error inserting message into MongoDB: {e}")

    # Emit the message to all connected clients
    emit(
        "message",
        {
            "text": text,
            "timestamp": timestamp,
            "id": message_id,
            "session_id": session_id,  # Optionally include session_id
        },
        broadcast=True,
    )


@socketio.on("image")
def handle_image(message: Dict[str, Any]) -> None:
    """
    Handle incoming image messages.
    Expects a dictionary with 'image' (Base64 string) and 'id'.
    """
    image_data: Optional[str] = message.get("image")
    message_id: Optional[str] = message.get(
        "id"
    )  # Unique identifier for the message

    if not image_data:
        logger.warning("Received empty image data.")
        return  # Optionally handle empty image data

    # Generate current UTC timestamp in ISO 8601 format
    timestamp: str = datetime.now(timezone.utc).isoformat()

    # Retrieve the session_id for the current user
    session_id: str = connected_users.get(
        request.sid, "anonymous"
    )  # request.sid is now recognized

    # Prepare the image document
    image_doc: Dict[str, Any] = {
        "message_id": message_id,
        "session_id": session_id,
        "message_type": "image",
        "content": image_data,  # Base64 encoded image
        "timestamp": timestamp,
    }

    try:
        collection = get_db()
        if collection:
            collection.insert_one(image_doc)
            logger.debug(f"Inserted image into MongoDB: {image_doc}")
    except Exception as e:
        logger.error(f"Error inserting image into MongoDB: {e}")

    # Emit the image to all connected clients
    emit(
        "image",
        {
            "image": image_data,
            "timestamp": timestamp,
            "id": message_id,
            "session_id": session_id,  # Optionally include session_id
        },
        broadcast=True,
    )

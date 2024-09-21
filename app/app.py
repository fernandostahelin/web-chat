from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from config import Config
from datetime import datetime, timezone
from pymongo import MongoClient
import uuid  # For generating unique session IDs if needed
import logging

app = Flask(__name__)
app.config.from_object(Config)

# Configure Logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG for detailed logs
logger = logging.getLogger(__name__)

socketio = SocketIO(app)

# Initialize MongoDB Client
client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB]
collection = db[Config.MONGO_COLLECTION]

# Optional: If you don't have user sessions set up, you can generate a unique session ID per connection
# This example uses UUIDs to assign a unique session ID to each user upon connection
connected_users = {}

@socketio.on('connect')
def handle_connect():
    # Generate a unique session ID for the user
    session_id = str(uuid.uuid4())
    connected_users[request.sid] = session_id
    logger.info(f"User connected: {session_id}")

@socketio.on('disconnect')
def handle_disconnect():
    session_id = connected_users.pop(request.sid, None)
    logger.info(f"User disconnected: {session_id}")

@socketio.on('message')
def handle_message(message):
    """
    Handle incoming text messages.
    Expects a dictionary with 'text' and 'id'.
    """
    text = message.get('text')
    message_id = message.get('id')  # Unique identifier for the message

    if not text:
        logger.warning("Received empty text message.")
        return  # Optionally handle empty messages

    # Generate current UTC timestamp in ISO 8601 format
    timestamp = datetime.now(timezone.utc).isoformat()

    # Retrieve the session_id for the current user
    session_id = connected_users.get(request.sid, 'anonymous')

    # Prepare the message document
    message_doc = {
        'message_id': message_id,
        'session_id': session_id,
        'message_type': 'text',
        'content': text,
        'timestamp': timestamp
    }

    # Insert the message into MongoDB
    try:
        collection.insert_one(message_doc)
        logger.debug(f"Inserted message into MongoDB: {message_doc}")
    except Exception as e:
        logger.error(f"Error inserting message into MongoDB: {e}")

    # Emit the message to all connected clients
    emit('message', {
        'text': text,
        'timestamp': timestamp,
        'id': message_id,
        'session_id': session_id  # Optionally include session_id
    }, broadcast=True)

@socketio.on('image')
def handle_image(message):
    """
    Handle incoming image messages.
    Expects a dictionary with 'image' (Base64 string) and 'id'.
    """
    image_data = message.get('image')
    message_id = message.get('id')  # Unique identifier for the message

    if not image_data:
        logger.warning("Received empty image data.")
        return  # Optionally handle empty image data

    # Generate current UTC timestamp in ISO 8601 format
    timestamp = datetime.now(timezone.utc).isoformat()

    # Retrieve the session_id for the current user
    session_id = connected_users.get(request.sid, 'anonymous')

    # Prepare the image document
    image_doc = {
        'message_id': message_id,
        'session_id': session_id,
        'message_type': 'image',
        'content': image_data,  # Base64 encoded image
        'timestamp': timestamp
    }

    # Insert the image into MongoDB
    try:
        collection.insert_one(image_doc)
        logger.debug(f"Inserted image into MongoDB: {image_doc}")
    except Exception as e:
        logger.error(f"Error inserting image into MongoDB: {e}")

    # Emit the image to all connected clients
    emit('image', {
        'image': image_data,
        'timestamp': timestamp,
        'id': message_id,
        'session_id': session_id  # Optionally include session_id
    }, broadcast=True)
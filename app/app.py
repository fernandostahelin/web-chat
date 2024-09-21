from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from config import Config
from datetime import datetime, timezone

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    """
    Handle incoming text messages.
    Expects a dictionary with 'text' and 'id'.
    """
    text = message.get('text')
    message_id = message.get('id')  # Unique identifier for the message

    if not text:
        return  # Optionally handle empty messages

    # Generate current UTC timestamp in ISO 8601 format
    timestamp = datetime.now(timezone.utc).isoformat()

    # Emit message as a dictionary containing text, timestamp, and id
    emit('message', {'text': text, 'timestamp': timestamp, 'id': message_id}, broadcast=True)

@socketio.on('image')
def handle_image(message):
    """
    Handle incoming image messages.
    Expects a dictionary with 'image' (Base64 string) and 'id'.
    """
    image_data = message.get('image')
    message_id = message.get('id')  # Unique identifier for the message

    if not image_data:
        return  # Optionally handle empty image data

    # Generate current UTC timestamp in ISO 8601 format
    timestamp = datetime.now(timezone.utc).isoformat()

    # Emit image as a dictionary containing image data, timestamp, and id
    emit('image', {'image': image_data, 'timestamp': timestamp, 'id': message_id}, broadcast=True)
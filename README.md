# Web Chat Application

This is a real-time web chat application built using Flask, Flask-SocketIO, and MongoDB. The application allows users to send text messages and images, which are stored in a MongoDB database. The frontend is built with HTML, CSS, and JavaScript, and uses Bootstrap for styling.

## Features

- Real-time messaging using WebSockets
- Image upload and capture via webcam
- Messages and images are stored in MongoDB
- User sessions are managed using unique session IDs
- Responsive design with Bootstrap

## Prerequisites

- Python 3.8+
- MongoDB instance (local or cloud)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/web-chat.git
    cd web-chat
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following variables:

    ```env
    FLASK_DEBUG=False
    MONGO_USER=webchat
    MONGO_PASSWORD=dsWcIXV3QfpsZ2Km
    MONGO_DB=messages_db
    MONGO_COLLECTION=chat-messages
    FLASK_HOST=127.0.0.1
    FLASK_PORT=5000
    MONGO_URI="mongodb+srv://webchat:dsWcIXV3QfpsZ2Km@web-chat-app.ces2z.mongodb.net/?retryWrites=true&w=majority&appName=web-chat-app"
    ```

## Running the Application

1. **Start the Flask application:**

    ```sh
    python run.py
    ```

2. **Open your browser and navigate to:**

    ```
    http://127.0.0.1:5000
    ```


## Makefile Commands

- **Format code:**

    ```sh
    make format
    ```

- **Lint code:**

    ```sh
    make lint
    ```

- **Type check:**

    ```sh
    make type
    ```

- **Run all checks (format, lint, type):**

    ```sh
    make ci
    ```

## Usage

### Sending Messages

- Type your message in the input field and click the "Send" button or press "Enter" to send a text message.

### Sending Images

- Click the camera button to capture an image using your webcam.
- Click the gallery button to upload an image from your device.

### Viewing Messages

- Messages and images will appear in the chat window in real-time.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the WTFPL License. See the [LICENSE](LICENSE) file for details.
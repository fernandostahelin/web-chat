const socket = io();
const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const cameraButton = document.getElementById('camera-button');
const galleryButton = document.getElementById('gallery-button');
const cameraInput = document.getElementById('camera-input');
const galleryInput = document.getElementById('gallery-input');

// Keep track of sent messages using unique identifiers
let myMessageIds = new Set();

// Function to generate a simple unique ID for each message
function generateMessageId() {
    return '_' + Math.random().toString(36).substr(2, 9);
}

// Event listener for camera button
cameraButton.addEventListener('click', () => {
    cameraInput.click();
});

// Event listener for gallery button
galleryButton.addEventListener('click', () => {
    galleryInput.click();
});

// Handle image selection from camera
cameraInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
        sendImage(file);
    }
    // Reset the input value to allow re-uploading the same image if needed
    cameraInput.value = '';
});

// Handle image selection from gallery
galleryInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
        sendImage(file);
    }
    // Reset the input value to allow re-uploading the same image if needed
    galleryInput.value = '';
});

// Function to convert image file to Base64 and send
function sendImage(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const imageBase64 = e.target.result; // This is the base64 string
        const messageId = generateMessageId();
        socket.emit('image', { image: imageBase64, id: messageId });
        myMessageIds.add(messageId);
    };
    reader.readAsDataURL(file);
}

// Listen for 'message' events
socket.on('message', function(message) {
    renderMessage(message);
});

// Listen for 'image' events
socket.on('image', function(message) {
    renderMessage(message);
});

// Function to render messages and images
function renderMessage(message) {
    // Create a container div for the message
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message-container');

    // Determine if the message is text or image
    if (message.text) {
        // Text message
        const messageElement = document.createElement('p');
        messageElement.textContent = message.text;
        messageElement.classList.add('message-text');

        // Create a span for the timestamp
        const timestamp = document.createElement('span');
        timestamp.classList.add('timestamp');
        const localTime = new Date(message.timestamp);
        if (isNaN(localTime)) {
            timestamp.textContent = 'Invalid Date';
        } else {
            timestamp.textContent = localTime.toLocaleString();
        }

        // Append timestamp to the message
        messageElement.appendChild(timestamp);
        messageContainer.appendChild(messageElement);
    }

    if (message.image) {
        // Image message
        const imageElement = document.createElement('img');
        imageElement.src = message.image;
        imageElement.alt = 'User Image';
        imageElement.classList.add('message-image');

        // Create a span for the timestamp
        const timestamp = document.createElement('span');
        timestamp.classList.add('timestamp');
        const localTime = new Date(message.timestamp);
        if (isNaN(localTime)) {
            timestamp.textContent = 'Invalid Date';
        } else {
            timestamp.textContent = localTime.toLocaleString();
        }

        // Append timestamp to the image
        imageElement.appendChild(timestamp);
        messageContainer.appendChild(imageElement);
    }

    // Check if the message was sent by the current user using the unique ID
    if (message.id && myMessageIds.has(message.id)) {
        messageContainer.classList.add('sent');
        myMessageIds.delete(message.id); // Remove the ID after marking
    }

    // Append the message container to the messages div
    messagesDiv.appendChild(messageContainer);

    // Scroll to the bottom of the messages container
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Function to send text messages
function sendMessage() {
    const messageText = messageInput.value.trim();
    if (messageText) {
        const messageId = generateMessageId(); // Generate a unique ID for the message
        socket.emit('message', { text: messageText, id: messageId });
        myMessageIds.add(messageId); // Track sent message by ID
        messageInput.value = '';
    }
}

// Add event listener for Enter key to send messages
messageInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});
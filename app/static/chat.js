const socket = io();
const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('message-input');

socket.on('message', function(message) {
    const messageElement = document.createElement('p');
    messageElement.textContent = message;
    messagesDiv.appendChild(messageElement);
});

function sendMessage() {
    const message = messageInput.value;
    if (message) {
        socket.emit('message', message);
        messageInput.value = '';
    }
}

// Add event listener for Enter key
messageInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});
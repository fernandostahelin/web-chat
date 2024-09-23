const socket = io();

// DOM elements
const chatContainer = document.querySelector(".chat-container");
const messagesDiv = document.getElementById("messages");
const messageInput = document.getElementById("message-input");
const cameraButton = document.getElementById("camera-button");
const galleryButton = document.getElementById("gallery-button");
const galleryInput = document.getElementById("gallery-input");
const sendButton = document.getElementById("send-button");

// Elements for webcam modal
const webcamModalElement = document.getElementById("webcamModal");
let webcamModal;
if (webcamModalElement) {
  webcamModal = new bootstrap.Modal(webcamModalElement);
}
const webcamVideo = document.getElementById("webcamVideo");
const webcamCanvas = document.getElementById("webcamCanvas");
const captureButton = document.getElementById("captureButton");

// Keep track of sent messages using unique identifiers
let myMessageIds = new Set();

// Function to generate a simple unique ID for each message
function generateMessageId() {
  return "_" + Math.random().toString(36).slice(2, 9);
}

// Event listener for camera button (opens webcam modal)
cameraButton.addEventListener("click", () => {
  startWebcam();
});

// Event listener for gallery button
galleryButton.addEventListener("click", () => {
  galleryInput.click();
});

// Handle image selection from gallery
galleryInput.addEventListener("change", function (event) {
  const file = event.target.files[0];
  if (file && file.type.startsWith("image/")) {
    sendImage(file);
  }
  // Reset the input value to allow re-uploading the same image if needed
  galleryInput.value = "";
});

// Function to convert image file to Base64 and send
function sendImage(file) {
  const reader = new FileReader();
  reader.onload = function (e) {
    const imageBase64 = e.target.result; // This is the base64 string
    const messageId = generateMessageId();
    socket.emit("image", { image: imageBase64, id: messageId });
    myMessageIds.add(messageId);
  };
  reader.readAsDataURL(file);
}

// Function to start the webcam
function startWebcam() {
  if (!webcamModal) {
    console.error("Webcam modal not found!");
    return;
  }

  // Show the webcam modal
  webcamModal.show();

  // Access the webcam
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      webcamVideo.srcObject = stream;
      webcamVideo.play();
    })
    .catch((err) => {
      console.error("Error accessing webcam: ", err);
      alert("Unable to access the webcam. Please check your permissions.");
      webcamModal.hide();
    });
}

// Event listener for capture button in modal
captureButton.addEventListener("click", () => {
  // Draw the video frame to the canvas
  webcamCanvas.width = webcamVideo.videoWidth;
  webcamCanvas.height = webcamVideo.videoHeight;
  const context = webcamCanvas.getContext("2d");
  context.drawImage(webcamVideo, 0, 0, webcamCanvas.width, webcamCanvas.height);

  // Convert the canvas to a Base64 image
  const imageBase64 = webcamCanvas.toDataURL("image/png");

  // Send the captured image
  const messageId = generateMessageId();
  socket.emit("image", { image: imageBase64, id: messageId });
  myMessageIds.add(messageId);

  // Stop all video streams to free the webcam
  webcamVideo.srcObject.getTracks().forEach((track) => track.stop());

  // Hide the webcam modal
  webcamModal.hide();
});

// Listen for 'message' and 'image' events from the server
socket.on("message", function (message) {
  renderMessage(message);
});

socket.on("image", function (message) {
  renderMessage(message);
});

// Function to render messages and images
function renderMessage(message) {
  // Create a container div for the message
  const messageContainer = document.createElement("div");
  messageContainer.classList.add("message-container");

  // Determine if the message is text or image
  if (message.text) {
    // Text message
    const messageElement = document.createElement("p");
    messageElement.textContent = message.text;
    messageElement.classList.add("message-text");

    // Create a span for the timestamp
    const timestamp = document.createElement("span");
    timestamp.classList.add("timestamp");
    const localTime = new Date(message.timestamp);
    if (isNaN(localTime)) {
      timestamp.textContent = "Invalid Date";
    } else {
      timestamp.textContent = localTime.toLocaleString();
    }

    // Append timestamp to the message
    messageElement.appendChild(timestamp);
    messageContainer.appendChild(messageElement);
  }

  if (message.image) {
    // Image message
    const imageElement = document.createElement("img");
    imageElement.src = message.image;
    imageElement.alt = "User Image";
    imageElement.classList.add("message-image");

    // Append image to the message container
    messageContainer.appendChild(imageElement);

    // Create a span for the timestamp
    const timestamp = document.createElement("span");
    timestamp.classList.add("timestamp");
    const localTime = new Date(message.timestamp);
    if (isNaN(localTime)) {
      timestamp.textContent = "Invalid Date";
    } else {
      timestamp.textContent = localTime.toLocaleString();
    }

    // Append timestamp below the image
    messageContainer.appendChild(timestamp);
  }

  // Determine if the message was sent by the current user
  // Assuming you have access to the current user's session_id in the frontend
  const currentSessionId = getCurrentSessionId(); // Implement this function based on your setup

  if (message.session_id === currentSessionId) {
    messageContainer.classList.add("sent");
  } else {
    messageContainer.classList.add("received");
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
    socket.emit("message", { text: messageText, id: messageId });
    myMessageIds.add(messageId); // Track sent message by ID
    messageInput.value = "";
  }
}

// Event listener for Send button
sendButton.addEventListener("click", () => {
  sendMessage();
});

// Add event listener for Enter key to send messages
messageInput.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});

let currentSessionId = null;

// Add this at the beginning of your file, after initializing the socket
socket.on('session', function(data) {
    currentSessionId = data.session_id;
    console.log('Session ID received:', currentSessionId);
});

// Implement the getCurrentSessionId function
function getCurrentSessionId() {
    if (currentSessionId === null) {
        console.error('Session ID not set. User might not be properly connected.');
        return 'unknown';
    }
    return currentSessionId;
}

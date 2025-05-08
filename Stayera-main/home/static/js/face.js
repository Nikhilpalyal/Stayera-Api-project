const video = document.getElementById("cameraFeed");
const captureBtn = document.getElementById("captureBtn");
const registerBtn = document.getElementById("registerBtn");
const canvas = document.getElementById("canvas");
const message = document.getElementById("message");

// Start the camera
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error("Error accessing camera:", error);
        message.style.color = "red";
        message.textContent = "Camera access denied!";
    });

let imageData = null;

captureBtn.addEventListener("click", () => {
    const ctx = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Get base64 data
    imageData = canvas.toDataURL("image/jpeg");
    registerBtn.style.display = "block";
    message.style.color = "blue";
    message.textContent = "Face Captured! Click Register to submit.";
});

registerBtn.addEventListener("click", () => {
    if (!imageData) {
        message.style.color = "red";
        message.textContent = "No image captured!";
        return;
    }

    fetch("/registerface", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()  // if CSRF is enabled
        },
        body: new URLSearchParams({
            image_data: imageData
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            message.style.color = "green";
            message.textContent = data.message || "Registration successful!";
        } else {
            message.style.color = "red";
            message.textContent = data.message || "Registration failed.";
        }
    })
    .catch(error => {
        console.error("Error during registration:", error);
        message.style.color = "red";
        message.textContent = "An error occurred.";
    });
});

// CSRF token helper (only needed if CSRF is not exempted)
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue;
}

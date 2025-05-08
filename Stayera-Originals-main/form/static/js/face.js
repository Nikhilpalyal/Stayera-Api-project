// Access the camera
const video = document.getElementById("cameraFeed");
const captureBtn = document.getElementById("captureBtn");
const canvas = document.getElementById("canvas");
const scanBtn = document.getElementById("scanBtn");
const message = document.getElementById("message");
const extractedTextDiv = document.getElementById("extractedText");

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error("Error accessing camera:", error);
        message.style.color = "red";
        message.textContent = "Camera access denied!";
    });

captureBtn.addEventListener("click", () => {
    const ctx = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    scanBtn.style.display = "block";
    message.style.color = "blue";
    message.textContent = "ID Captured! Click Scan to process.";
});

scanBtn.addEventListener("click", () => {
    message.style.color = "blue";
    message.textContent = "Scanning ID... Please wait.";

    const imageData = canvas.toDataURL(); // Get the image data as Base64

    // Send the image to the backend for validation
    fetch("http://127.0.0.1:5000/register-id", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ image: imageData })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                extractedTextDiv.textContent = `Extracted Data: Welcome, ${data.name}`;
                message.style.color = "green";
                message.textContent = "ID Scanned Successfully! Redirecting...";

                setTimeout(() => {
                    window.location.href = "http://127.0.0.1:5000/hotels"; // Redirect to hotels page
                }, 2000);
            } else {
                message.style.color = "red";
                message.textContent = data.message;
            }
        })
        .catch(error => {
            console.error("Error:", error);
            message.style.color = "red";
            message.textContent = "Error scanning ID. Try again.";
        });
});
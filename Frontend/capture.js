// Replace with your ESP32-CAM IP Address
let esp32StreamURL = "http://<ESP32_IP>:81/stream";
let snapshotURL = "http://<ESP32_IP>/capture";

// Start ESP32-CAM Stream
function startESP32Cam() {
    let videoElement = document.getElementById("camera");
    videoElement.src = esp32StreamURL;
}

// Capture Image from ESP32-CAM
function captureImage() {
    let capturedImg = document.getElementById("captured-image");
    
    fetch(snapshotURL)
        .then(response => response.blob())
        .then(blob => {
            let imageURL = URL.createObjectURL(blob);
            capturedImg.src = imageURL;
            capturedImg.setAttribute("data-file", imageURL);
            document.querySelector(".search-btn").disabled = false;
        })
        .catch(error => console.error("Error capturing image:", error));
}

// Search Number Plate
function searchNumber() {
    let imageElement = document.getElementById("captured-image");
    let imageURL = imageElement.getAttribute("data-file");

    if (!imageURL) {
        alert("Please capture an image first.");
        return;
    }

    let loader = document.getElementById("loader");
    loader.classList.add("show");

    fetch(imageURL)
        .then(response => response.blob())
        .then(blob => {
            let file = new File([blob], "captured_plate.jpg", { type: "image/jpeg" });
            let formData = new FormData();
            formData.append("file", file);

            return fetch("http://localhost:5000/ocr-api/upload_image", {
                method: "POST",
                body: formData,
            });
        })
        .then(response => response.json())
        .then(data => {
            loader.classList.remove("show");
            if (data.success && data.user_details.success) {
                showUserDetails(data.user_details.data);
            } else {
                alert(data.user_details.message || "No matching details found.");
            }
        })
        .catch(error => {
            console.error("Error searching number:", error);
            loader.classList.remove("show");
            alert("Error: " + JSON.stringify(error));
        });
}

// Show User Details in a Popup
function showUserDetails(user) {
    if (!user) {
        alert("No user details found.");
        return;
    }

    let modalContent = `
        <span class="close-btn" onclick="closeModal()">&times;</span>
        <h3>User Details</h3>
        <p><strong>Name:</strong> ${user.name || "N/A"}</p>
        <p><strong>Plate Number:</strong> ${user.plate_number || "N/A"}</p>
        <p><strong>Status:</strong> ${user.status || "N/A"}</p>
        <p><strong>Challan Reason:</strong> ${user.challan_reason || "N/A"}</p>
        <button onclick="updateUser('${user.plate_number || 0}')">Update/Challan</button>
    `;
    document.getElementById("modal-content").innerHTML = modalContent;
    document.getElementById("userModal").style.display = "block";
}

// Update User Status and Challan Reason
function updateUser(plateNumber) {
    if (!plateNumber) {
        alert("Plate number is missing!");
        return;
    }

    let newStatus = prompt(`Enter new status for ${plateNumber} (Green, Yellow, Red):`);
    if (!newStatus) return;

    let newChallanReason = prompt(`Enter new challan reason for ${plateNumber} (or leave empty to keep current reason):`);

    fetch(`http://localhost:5000/api/update_user/${plateNumber}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            status: newStatus,
            challan_reason: newChallanReason || null
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error("Error updating user:", error));
}

// Close the Modal
function closeModal() {
    document.getElementById("userModal").style.display = "none";
}

// Logout Function
function logout() {
    window.location.href = "login.html";
}

// Start the camera on page load
window.onload = startESP32Cam;
pip freeze > requirements.txt

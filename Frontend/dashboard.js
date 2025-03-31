let currentPage = 1;
const rowsPerPage = 5;  
let totalData = [];

function loadTable() {
    fetch('http://localhost:5000/api/plates')  
    .then(response => response.json())
    .then(data => {
        totalData = data;
        displayTable();
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        alert('Failed to load user data.');
    });
}

function displayTable() {
    let tableBody = document.getElementById('data-table');
    tableBody.innerHTML = "";  

    let start = (currentPage - 1) * rowsPerPage;
    let end = start + rowsPerPage;
    let paginatedData = totalData.slice(start, end);

    paginatedData.forEach(row => {
        let tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${row.id}</td>
            <td>${row.name}</td>
            <td>${row.plate_number}</td>
            <td>${row.status}</td>
            <td>${row.challan_reason || 'N/A'}</td>
            <td>
                <button class="update-btn" onclick="updateUser('${row.plate_number}')">Update</button>
                <button class="delete-btn" onclick="deleteUser('${row.plate_number}')">Delete</button>
            </td>
        `;
        tableBody.appendChild(tr);
    });

    updatePaginationControls();
}

function updatePaginationControls() {
    document.getElementById('pageNumber').innerText = `Page ${currentPage}`;
    document.getElementById('prevBtn').disabled = currentPage === 1;
    document.getElementById('nextBtn').disabled = currentPage * rowsPerPage >= totalData.length;
}

function nextPage() {
    if (currentPage * rowsPerPage < totalData.length) {
        currentPage++;
        displayTable();
    }
}

function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        displayTable();
    }
}

function searchData() {
    let plateNumber = document.getElementById("search-input").value.trim();
    if (!plateNumber) {
        alert("Please enter a plate number.");
        return;
    }

    fetch(`http://localhost:5000/api/get_user/${plateNumber}`)
    .then(response => response.json())
    .then(data => {
        if (data.success && data.data) {
            document.getElementById("user-name").innerText = data.data.name || "N/A";
            document.getElementById("user-plate-number").innerText = data.data.plate_number || "N/A";
            document.getElementById("user-status").innerText = data.data.status || "N/A";
            document.getElementById("user-challan-reason").innerText = data.data.challan_reason || "N/A";
            document.getElementById("userDetailsModal").style.display = "block";
        } else {
            alert("User not found!");
        }
    })
    .catch(error => {
        console.error("Fetch error:", error);
        alert("Failed to fetch data.");
    });
}

function closeModal() {
    document.getElementById("userDetailsModal").style.display = "none";
}

window.onclick = function(event) {
    if (event.target === document.getElementById("userDetailsModal")) {
        closeModal();
    }
}

function updateUser(plateNumber) {
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
        loadTable();
    })
    .catch(error => console.error("Error updating user:", error));
}

function deleteUser(plateNumber) {
    if (!confirm(`Are you sure you want to delete user with plate number ${plateNumber}?`)) return;

    fetch(`http://localhost:5000/api/delete_user/${plateNumber}`, {
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadTable();
    })
    .catch(error => console.error("Error deleting user:", error));
}

function logout() {
    window.location.href = "login.html";
}

window.onload = loadTable;

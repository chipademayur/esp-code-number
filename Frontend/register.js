async function registerAdmin() {
    let username = document.getElementById("reg-username").value;
    let password = document.getElementById("reg-password").value;

    let response = await fetch("http://localhost:5000/admin/register_admin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    let result = await response.json();
    if (result.success) {
        alert("Admin Registered Successfully!");
        window.location.href = "dashboard.html";
    } else {
        alert(result.message);
    }
}

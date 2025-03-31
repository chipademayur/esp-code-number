async function login() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    let response = await fetch("http://localhost:5000/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    let result = await response.json();
    console.log(result); // Debugging to check API response

    if (result.success) {  // ✅ Fix: Check `result.success` instead of `result.status`
        localStorage.setItem("admin_logged_in", "true");
        window.location.href = "dashboard.html"; // Redirect to dashboard
    } else {
        alert("Invalid Credentials!");
    }
}


function logout() {
    fetch("http://localhost:5000/admin/logout").then(() => {
        localStorage.removeItem("admin_logged_in");
        window.location.href = "login.html";
    });
}

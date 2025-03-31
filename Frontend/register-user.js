async function register_user() {
    let name = document.getElementById("reg-username").value.trim();
    let plate_number = document.getElementById("PlateNumber").value.trim();
    let status = document.getElementById("status").value.trim();
    let challan_reason = document.getElementById("challan_reason").value.trim();

    // Validation for empty fields
    if (!name || !plate_number || !status || !challan_reason) {
        alert("Please fill in all fields before submitting.");
        return;
    }

    try {
        let response = await fetch("http://localhost:5000/api/register_user", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, plate_number, status, challan_reason })
        });

        let result = await response.json();
        if (result.success) {
            alert("User Registered Successfully!");
            window.location.href = "dashboard.html";
        } else {
            alert(result.message);
        }
    } catch (error) {
        alert("Error registering user: " + error);
        console.error("Error:", error);
    }
}

const API_BASE = "/api/users";

async function createUser() {
    const payload = {
        name: document.getElementById("name").value,
        phone_number: document.getElementById("phone").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
    };

    const response = await fetch(`${API_BASE}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    const data = await response.json();
    document.getElementById("output").textContent =
        JSON.stringify(data, null, 2);
}


async function login() {
    const form = new URLSearchParams();
    form.append("username", phone);
    form.append("password", password);

    const response = await fetch("/api/users/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: form,
    });

    const data = await response.json();
    localStorage.setItem("access_token", data.access_token);
}


async function getMe() {
    const token = localStorage.getItem("access_token");

    const response = await fetch("/api/users/me", {
        headers: {
            "Authorization": `Bearer ${token}`,
        },
    });

    const data = await response.json();
    console.log(data);
}
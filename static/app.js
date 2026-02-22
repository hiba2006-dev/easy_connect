const API_URL = "http://127.0.0.1:8000";

document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = e.target[0].value;
    const password = e.target[1].value;

    const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });

    const data = await response.json();

    if(data.access_token){
        localStorage.setItem("token", data.access_token);
        window.location.href = "dashboard.html";
    }
});

// Connection with api / our python logic
try {
    const ws = new WebSocket(
        "wss://gannon-unfiscal-reactively.ngrok-free.dev/ws",
    );
    if (ws) {
        ws.onmessage = (event) => {
            showNotification();
        };
    }
} catch (err) {
    console.log(err);
    console.log("Websocket is not open");
}

const notification = document.getElementById("notification");
const triggerHelp = document.getElementById("triggerHelp");
const request = document.getElementById("request");

function showNotification(
    message = "A user is requesting help!",
    duration = 3000,
) {
    notification.textContent = message;
    notification.classList.remove("hidden");

    request.classList.remove("hidden");
    document.getElementById("no-requests").classList.add("hidden");

    setTimeout(() => {
        notification.classList.add("hidden");
    }, duration);
}

triggerHelp.addEventListener("click", () => {
    showNotification("A user is requesting help!", 4000);
});

// ############# MAP LOGIC ##############
const map = L.map("map").setView([0, 0], 2);

// OpenStreetMap
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

// Get user locaiton
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const { latitude, longitude } = pos.coords;
            map.setView([latitude, longitude], 13);

            L.marker([latitude, longitude])
                .addTo(map)
                .bindPopup("You are here")
                .openPopup();
        },
        (err) => {
            console.error("Geolocation error:", err.message);
            showNotification("Could not get your location", 3000);
        },
    );
} else {
    showNotification("Geolocation not supported", 3000);
}

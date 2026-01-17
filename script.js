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
const request = document.getElementById("request");
const helpPersonBtn = document.getElementById("helpPersonBtn");
const crxCoordinates = [45.42193, -75.6817];

function showNotification(
    message = "A user is requesting help!",
    duration = 3000,
) {
    notification.textContent = message;
    notification.classList.remove("hidden");

    request.classList.remove("hidden");
    document.getElementById("no-requests").classList.add("hidden");

    // Currently hardcoded the location of the client in need of help
    L.marker(crxCoordinates)
        .addTo(map)
        .bindPopup("Person in need of help")
        .openPopup();

    map.setView(crxCoordinates, 18);

    setTimeout(() => {
        notification.classList.add("hidden");
    }, duration);
}

helpPersonBtn.addEventListener("click", () => {
    map.setView(crxCoordinates, 20);
});

// ############# MAP LOGIC ##############
const map = L.map("map").setView(crxCoordinates, 17);

// OpenStreetMap
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

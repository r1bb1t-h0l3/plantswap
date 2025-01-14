// Initialize the map
const map = L.map('map').setView([52.5200, 13.4050], 12);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Add a marker at the center
const marker = L.marker([52.5200, 13.4050]).addTo(map);
marker.bindPopup("<b>Berlin</b><br>Plant-Swap").openPopup();
console.log("Leaflet map script loaded successfully");

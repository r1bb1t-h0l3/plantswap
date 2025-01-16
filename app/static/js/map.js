// Check if the map container already exists

if (typeof plantSwapMap === 'undefined') {
// Initialize the map
var plantSwapMap = L.map('map').setView([52.5200, 13.4050], 12); // Center on Berlin

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(plantSwapMap);

// Add markers for each post
mapData.forEach(post => {
    L.marker([post.latitude, post.longitude])
        .addTo(plantSwapMap)
        .bindPopup(`<b>${post.plant_type}</b><br>${post.description}<br>Contact: ${post.contact_info}`);
});
}


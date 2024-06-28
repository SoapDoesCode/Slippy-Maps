from flask import Flask, request, render_template_string
import socket
import math
import random
import folium

app = Flask(__name__)

def haversine(coord1, coord2):
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    
    dlat = lat2 - lat1
    dlon = coord2[1] - coord1[1]
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371  # Radius of the Earth in kilometers
    distance_km = r * c
    return distance_km

def generate_random_coordinate_within_annulus(home, min_radius_km, max_radius_km):
    earth_radius_km = 6371
    min_radius_in_degrees = min_radius_km / earth_radius_km
    max_radius_in_degrees = max_radius_km / earth_radius_km

    while True:
        random_distance = random.uniform(min_radius_in_degrees, max_radius_in_degrees)
        random_angle = random.uniform(0, 2 * math.pi)

        delta_lat = random_distance * math.cos(random_angle)
        delta_lon = random_distance * math.sin(random_angle) / math.cos(math.radians(home[0]))

        new_lat = home[0] + math.degrees(delta_lat)
        new_lon = home[1] + math.degrees(delta_lon)

        if min_radius_km < haversine(home, [new_lat, new_lon]) < max_radius_km:
            return [new_lat, new_lon]
        
def generate_map(currentLocation, newLocation):
    map = folium.Map(location=currentLocation, zoom_start=15)
    folium.CircleMarker(location=currentLocation, radius=50, popup="Current location").add_to(map)
    folium.Marker(currentLocation, popup="Current location").add_to(map)
    folium.Marker(newLocation, popup="New location").add_to(map)
    folium.PolyLine(locations=[currentLocation, newLocation], line_opacity=0.6).add_to(map)
    return map._repr_html_()

# Base HTML template
base_html = """
<!DOCTYPE html>
<html>
<body>
<h1>HTML Geolocation</h1>
<p>Click the button to get your coordinates.</p>

<button onclick="getLocation()">Try It</button>

<p id="demo"></p>

<script>
const x = document.getElementById("demo");

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  x.innerHTML = "Latitude: " + position.coords.latitude + 
  "<br>Longitude: " + position.coords.longitude;
}
</script>

<form id="coordinatesForm" method="POST" action="/submit_coordinates">
    <h2>Enter Coordinates Manually</h2>
    <label for="latitudeInput">Latitude:</label>
    <input type="text" id="latitudeInput" name="latitudeInput" required>
    <br>
    <label for="longitudeInput">Longitude:</label>
    <input type="text" id="longitudeInput" name="longitudeInput" required>
    <br>
    <label for="minRadius">Minimum radius (km):</label>
    <input type="text" id="minRadius" name="minRadius" required>
    <br>
    <label for="maxRadius">Maximum radius (km):</label>
    <input type="text" id="maxRadius" name="maxRadius" required>
    <br>
    <button type="submit">Submit</button>
</form>

<div id="map-container">
    {{ map_html | safe }}
</div>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(base_html, map_html="")

@app.route('/submit_coordinates', methods=['POST'])
def submit_coordinates():
    lat = float(request.form.get('latitudeInput'))
    lon = float(request.form.get('longitudeInput'))
    min_rad = float(request.form.get('minRadius'))
    max_rad = float(request.form.get('maxRadius'))
    
    current_coords = [lat, lon]
    new_coords = generate_random_coordinate_within_annulus(current_coords, min_rad, max_rad)
    map_html = generate_map(current_coords, new_coords)
    
    return render_template_string(base_html, map_html=map_html)

if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"Server is running at http://{local_ip}:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
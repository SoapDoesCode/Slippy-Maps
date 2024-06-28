import math
import random

import folium

def haversine(coord1, coord2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371  # Radius of the Earth in kilometers
    
    # Distance in kilometers
    distance_km = r * c
    return distance_km

def generate_random_coordinate_within_annulus(home, min_radius_km, max_radius_km):
    # Radius of the Earth in kilometers
    earth_radius_km = 6371

    # Convert radius from kilometers to degrees
    min_radius_in_degrees = min_radius_km / earth_radius_km
    max_radius_in_degrees = max_radius_km / earth_radius_km

    while True:
        # Random distance and angle
        random_distance = random.uniform(min_radius_in_degrees, max_radius_in_degrees)
        random_angle = random.uniform(0, 2 * math.pi)

        # Calculate offset in latitude and longitude
        delta_lat = random_distance * math.cos(random_angle)
        delta_lon = random_distance * math.sin(random_angle) / math.cos(math.radians(home[0]))

        # Calculate new latitude and longitude
        new_lat = home[0] + math.degrees(delta_lat)
        new_lon = home[1] + math.degrees(delta_lon)

        # Ensure the new point is within the specified annulus
        if min_radius_km < haversine(home, [new_lat, new_lon]) < max_radius_km:
            return [new_lat, new_lon]
        
def generate_map(currentLocation, newLocation):
    map = folium.Map(location=Home,zoom_start=15)
    folium.CircleMarker(location=Home,radius=50,popup = "anyplace").add_to(map)
    folium.Marker(Home,popup= "Home").add_to(map)
    folium.Marker(ToAddress,popup= "New Address").add_to(map)
    folium.PolyLine(locations=[Home,ToAddress],line_opacity = 0.6).add_to(map)
    map.save("map.html")

# Coordinates
Home = [52.69057, -1.83225]

# Generate random ToAddress within 1.5 km radius but not within 0.5 km radius
ToAddress = generate_random_coordinate_within_annulus(Home, 0.5, 1.5)

# Calculate distance
distance = haversine(Home, ToAddress)

generate_map(Home, ToAddress)

print(f"Current coordinates: {Home}")
print(f"New coordinates: {ToAddress}")
print("The map between these coordinates has been generated successfully!")
print(f"The distance is {distance:.2f} kilometers")
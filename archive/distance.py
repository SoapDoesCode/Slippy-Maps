import math

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

# Coordinates
Home = [52.69057, -1.83225]
ToAddress = [52.67057, -1.83225]

# Calculate distance
distance = haversine(Home, ToAddress)
print(f"The distance is {distance} kilometers")
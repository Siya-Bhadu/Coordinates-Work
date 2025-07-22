import numpy as np
import math
from typing import List

# Earth radius in meters
EARTH_RADIUS = 6371000

# Convert degrees to radians
def deg2rad(deg):
    return deg * math.pi / 180 # Conversion formula

# Calculates the Haversine distance between two points on the Earth
# Practice using type hints (: float) and return type hints (-> float)
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float: 
    dlat: float = deg2rad(lat2 - lat1)
    dlon: float = deg2rad(lon2 - lon1)
    lat1 = deg2rad(lat1)
    lat2 = deg2rad(lat2)

    a: float = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c: float = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS * c

# Calculates the initial bearing from one point to another
def initial_bearing(lat1: float, lon1: float, lat2: float, lon2: float):
    lat1 = deg2rad(lat1)
    lat2 = deg2rad(lat2)
    dlon = deg2rad(lon2 - lon1)

    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dlon)
    return math.atan2(x, y)

# Converts geodetic coordinates (latitude, longitude) to local Cartesian coordinates (x, y)
def geodetic_to_cartesian(origin_lat: float, origin_lon: float, target_lat: float, target_lon: float):
    distance: float = haversine_distance(origin_lat, origin_lon, target_lat, target_lon)
    bearing: float = initial_bearing(origin_lat, origin_lon, target_lat, target_lon)
    x: float = distance * math.sin(bearing)
    y: float = distance * math.cos(bearing)
    return x, y

# Converts a list of coordinates (latitude, longitude) to local Cartesian coordinates
def convert_all_to_cartesian(coords: List[List[float]]) -> List[List[float]]: # coords is a list of lists, each containing latitude and longitude
    if not coords:
        return []

    origin_lat: float = coords[0][0] # Uses the first coordinate as the origin, as Aarohi said to do
    origin_lon: float = coords[0][1]

    cartesian_coords: List[List[float]] = [] # Initialize an empty list to store Cartesian coordinates

    for lat, lon in coords: # Interate through each longitude and latitude pair
        x, y = geodetic_to_cartesian(origin_lat, origin_lon, lat, lon)
        cartesian_coords.append([x, y]) # Adds to the list

    return cartesian_coords

def main() -> None:
    # Coordinate List:
    coord_list: List[List[float, float]] = [[39.033236, -94.577538], 
    [39.040763, -94.577611], 
    [39.024617, -94.577756], 
    [39.033840, -94.554732], 
    [39.033559, -94.602259], # Real Coordinates
    [39.038549, -94.562202],
    [39.033447, -94.591252],
    [39.024701, -94.591180],
    [39.025878, -94.564259]]

    cartesian_xy: List[List[float]] = convert_all_to_cartesian(coord_list)

    print("New Cartesian Coordinates:")
    for xy in cartesian_xy:
        print(f"X: {xy[0]:.2f}, Y: {xy[1]:.2f}") # Formats to two decimal points

# Run the program
if __name__ == '__main__':
    main()




















































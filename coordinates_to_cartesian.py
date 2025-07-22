import numpy as np
import math
from typing import List, Tuple

# Earth radius in meters
EARTH_RADIUS = 6371000

def deg2rad(deg: float) -> float:
    return deg * math.pi / 180 

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float: 
    """
    Calculates the Haversine distance between two points, longitude and latitude (in decimal degrees).
    
    Args: lat1 (float): Latitude of the first point.
          lon1 (float): Longitude of the first point.
          lat2 (float): Latitude of the second point.
          lon2 (float): Longitude of the second point.

    Returns:
        float: The Haversine distance in meters between the two points.
    
    """
    dlat: float = deg2rad(lat2 - lat1)
    dlon: float = deg2rad(lon2 - lon1)
    lat1 = deg2rad(lat1)
    lat2 = deg2rad(lat2)

    a: float = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c: float = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS * c


def initial_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the initial bearing (direction) from one point to another.
    Longitude and latitude are in decimal degrees.

    Args:
        lat1 (float): Latitude of the first point.
        lon1 (float): Longitude of the first point.
        lat2 (float): Latitude of the second point.
        lon2 (float): Longitude of the second point.

    Returns:
        float: The initial bearing in radians from the first point to the second point.
    
    """
    lat1 = deg2rad(lat1)
    lat2 = deg2rad(lat2)
    dlon = deg2rad(lon2 - lon1)

    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dlon)
    return math.atan2(x, y)


def geodetic_to_cartesian(origin_lat: float, origin_lon: float, target_lat: float, target_lon: float) -> Tuple[float, float]:
    """
    Converts geodetic coordinates (latitude, longitude) to Cartesian coordinates (x, y) relative to an origin point.
    Longitude and latitude are in decimal degrees.

    Args:
        origin_lat (float): Latitude of the origin point.
        origin_lon (float): Longitude of the origin point.
        target_lat (float): Latitude of the target point.
        target_lon (float): Longitude of the target point.

    Returns:
        tuple: A coordinate pair (x, y) representing the Cartesian coordinates relative to the origin point.
    
    """
    distance: float = haversine_distance(origin_lat, origin_lon, target_lat, target_lon)
    bearing: float = initial_bearing(origin_lat, origin_lon, target_lat, target_lon)
    x: float = distance * math.sin(bearing)
    y: float = distance * math.cos(bearing)
    return x, y


def convert_all_to_cartesian(coords: List[List[float]]) -> List[List[float]]: 
    """
    Converts a list of longitude/latitude coordinates to local Cartesian coordinates, using the first coordinate as the origin.
    Longitude and latitude are in decimal degrees.
    Args:
        coords (List[List[float]]): A list of lists, where each inner list contains a latitude and longitude pair.

    Returns:
        List[List[float]]: A list of Cartesian coordinates (x, y) relative to the first coordinate in the list (the origin).
    
    """
    if not coords:
        return []

    origin_lat: float = coords[0][0] 
    origin_lon: float = coords[0][1]

    cartesian_coords: List[List[float]] = [] 

    for lat, lon in coords: 
        x, y = geodetic_to_cartesian(origin_lat, origin_lon, lat, lon)
        cartesian_coords.append([x, y]) 

    return cartesian_coords

def main() -> None:
    # Coordinate List, using realistic GPS coordinates:
    coord_list: List[List[float, float]] = [[39.033236, -94.577538], 
    [39.040763, -94.577611], 
    [39.024617, -94.577756], 
    [39.033840, -94.554732], 
    [39.033559, -94.602259], 
    [39.038549, -94.562202],
    [39.033447, -94.591252],
    [39.024701, -94.591180],
    [39.025878, -94.564259]]

    cartesian_xy: List[List[float]] = convert_all_to_cartesian(coord_list)

    print("New Cartesian Coordinates:")
    for xy in cartesian_xy:
        print(f"X: {xy[0]:.2f}, Y: {xy[1]:.2f}") # Formats to two decimal points

if __name__ == '__main__':
    main()




















































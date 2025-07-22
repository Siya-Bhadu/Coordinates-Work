import numpy as np
import math 

# Earth radius in meters
EARTH_RADIUS = 6371000  

def deg2rad(deg):
    return deg * math.pi / 180

def haversine_distance(lat1, lon1, lat2, lon2):
    dlat = deg2rad(lat2 - lat1)
    dlon = deg2rad(lon2 - lon1)
    lat1 = deg2rad(lat1)
    lat2 = deg2rad(lat2)

    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS * c

def initial_bearing(lat1, lon1, lat2, lon2):
    lat1 = deg2rad(lat1)
    lat2 = deg2rad(lat2)
    dlon = deg2rad(lon2 - lon1)

    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dlon)
    return math.atan2(x, y)

def geodetic_to_local(origin_lat, origin_lon, target_lat, target_lon):
    distance = haversine_distance(origin_lat, origin_lon, target_lat, target_lon)
    bearing = initial_bearing(origin_lat, origin_lon, target_lat, target_lon)
    x = distance * math.sin(bearing)
    y = distance * math.cos(bearing)
    return x, y



def main():
    # Extract GPS data
    latitudes = df['latitude']
    longitudes = df['longitude']

    # Use the first point as origin
    origin_lat:float = latitudes.iloc[0]
    origin_lon = longitudes.iloc[0]
    local_waypoint_x, local_waypoint_y = geodetic_to_local(origin_lat, origin_lon, 38.6962666, -94.2580533)


    # Compute local x/y using Haversine
    local_x = []
    local_y = []


    for lat, lon in zip(latitudes, longitudes):
        x_local, y_local = geodetic_to_local(origin_lat, origin_lon, lat, lon)
        local_x.append(x_local)
        local_y.append(y_local)

    # Replace or add local x/y columns
    df['x_local'] = local_x
    df['y_local'] = local_y


    x = df['x_local']
    y = df['y_local']



if __name__ == '__main__':
    main()


# Look over Aarohi's GitHub Repositories
# Download ArduPilot -> DONE
# Install Docker
# Docker & ROS2 Slides Review + Research Additional Information
# Code above is converting Waypoints set in Coordinates (Longitude, Latitude)  -> Cartesian (x, y)
# Goal is explained below

'''
The above code already does lat long (coordinates) to x,y (cartesian) so alter the body and the functions to work with the lists
The functions only work with 1 origin and 1 target lat and long
Change it to work with an inputted list, don't forget to type hint each variable (int, float, str, etc.)

say your function takes in a list of lists: [[20,30], [60,70], [100,100]]
you want to return a list of lists that is in lat and long

Example Aarohi Gave for Hard Coding a list of (real world) coordinates (cartesian for inverse): 

from typing import List, Any, Dict

def main() -> None: 
    print("Hello World")   
    coord_list:List[List[float, float]] = [[1.345566,45.67464], [54.656546, 65.35474747]]

if __name__ == '__main__':
    main()


Other:


def main() -> None:
    # Pre-defined list of [latitude, longitude]
    gps_coordinates: List[List[float]] = [
        [38.6956965, -94.2573627],  # Origin
        [38.6962666, -94.2580533],
        [38.6967000, -94.2590000]
    ]

    local_xy: List[List[float]] = convert_all_to_local(gps_coordinates)

    print("Local X/Y Coordinates:")
    for xy in local_xy:
        print(f"X: {xy[0]:.2f}, Y: {xy[1]:.2f}")

if __name__ == '__main__':
    main()



'''
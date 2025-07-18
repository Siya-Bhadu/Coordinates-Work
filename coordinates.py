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
    
    df = pd.read_csv("apmuas_data/global_data.csv")

    # Extract GPS data
    latitudes = df['latitude']
    longitudes = df['longitude']

    # Use the first point as origin
    origin_lat = latitudes.iloc[0]
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


    plt.figure(figsize=(10, 10))
    plt.plot(df['x_local'], df['y_local'], marker='o', linestyle='-', color='blue', label='Trajectory')
    #plt.plot(local_waypoint_x, local_waypoint_y, 'ro', markersize=8, label='Waypoint')
    plt.title("Drone Trajectory in Local Coordinates")
    plt.xlabel("East (meters)")
    plt.ylabel("North (meters)")
    plt.legend()
    plt.axis('equal')  # Preserve aspect ratio so scale is correct
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()


import os
import sys
import random

import pyproj

# these imports are required for SUMO
if 'SUMO_HOME' in os.environ:
    sumo_tools_directory = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(sumo_tools_directory)
else:
    raise ModuleNotFoundError("You must declare the environmental variable 'SUMO_HOME' to load the necessary packages.")
import traci
import sumolib


def get_response_times(station_coordinates, num_simulations=10):
    """This function will run multiple simulations in SUMO and return the resulting response times."""

    response_times = []
    for _ in range(num_simulations):
        start_simulation()
        response_times.append(respond_to_emergency(station_coordinates))
        close_simulation()

    return response_times


def start_simulation(gui=False, auto_start_close=True):
    """Starts a simulation in SUMO."""

    # this absolute file path must point to where SUMO is installed, there is no way around this
    if gui:
        sumo_file_path = r"C:\Program Files (x86)\Eclipse\Sumo\bin\sumo-gui.exe"
    else:
        sumo_file_path = r"C:\Program Files (x86)\Eclipse\Sumo\bin\sumo.exe"

    # construct the sumo command
    config_file_path = r"D:\burlington.sumocfg"
    sumo_command = [sumo_file_path, "-c", config_file_path]
    if auto_start_close:
        sumo_command.append('--start')
        sumo_command.append('--quit-on-end')

    # call the command to start the simulation
    traci.start(sumo_command)


def respond_to_emergency(station_coordinates):
    """
    This function creates an emergency, finds the nearest station, and sends the emergency vehicle.
    It returns the amount of time (in seconds) it takes for the emergency vehicle to arrive on scene.
    """

    # find the edges of the source and destination
    emergency_edge, emergency_lat, emergency_lon = get_emergency()
    station_coordinate = get_closest_station(station_coordinates, (emergency_lat, emergency_lon))
    station_edge = get_edge_id_from_gps(station_coordinate)

    # create the emergency vehicle and send it from the source to the destination
    traci.route.add("trip", [station_edge, emergency_edge])
    traci.vehicle.add("fire_truck", "trip")
    traci.vehicle.setVehicleClass("fire_truck", "emergency")
    traci.vehicle.setColor("fire_truck", (255, 0, 0, 255))

    # track how long the emergency vehicle takes to arrive on scene
    while 'fire_truck' not in traci.simulation.getArrivedIDList():
        traci.simulationStep()
    arrival_time = traci.simulation.getTime()

    return arrival_time


def close_simulation():
    """Closes the simulation in SUMO."""

    traci.close()


def get_emergency():
    net_file_path = r"sumo\osm.net.xml"
    net = sumolib.net.readNet(net_file_path)

    # find a valid edge for emergency vehicle
    edge = None
    while not edge:
        edge_ID = random.choice(traci.edge.getIDList())
        if net.hasEdge(edge_ID):
            edge = net.getEdge(edge_ID)
            if not edge.allows("emergency"):
                edge = None

    edge = net.getEdge(edge_ID)
    x, y, _, _ = edge.getBoundingBox()
    lon, lat = net.convertXY2LonLat(x, y)

    return edge_ID, lat, lon


def get_edge_id_from_gps(coordinate, search_radius=100):
    """Returns the nearest edge to the passed coordinates that the emergency vehicle can depart from."""

    # get a list of nearby edges
    net_file_path = r"sumo\osm.net.xml"
    latitude, longitude = coordinate
    net = sumolib.net.readNet(net_file_path)
    x, y = net.convertLonLat2XY(longitude, latitude)
    edges = net.getNeighboringEdges(x, y, search_radius)

    # return the closest allowed edge ID
    edges = sorted(edges, key=lambda x: x[1])
    for edge in edges:
        if edge[0].allows("emergency"):
            return edge[0].getID()

    raise ValueError(f"No edges within search radius:{search_radius} of coordinate:{coordinate} was found.")


def get_distance(coordinates_1, coordinates_2):
    """Returns the distance between two GPS coordinates."""

    geo_dist = pyproj.Geod(ellps='WGS84')
    lat_1, lon_1 = coordinates_1
    lat_2, lon_2 = coordinates_2

    return geo_dist.inv(lon_1, lat_1, lon_2, lat_2)[2]


def get_closest_station(station_coordinates, emergency_coordinate):
    """
    First argument is a list of station coordinates where each coordinate is a tuple of (lat, lon).
    Second argument is tuple of (lat, lon) of emergency location.
    Returns a tuple containing the lat and lon of the fire station nearest to the coordinates.
    """

    distances = [get_distance(s_c, emergency_coordinate) for s_c in station_coordinates]
    min_index = distances.index(min(distances))

    return station_coordinates[min_index]


def main():

    station_coordinates = [(44.485567, -73.222804), (44.476561, -73.210535), (44.466561, -73.210535), (44.478, -73.213), (44.476, -73.205)]
    # station_coordinates = [(44.476561, -73.210535)]
    response_times = get_response_times(station_coordinates)
    # print(f"Response time was {response_time} seconds")

    print(response_times)
    print(sum(response_times) / len(response_times))


main()

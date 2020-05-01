"""This file provides functionality for interacting with the Simulation of Urban Mobility."""

import os
import sys
import random

import pyproj
# these imports are required for SUMO
if 'SUMO_HOME' in os.environ:
    sumo_tools_directory = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(sumo_tools_directory)
else:
    raise ModuleNotFoundError("Install SUMO and the environmental variable 'SUMO_HOME' will be automatically set.")
import traci
import sumolib

from file_paths import get_simulation_data_file_path


def get_response_times(data_directory,
                       station_coordinates,
                       num_simulations=10,
                       gui=False,
                       auto_start_close=False):
    """This function will run multiple simulations in SUMO and return the resulting response times."""

    response_times = []
    config_file_path = get_config_file_path(data_directory)
    net_file_path = get_network_file_path(data_directory)

    for _ in range(num_simulations):
        start_simulation(config_file_path, gui, auto_start_close)
        response_times.append(respond_to_emergency(net_file_path, station_coordinates))
        close_simulation()

    return response_times


def start_simulation(config_file_path, gui=False, auto_start_close=True):
    """Starts a simulation in SUMO."""

    # find the SUMO file path
    if gui:
        sumo_executable = 'sumo-gui.exe'
    else:
        sumo_executable = 'sumo.exe'
    sumo_file_path = os.path.join(os.environ['SUMO_HOME'], 'bin', sumo_executable)

    # construct the sumo command
    sumo_command = [sumo_file_path, "-c", config_file_path]
    if auto_start_close:
        sumo_command.append('--start')
        sumo_command.append('--quit-on-end')

    # call the command to start the simulation
    traci.start(sumo_command)


def respond_to_emergency(net_file_path, station_coordinates, prior_time=400):
    """
    This function creates an emergency, finds the nearest station, and sends the emergency vehicle.
    It returns the amount of time (in seconds) it takes for the emergency vehicle to arrive on scene.
    """

    # find the edges of the source and destination
    emergency_edge, emergency_lat, emergency_lon = get_emergency(net_file_path)
    station_coordinate = get_closest_station(station_coordinates, (emergency_lat, emergency_lon))
    station_edge = get_edge_id_from_gps(net_file_path, station_coordinate)

    # run the simulation a little to allow traffic to flow
    while traci.simulation.getTime() < prior_time:
        traci.simulationStep()

    # create the emergency vehicle and send it from the source to the destination
    traci.route.add("trip", [station_edge, emergency_edge])
    traci.vehicle.add("fire_truck", "trip")
    traci.vehicle.setVehicleClass("fire_truck", "emergency")
    traci.vehicle.setSpeedFactor("fire_truck", 1.5)
    traci.vehicle.setSpeedMode("fire_truck", 0)
    traci.vehicle.setColor("fire_truck", (255, 0, 0, 255))
    traci.vehicle.setShapeClass("fire_truck", "truck")

    # track how long the emergency vehicle takes to arrive on scene
    while 'fire_truck' not in traci.simulation.getArrivedIDList():
        traci.simulationStep()

    # compute the response time
    preparation_time = 75
    travel_time = traci.simulation.getTime() - prior_time
    response_time = preparation_time + travel_time

    return response_time


def close_simulation():
    """Closes the simulation in SUMO."""

    traci.close()


def get_emergency(network_file_path):
    """Returns the edgeID and GPS coordinates of an emergency."""

    net = get_network(network_file_path)

    # find a valid edge for emergency vehicle
    edge = None
    while not edge:
        edge = random.choice(net.getEdges())
        if not edge.allows("emergency"):
            edge = None

    # get the ID, lat, and lon
    edge_ID = edge.getID()
    lon, lat = net.convertXY2LonLat(*edge.getToNode().getCoord())

    return edge_ID, lat, lon


def get_edge_id_from_gps(network_file_path, coordinate, search_radius=1000):
    """Returns the nearest edge to the passed coordinates that the emergency vehicle can depart from."""

    # get a list of nearby edges
    latitude, longitude = coordinate
    net = get_network(network_file_path)
    x, y = net.convertLonLat2XY(longitude, latitude)
    edges = net.getNeighboringEdges(x, y, search_radius)

    # return the closest allowed edge ID
    edges = sorted(edges, key=lambda x: x[1])
    for edge in edges:
        if edge[0].allows("emergency"):
            return edge[0].getID()

    raise ValueError(f"Found no edges within search radius {search_radius} of coordinate {coordinate} that support "
                     f"emergency vehicles."
                     f"\nCheck to make sure your coordinates are reasonable "
                     f"and consider increasing the search radius.")


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


def get_network_coordinate_bounds(network_file_path):
    """
    Returns a tuple containing two coordinates where each coordinate is a (lat, lon) representing the bounds of the
    network.
    """

    net = get_network(network_file_path)
    coordinate_1 = net.convertXY2LonLat(*net.getBBoxXY()[0])
    coordinate_2 = net.convertXY2LonLat(*net.getBBoxXY()[1])

    return (coordinate_1[1], coordinate_1[0]), (coordinate_2[1], coordinate_2[0])


def get_network(network_file_path):
    """Loads and returns the network object from the passed file path."""

    return sumolib.net.readNet(network_file_path)


def get_config_file_path(data_directory):
    """Returns the file path to the SUMO configuration file."""

    return os.path.join(data_directory, 'osm.sumocfg')


def get_network_file_path(data_directory):
    """Returns the file path to the file encoding the road network."""

    return os.path.join(data_directory, 'osm.net.xml')


def main():
    """Runs a small sample network with theoretical department locations for experimentation."""

    data_directory = get_simulation_data_file_path('test_sim')
    station_coordinates = [(44.485567, -73.222804),
                           (44.476561, -73.210535),
                           (44.466561, -73.210535),
                           (44.478, -73.213),
                           (44.476, -73.205)]

    response_times = get_response_times(data_directory, station_coordinates)
    print(f"Response times were: {response_times} seconds.")


if __name__ == "__main__":
    main()

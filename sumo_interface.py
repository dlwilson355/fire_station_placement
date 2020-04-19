import os
import sys
import random

# these imports are required for SUMO
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
import traci
import sumolib
import traci.constants as tc


def create_simulation(config_file_path, gui=False, auto_start=True):

    if gui:
        sumo_file_path = r"C:\Program Files (x86)\Eclipse\Sumo\bin\sumo-gui.exe"
    else:
        sumo_file_path = r"C:\Program Files (x86)\Eclipse\Sumo\bin\sumo.exe"

    sumo_command = [sumo_file_path, "-c", config_file_path]
    if auto_start:
        sumo_command.append('--start')

    traci.start(sumo_command)


def get_edge_id_from_gps(latitude, longitude, search_radius=100):
    """TODO: find closest"""

    net_file_path = r"C:\Users\Daniel\OneDrive\Documents\School Work\Data Science 2\HW\Final Project\2020-04-18-18-20-43\osm.net.xml"
    net = sumolib.net.readNet(net_file_path)
    x, y = net.convertLonLat2XY(longitude, latitude)
    edges = net.getNeighboringEdges(x, y, search_radius)

    return edges[0][0].getID()


def main():
    # config_file_1 = r"C:\Program Files (x86)\Eclipse\Sumo\test.sumocfg"
    # create_simulation(config_file_1, gui=False)
    # print(traci.edge.getIDList())
    # traci.route.add("trip", ['gneE0', 'gneE1'])
    # traci.vehicle.add("newVeh", "trip")
    # traci.vehicle.getVehicleClass("newVeh")
    # traci.vehicle.setVehicleClass("newVeh", "emergency")

    config_file_2 = r"D:\burlington.sumocfg"
    create_simulation(config_file_2, gui=True, auto_start=False)
    # print(traci.edge.getIDList())

    fire_department = get_edge_id_from_gps(44.476561, -73.210535)
    # destination = get_edge_id_from_gps(44.483553, -73.209826, search_radius=1000)
    destination = get_edge_id_from_gps(44.473297, -73.208789)

    traci.route.add("trip", [fire_department, destination])
    traci.vehicle.add("fire_truck", "trip")
    traci.vehicle.setVehicleClass("fire_truck", "emergency")
    traci.vehicle.setColor("fire_truck", (255, 0, 0, 255))

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if 'fire_truck' in traci.simulation.getArrivedIDList():
            print(f"Arrived at: {traci.simulation.getTime()}")
        # print(traci.simulation.getTime())

    traci.close()


main()

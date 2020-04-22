import pandas as pd
import os

from sumo_interface import get_response_times


def load_station_coordinates():
    """This function returns """

    stations = pd.read_csv(os.path.join("data", "FDNY_Firehouse_Listing.csv"))
    station_coordinates = []
    for i in range(stations.shape[0]):
        latitude = stations['Latitude'].iloc[i]
        longitude = stations['Longitude'].iloc[i]
        station_coordinates.append((latitude, longitude))

    return station_coordinates


def simulate():
    directory = "staten_island_south_west"
    config_file_path = os.path.join(directory, "osm.sumocfg")
    net_file_path = os.path.join(directory, "osm.net.xml")
    station_coordinates = load_station_coordinates()
    response_times = get_response_times(config_file_path, net_file_path, station_coordinates, gui=True)
    print(response_times)
    print(sum(response_times) / len(response_times))


if __name__ == "__main__":
    simulate()
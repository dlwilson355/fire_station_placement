import os

import pandas as pd
import matplotlib.pyplot as plt

from sumo_interface import get_response_times
from exploratory_data_analysis import compute_summary_statistics, get_ECDF_values, load_nyc_response_time_dataset, \
    create_output_directory


def load_nyc_station_coordinates():
    """This function returns the coordinates of the New York fire stations as a list of (lat, lon) tuples."""

    stations = pd.read_csv(os.path.join("data", "FDNY_Firehouse_Listing.csv"))
    station_coordinates = []
    for i in range(stations.shape[0]):
        latitude = stations['Latitude'].iloc[i]
        longitude = stations['Longitude'].iloc[i]
        station_coordinates.append((latitude, longitude))

    return station_coordinates


def get_simulated_response_times(num_simulations=10):
    directory = "staten_island_south_west"
    station_coordinates = load_nyc_station_coordinates()
    simulated_response_times = get_response_times(directory, station_coordinates, num_simulations)

    return simulated_response_times


def analyze_relationship(real_response_times, simulated_response_times):
    """
    Constructs an ECDF and computes summary statistics analyzing the relationship between real and simulated response
    times.
    """

    create_output_directory()

    # construct an ECDF
    plt.style.use('Solarize_Light2')
    font = {'weight': 'bold', 'size': 22}
    plt.rc('font', **font)
    plt.plot(*get_ECDF_values(real_response_times))
    plt.plot(*get_ECDF_values(simulated_response_times), '--')
    plt.xlabel("Response Time (s)")
    plt.ylabel("Pr < X")
    plt.title("Real vs Simulated Response Times")
    plt.legend(["Real", "Simulated"])
    plt.savefig(os.path.join("plots", "real_vs_simulated_response_times_ecdf.png"))

    # compute summary statistics
    data_dict = {"Real": real_response_times, "Simulated": simulated_response_times}
    compute_summary_statistics(data_dict, os.path.join("plots", "real_vs_simulated_response_times.txt"))


def main():
    real_response_times = list(load_nyc_response_time_dataset()["AVERAGERESPONSETIME"])
    simulated_response_times = get_response_times("staten_island_south_west", load_nyc_station_coordinates(), 5)
    analyze_relationship(real_response_times, simulated_response_times)


if __name__ == "__main__":
    main()

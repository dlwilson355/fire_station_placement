"""This file contains code for measuring simulated response times and comparing them to actual response times."""

import pandas as pd
import matplotlib.pyplot as plt

from file_paths import get_police_data_file_path, get_simulation_data_file_path, \
    get_output_file_path, create_output_directory
from sumo_interface import get_response_times
from exploratory_data_analysis import compute_summary_statistics, get_ECDF_values, load_nyc_response_time_dataset


def load_nyc_station_coordinates():
    """This function returns the coordinates of the New York fire stations as a list of (lat, lon) tuples."""

    stations = pd.read_csv(get_police_data_file_path("FDNY_Firehouse_Listing.csv"))
    station_coordinates = []
    for i in range(stations.shape[0]):
        latitude = stations['Latitude'].iloc[i]
        longitude = stations['Longitude'].iloc[i]
        station_coordinates.append((latitude, longitude))

    return station_coordinates


def analyze_relationship(real_response_times, simulated_response_times):
    """
    Constructs an ECDF and computes summary statistics analyzing the relationship between real and simulated response
    times.
    """

    create_output_directory()

    # construct an ECDF
    fig, _ = plt.subplots(figsize=(15, 8))
    plt.style.use('Solarize_Light2')
    plt.plot(*get_ECDF_values(real_response_times))
    plt.plot(*get_ECDF_values(simulated_response_times), '--')
    plt.xlabel("Response Time (s)", fontsize=22)
    plt.ylabel("Pr < X", fontsize=22)
    plt.title("Real vs Simulated Response Times", fontsize=30)
    plt.legend(["Real", "Simulated"], fontsize=22)
    plt.savefig(get_output_file_path("real_vs_simulated_response_times_ecdf.png"))

    # compute summary statistics
    data_dict = {"Real": real_response_times, "Simulated": simulated_response_times}
    compute_summary_statistics(data_dict, get_output_file_path("real_vs_simulated_response_times.txt"))


def main():
    real_response_times = list(load_nyc_response_time_dataset()["AVERAGERESPONSETIME"])
    simulated_response_times = get_response_times(get_simulation_data_file_path("staten_island_south_west"),
                                                  load_nyc_station_coordinates(), 500)
    analyze_relationship(real_response_times, simulated_response_times)


if __name__ == "__main__":
    main()

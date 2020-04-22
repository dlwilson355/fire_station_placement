import os

import pandas as pd
import matplotlib.pyplot as plt

from sumo_interface import get_response_times
from exploratory_data_analysis import print_summary_statistics, construct_ecdf, get_seconds
from optimization import load_station_coordinates


def get_real_world_response_times():
    data = pd.read_csv(os.path.join("data", "FDNY_Monthly_Response_Times.csv"))
    data["AVERAGERESPONSETIME"] = data["AVERAGERESPONSETIME"].apply(get_seconds)

    return data["AVERAGERESPONSETIME"]


def get_simulated_response_times(num_simulations=10):
    directory = "staten_island_south_west"
    config_file_path = os.path.join(directory, "osm.sumocfg")
    net_file_path = os.path.join(directory, "osm.net.xml")
    station_coordinates = load_station_coordinates()
    simulated_response_times = get_response_times(config_file_path, net_file_path, station_coordinates, num_simulations)

    return simulated_response_times


def ecdf(real_response_times, simulated_response_times):

    real_response_times = sorted(real_response_times)
    simulated_response_times = sorted(simulated_response_times)

    l_r = len(real_response_times)
    l_s = len(simulated_response_times)

    p_r = [i / l_r for i in range(l_r)]
    p_s = [i / l_s for i in range(l_s)]

    plt.plot(real_response_times, p_r)
    plt.plot(simulated_response_times, p_s, '--')
    plt.xlabel("Response Time (s)")
    plt.ylabel("Pr < X")
    plt.title("Real vs Simulated Response Times")
    plt.legend(["Real", "Simulated"])
    plt.show()


def analyze_relationship(real_response_times, simulated_response_times):

    print("Summary Statistics for real response times")
    print_summary_statistics(real_response_times)
    print("Summary Statistics for simulated response times")
    print_summary_statistics(simulated_response_times)

    plt.style.use('Solarize_Light2')
    font = {'family': 'normal',
            'weight': 'bold',
            'size': 22}
    plt.rc('font', **font)

    ecdf(real_response_times, simulated_response_times)


def main():
    real_response_times = list(get_real_world_response_times())
    simulated_response_times = get_simulated_response_times(500)
    print(real_response_times)
    print(simulated_response_times)
    # simulated_response_times = get_real_world_response_times()[10:20]
    # print(real_response_times)
    # print(simulated_response_times)
    analyze_relationship(real_response_times, simulated_response_times)


if __name__ == "__main__":
    main()
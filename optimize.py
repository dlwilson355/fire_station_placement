"""This file contains code for optimizing the placement of fire stations."""

import matplotlib.pyplot as plt

from optimization_algorithms import HillClimberOptimizationAlgorithm
from sumo_interface import get_network_coordinate_bounds, get_network_file_path
from file_paths import get_simulation_data_file_path
from loss_functions import get_average_response_loss, \
    get_median_response_loss, get_max_95_percentile_response_loss, get_max_loss


def run_algorithm():
    directory = get_simulation_data_file_path('test_sim')
    loss_function = get_max_loss(directory, 3)
    bounds = get_network_coordinate_bounds(get_network_file_path(directory))
    algorithm = HillClimberOptimizationAlgorithm(loss_function, 3, bounds, 1, 0.1)

    fitness_values = [algorithm.fitness]
    for _ in range(6):
        fitness_values.append(algorithm.update_placements())

    plt.plot(fitness_values)
    plt.show()


if __name__ == "__main__":
    run_algorithm()

"""This file contains code for optimizing the placement of fire stations."""

import matplotlib.pyplot as plt

from optimization_algorithms import HillClimberOptimizationAlgorithm
from sumo_interface import get_response_times, get_network_coordinate_bounds, get_network_file_path


def average_response_loss(simulation_directory, station_placements, num_simulations=100):
    """This loss function returns the mean response time over a specified number of simulated emergencies."""

    response_times = get_response_times(simulation_directory, station_placements, num_simulations)
    mean_response_time = sum(response_times) / len(response_times)

    return mean_response_time


def run_algorithm():
    directory = 'test_sim'
    loss_function = lambda placements: average_response_loss(directory, placements, 3)
    bounds = get_network_coordinate_bounds(get_network_file_path(directory))
    algorithm = HillClimberOptimizationAlgorithm(loss_function, 3, bounds, 1, 0.1, seed=1)

    fitnesses = [algorithm.fitness]
    for _ in range(6):
        fitnesses.append(algorithm.update_placements())

    plt.plot(fitnesses)
    plt.show()


if __name__ == "__main__":
    run_algorithm()

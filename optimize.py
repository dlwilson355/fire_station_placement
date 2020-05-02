"""This file contains code for optimizing the placement of fire stations."""

import matplotlib.pyplot as plt

from optimization_algorithms import HillClimberOptimizationAlgorithm
from sumo_interface import get_network_coordinate_bounds, get_network_file_path
from file_paths import get_simulation_data_file_path
from loss_functions import get_average_response_loss, \
    get_median_response_loss, get_max_95_percentile_response_loss, get_max_loss


def construct_fitness_plot(fitness_values, parameters, title="Fitness Plot"):
    """Makes a plot of the fitness scores achieved at each time step for each value of the algorithm parameter."""

    pass


def run_algorithm(algorithm, num_generations=10):
    """Runs the passed optimization algorithm and returns its fitness scores."""

    fitness_values = [algorithm.fitness]
    for _ in range(num_generations):
        fitness_values.append(algorithm.update_placements())

    return fitness_values


def run_experiment():
    """
    Runs an the optimization algorithm for different parameter values,
    records the fitness values,
    and plots the results.
    """

    directory = get_simulation_data_file_path('test_sim')
    station_bounds = get_network_coordinate_bounds(get_network_file_path(directory))
    num_stations = 3
    num_simulations = 2
    loss_functions = [get_average_response_loss(directory, num_simulations),
                      get_median_response_loss(directory, num_simulations),
                      get_max_95_percentile_response_loss(directory, num_simulations),
                      get_max_loss(directory, num_simulations)]
    mutation_distances = [0.001, 0.01, 0.1, 1]

    algorithm = HillClimberOptimizationAlgorithm(loss_functions[0], num_stations, station_bounds, 1, mutation_distances[0], seed=0)
    fitness_values = run_algorithm(algorithm)

    plt.plot(fitness_values)
    plt.show()


if __name__ == "__main__":
    run_experiment()

"""This file contains code for optimizing the placement of fire stations."""

import matplotlib.pyplot as plt

from optimization_algorithms import HillClimberOptimizationAlgorithm
from sumo_interface import get_network_coordinate_bounds, get_network_file_path
from file_paths import get_simulation_data_file_path, get_output_file_path, create_output_directory
from loss_functions import get_mean_response_loss, \
    get_median_response_loss, get_max_95_percentile_response_loss, get_max_loss


def construct_fitness_plot(fitness_values, parameters, loss_function_names, title="Fitness Plot"):
    """Makes a plot of the fitness scores achieved at each time step for each value of the algorithm parameter."""

    create_output_directory()
    fig, axs = plt.subplots(2, 2, figsize=(30, 30))

    for ax, loss_fitness, loss_function_name in zip(axs.reshape(-1), fitness_values, loss_function_names):
        for fitness_scores in loss_fitness:
            ax.plot(fitness_scores, linewidth=4)
        ax.tick_params(labelsize=22)
        ax.set_xlabel("Generation", fontsize=30)
        ax.set_ylabel("Fitness", fontsize=30)
        ax.legend(parameters, prop={"size": 40})
        ax.set_title(f"{loss_function_name}", fontsize=40)

    fig.suptitle(title, fontsize=50)
    plt.savefig(get_output_file_path(f"{title}.png"))


def run_algorithm(algorithm, num_generations=10):
    """Runs the passed optimization algorithm and returns its fitness scores."""

    fitness_values = [algorithm.fitness]
    for _ in range(num_generations):
        fitness_values.append(algorithm.update_placements())

    return fitness_values


def run_algorithm_experiments(algorithm, parameters):
    """Runs a series of experiments on the algorithm with each of the parameters and plots the results."""

    pass


def run_experiment():
    """
    Runs an the optimization algorithm for different parameter values,
    records the fitness values,
    and plots the results.
    """

    directory = get_simulation_data_file_path('test_sim')
    station_bounds = get_network_coordinate_bounds(get_network_file_path(directory))
    num_stations = 3
    num_simulations = 5
    loss_functions = [get_mean_response_loss(directory, num_simulations),
                      get_median_response_loss(directory, num_simulations),
                      get_max_95_percentile_response_loss(directory, num_simulations),
                      get_max_loss(directory, num_simulations)]
    # loss_functions = [get_mean_response_loss(directory, num_simulations)]
    loss_function_names = ["Mean Response Time",
                           "Median Response Time",
                           "Max 95th Percentile Response Time",
                           "Max Response Time"]
    algorithm_name = "Hill Climber Optimization"
    mutation_distances = [0.001, 0.01, 0.1, 1]
    # mutation_distances = [0.01]

    all_fitness_values = []  # a list of lists of each fitness from each loss function
    for loss_function in loss_functions:
        loss_fitness_values = []  # a list of fitness scores from the particular loss function
        for mutation_distance in mutation_distances:
            algorithm = HillClimberOptimizationAlgorithm(loss_function,
                                                         num_stations,
                                                         station_bounds,
                                                         1,
                                                         mutation_distance,
                                                         seed=0)
            loss_fitness_values.append(run_algorithm(algorithm, num_generations=10))
        all_fitness_values.append(loss_fitness_values)

    construct_fitness_plot(all_fitness_values,
                           mutation_distances,
                           loss_function_names,
                           algorithm_name)


if __name__ == "__main__":
    run_experiment()

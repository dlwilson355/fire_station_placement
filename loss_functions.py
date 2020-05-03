"""
This file contains the loss functions.
Each loss function takes the station coordinates as input.
Each function provides a loss value as output.
"""

import numpy as np

from sumo_interface import get_response_times


def get_mean_response_loss(simulation_directory, num_simulations=100):
    """Returns a loss function that computes the mean response time over a specified number of simulated emergencies."""

    def mean_response_loss(placements):
        response_times = get_response_times(simulation_directory,
                                            placements,
                                            num_simulations,
                                            prior_time=100,
                                            max_time=1000)
        mean_response_time = sum(response_times) / len(response_times)
        return mean_response_time

    return mean_response_loss


def get_median_response_loss(simulation_directory, num_simulations=100):
    """Returns a loss function that computes the median response time to the simulated emergencies."""

    def median_loss(placements):
        response_times = get_response_times(simulation_directory,
                                            placements,
                                            num_simulations,
                                            prior_time=100,
                                            max_time=1000)
        response_times = np.array(response_times)
        median = np.median(response_times)
        return median

    return median_loss


def get_max_95_percentile_response_loss(simulation_directory, num_simulations=100):
    """Returns a loss function that computes the max 95th percentile response time to the simulated emergencies."""

    def max_95_percentile_response_loss(placements):
        response_times = get_response_times(simulation_directory,
                                            placements,
                                            num_simulations,
                                            prior_time=100,
                                            max_time=1000)
        response_times = np.array(response_times)
        max_95_percentile = np.percentile(response_times, 95)
        return max_95_percentile

    return max_95_percentile_response_loss


def get_max_loss(simulation_directory, num_simulations=100):
    """Returns a loss function that computes the maximum response time to the simulated emergencies."""

    def max_loss(placements):
        response_times = get_response_times(simulation_directory,
                                            placements,
                                            num_simulations,
                                            prior_time=100,
                                            max_time=1000)
        max_response_time = max(response_times)
        return max_response_time

    return max_loss

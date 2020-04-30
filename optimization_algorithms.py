"""This file contains the implementation of the optimization algorithms."""

import random


class OptimizationAlgorithm:
    """This is a template optimization object which the optimization algorithms inherit."""

    def __init__(self, loss_function, num_stations, station_bounds):
        self.loss_function = loss_function
        self.num_stations = num_stations
        self.station_bounds = station_bounds
        self.fitness = 0
        self.station_placements = []
        self.initialize()

    def initialize(self):
        raise NotImplementedError("Implement this function in the optimization algorithm.")

    def update(self):
        raise NotImplementedError("Implement this function in the optimization algorithm.")

    def get_loss(self):
        return self.loss_function(self.station_placements)

    def get_random_station_location(self):
        """This function returns a random tuple of (lat, lon) within the bounds."""

        latitude = random.uniform(self.station_bounds[0][0], self.station_bounds[1][0])
        longitude = random.uniform(self.station_bounds[0][1], self.station_bounds[1][1])

        return latitude, longitude


class DistanceGeometricAlgorithm(OptimizationAlgorithm):

    pass


class CoverageGeometricAlgorithm(OptimizationAlgorithm):

    pass


class HillClimberOptimizationAlgorithm(OptimizationAlgorithm):

    def initialize(self):
        """This function makes initial station placements and computes initial fitness."""

        # place the stations randomly
        for _ in range(self.num_stations):
            self.station_placements.append(self.get_random_station_location())

        # find the fitness
        self.fitness = self.get_loss()

    def get_mutated_placements(self, max_shift_proportion=0.1):

        # determine how far each station can move
        max_lat_shift = (self.station_bounds[1][0] - self.station_bounds[0][0]) * max_shift_proportion
        max_lon_shift = (self.station_bounds[1][1] - self.station_bounds[0][1]) * max_shift_proportion

        # construct a list of mutated station placements
        mutated_station_placements = []
        for placement in self.station_placements:
            lat_shift = random.uniform(0, max_lat_shift)
            lon_shift = random.uniform(0, max_lon_shift)
            new_placement = (placement[0] + lat_shift, placement[1] + lon_shift)
            mutated_station_placements.append(new_placement)

        return mutated_station_placements

    def update(self):
        """
        Calling this function runs the next iteration of the hill climber optimization algorithm.
        Returns the improvement in fitness over the previous iteration (if any).
        """

        # find new station coordinates and evaluate their fitness
        new_placements = self.get_mutated_placements()
        new_fitness = self.loss_function(new_placements)

        # replace the current station coordinates if the new ones have greater fitness
        fitness_improvement = self.fitness - new_fitness if self.fitness > new_fitness else 0
        if fitness_improvement > 0:
            self.station_placements = new_placements
            self.fitness = new_fitness

        return fitness_improvement


class EvolutionaryOptimizationAlgorithm(OptimizationAlgorithm):

    pass

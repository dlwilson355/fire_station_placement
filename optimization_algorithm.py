"""This file contains the implementation of the optimization algorithms."""

import random


class OptimizationAlgorithm:

    def __init__(self, loss_function, num_stations, station_bounds):
        self.loss_function = loss_function
        self.num_stations = num_stations
        self.station_bounds = station_bounds
        self.station_placements = []
        self.initialize_station_placements()

    def initialize_station_placements(self):
        for _ in range(self.num_stations):
            latitude = random.uniform(self.station_bounds[0][0], self.station_bounds[1][0])
            longitude = random.uniform(self.station_bounds[0][1], self.station_bounds[1][1])
            self.station_placements.append((latitude, longitude))

    def update_station_placement(self):
        pass

    def get_loss(self):
        return self.loss_function(self.station_placements)


class DistanceGeometricAlgorithm(OptimizationAlgorithm):

    pass


class CoverageGeometricAlgorithm(OptimizationAlgorithm):

    pass


class HillClimberOptimizationAlgorithm(OptimizationAlgorithm):

    pass


class EvolutionaryOptimizationAlgorithm(OptimizationAlgorithm):

    pass

"""This file contains the implementation of the optimization algorithms."""

"""
Ideas: use force based algorithm (like for graphs with nodes)
Use goemetric optimization
Use coverage optimization
"""

import random


class OptimizationAlgorithm:
    """This is a template optimization object which the optimization algorithms inherit."""

    def __init__(self,
                 loss_function,
                 num_stations,
                 station_bounds,
                 seed=None):

        if seed:
            random.seed(seed)
        self.loss_function = loss_function
        self.num_stations = num_stations
        self.station_bounds = station_bounds
        self.fitness = 0
        self.station_placements = []
        self.initialize_placements()

    def initialize_placements(self):
        raise NotImplementedError("Implement this function in the optimization algorithm.")

    def update_placements(self):
        raise NotImplementedError("Implement this function in the optimization algorithm.")

    def get_random_station_location(self):
        """This function returns a random tuple of (lat, lon) within the bounds."""

        latitude = random.uniform(self.station_bounds[0][0], self.station_bounds[1][0])
        longitude = random.uniform(self.station_bounds[0][1], self.station_bounds[1][1])

        return latitude, longitude


class DistanceGeometricAlgorithm(OptimizationAlgorithm):
    """This class implements the distance based optimization algorithm."""

    pass


class CoverageGeometricAlgorithm(OptimizationAlgorithm):
    """This class implements the coverage oriented optimization algorithm."""

    pass


class HillClimberOptimizationAlgorithm(OptimizationAlgorithm):
    """This class implements the hill climber optimization algorithm."""

    def __init__(self,
                 loss_function,
                 station_bounds,
                 num_stations=3,
                 num_mutations=1,
                 max_shift_proportion=0.1,
                 seed=None):

        self.num_mutations = num_mutations
        self.max_shift_proportion = max_shift_proportion
        super().__init__(loss_function, num_stations, station_bounds, seed)

    def initialize_placements(self):
        """This function makes initial station placements and computes initial fitness."""

        # place the stations randomly
        for _ in range(self.num_stations):
            self.station_placements.append(self.get_random_station_location())

        # find the fitness
        self.fitness = self.loss_function(self.station_placements)

    def get_mutated_placements(self):
        """Returns a list of station placements that are mutated from the current placements."""

        # determine how far each station can move
        max_lat_shift = (self.station_bounds[1][0] - self.station_bounds[0][0]) * self.max_shift_proportion
        max_lon_shift = (self.station_bounds[1][1] - self.station_bounds[0][1]) * self.max_shift_proportion

        # mutate the list of station placements
        mutated_station_placements = [station for station in self.station_placements]
        for _ in range(self.num_mutations):
            index = random.randint(0, len(self.station_placements)-1)
            placement = self.station_placements[index]
            lat_shift = random.uniform(-max_lat_shift, max_lat_shift)
            lon_shift = random.uniform(-max_lon_shift, max_lon_shift)
            new_placement = (placement[0] + lat_shift, placement[1] + lon_shift)
            mutated_station_placements[index] = new_placement

        return mutated_station_placements

    def update_placements(self):
        """
        Calling this function runs the next iteration of the hill climber optimization algorithm.
        Returns the improvement in fitness over the previous iteration (if any).
        """

        # find new station coordinates and evaluate their fitness
        new_placements = self.get_mutated_placements()
        new_fitness = self.loss_function(new_placements)

        # if fitness has improved, replace the current solution with the new one
        if self.fitness > new_fitness:
            self.station_placements = new_placements
            self.fitness = new_fitness

        return self.fitness


class EvolutionaryOptimizationAlgorithm(OptimizationAlgorithm):
    """This class implements the genetic optimization algorithm."""

    def __init__(self,
                 loss_function,
                 station_bounds,
                 num_stations=3,
                 pop_size=5,
                 survivor_proportion=2,
                 num_mutations=1,
                 max_shift_proportion=0.1,
                 seed=None):

        self.pop_size = pop_size
        self.survivor_proportion = survivor_proportion
        self.num_mutations = num_mutations
        self.max_shift_proportion = max_shift_proportion
        self.fitness_scores = []
        super().__init__(loss_function, num_stations, station_bounds, seed)

    def initialize_placements(self):
        """This function makes initial station placements and computes initial fitness."""

        # place the stations randomly
        for _ in range(self.pop_size):
            pop = []
            for _ in range(self.num_stations):
                pop.append(self.get_random_station_location())
            self.station_placements.append(pop)

        # find the fitness
        self.fitness_scores, self.fitness = self.get_fitness_scores(self.station_placements)

    def get_fitness_scores(self, placements):
        """This function returns the fitness of each member of the population and best (lowest) fitness."""

        fitness_scores = []
        for pop in placements:
            fitness_scores.append(self.loss_function(pop))

        return fitness_scores, min(fitness_scores)

    def get_mutated_placements(self):
        """Returns a list of station placements that are mutated from the current placements."""

        # determine how far each station can move
        max_lat_shift = (self.station_bounds[1][0] - self.station_bounds[0][0]) * self.max_shift_proportion
        max_lon_shift = (self.station_bounds[1][1] - self.station_bounds[0][1]) * self.max_shift_proportion

        # mutate the list of station placements
        mutated_station_placements = [pop[:] for pop in self.station_placements]
        for p in range(self.pop_size):
            for _ in range(self.num_mutations):
                index = random.randint(0, self.num_stations-1)
                placement = self.station_placements[p][index]
                lat_shift = random.uniform(-max_lat_shift, max_lat_shift)
                lon_shift = random.uniform(-max_lon_shift, max_lon_shift)
                new_placement = (placement[0] + lat_shift, placement[1] + lon_shift)
                mutated_station_placements[p][index] = new_placement

        return mutated_station_placements

    def get_survivors(self):
        """Returns a new population with only the survivors with the best fitness scores."""

        surviving_station_placements = []
        num_survivors = int(self.survivor_proportion * self.pop_size)
        for _ in range(num_survivors):
            best_index = self.fitness_scores.index(min(self.fitness_scores))
            surviving_station_placements.append(self.station_placements[best_index])
            self.fitness_scores[best_index] = 99999

        return surviving_station_placements

    def crossover(self):
        """This function fills any missing population with crossover and returns the result."""

        crossover_station_placements = [pop[:] for pop in self.station_placements]
        while len(crossover_station_placements) < self.pop_size:
            new_pop = []
            for _ in range(self.num_stations):
                new_pop.append(random.choice(random.choice(self.station_placements)))
            crossover_station_placements.append(new_pop)

        return crossover_station_placements

    def update_placements(self):
        """
        Calling this function runs the next iteration of the evolutionary algorithm.
        Returns the best fitness achieved in this generation.
        """

        # find new station coordinates and evaluate their fitness
        new_placements = self.get_mutated_placements()
        self.fitness_scores, self.fitness = self.get_fitness_scores(new_placements)
        self.station_placements = self.get_survivors()
        self.station_placements = self.crossover()

        return self.fitness

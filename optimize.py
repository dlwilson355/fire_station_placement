"""This file contains code for optimizing the placement of fire stations."""


from optimization_algorithm import OptimizationAlgorithm

from sumo_interface import get_response_times, get_network_coordinate_bounds, get_network_file_path


# def simulate():
#     directory = "staten_island_south_west"
#     station_coordinates = load_nyc_station_coordinates()
#     response_times = get_response_times(directory, station_coordinates, gui=True)
#     print(response_times)
#     print(sum(response_times) / len(response_times))


def run_algorithm():
    directory = 'staten_island_sample'
    loss_function = lambda placements: get_response_times(directory, placements, 3, gui=False)
    bounds = get_network_coordinate_bounds(get_network_file_path(directory))
    algorithm = OptimizationAlgorithm(loss_function, 3, bounds)

    print("Losses")
    print(algorithm.get_loss())


if __name__ == "__main__":
    run_algorithm()

"""
This file contains settings applicable to where data is located and output is saved.
It also provides functionality for finding and manipulating input and output file paths.
"""

import os
import sys


OUTPUT_DIRECTORY = "plots"
POLICE_DATA_DIRECTORY = "police_data"
SIMULATION_DATA_DIRECTORY = "sumo_data"


def get_output_file_path(file_name):
    return os.path.join(OUTPUT_DIRECTORY, file_name)


def get_police_data_file_path(file_name):
    return os.path.join(POLICE_DATA_DIRECTORY, file_name)


def get_simulation_data_file_path(sim_name):
    return os.path.join(SIMULATION_DATA_DIRECTORY, sim_name)


def create_output_directory():
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.mkdir(OUTPUT_DIRECTORY)


def get_sumo_directory():
    if 'SUMO_HOME' in os.environ:
        sumo_directory = os.environ['SUMO_HOME']
        return sumo_directory
    else:
        raise ModuleNotFoundError("Install SUMO and the environmental variable 'SUMO_HOME' will be automatically set."
                                  "Please see the installation instructions: https://sumo.dlr.de/docs/Installing.html")


def import_sumo_tools():
    """Imports the sumo tools directory so that its packages can be loaded."""

    sumo_tools_directory = os.path.join(get_sumo_directory(), 'tools')
    sys.path.append(sumo_tools_directory)


def get_sumo_executable():
    pass


def get_sumo_tools_directory():
    return os.path.join(get_sumo_directory(), 'tools')

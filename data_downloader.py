"""This file downloads all the data sets."""

import os
import warnings

import gdown

from file_paths import SIMULATION_DATA_DIRECTORY, POLICE_DATA_DIRECTORY


def download_data(url, save_directory, temp_name="data"):
    if os.path.exists(save_directory):
        warnings.warn(f"The data in {save_directory} has already been downloaded."
                      f"\nDelete the directory if you want to download it again.")
    else:
        temp_name += '.zip'
        gdown.cached_download(url, temp_name, postprocess=gdown.extractall)
        os.remove(temp_name)


if __name__ == "__main__":
    police_data_url = r'https://drive.google.com/uc?id=1VPV9fZssEfuVYD4zhAPRbGE-SjWmKkYy'
    sumo_data_url = r'https://drive.google.com/uc?id=1Wqhqrjyr4nwKO8PYBYGN3OZQPWRWOOyA'

    download_data(police_data_url, POLICE_DATA_DIRECTORY)
    download_data(sumo_data_url, SIMULATION_DATA_DIRECTORY)

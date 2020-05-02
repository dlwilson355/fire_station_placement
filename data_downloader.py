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


def download_sumo_data():
    if os.path.exists(SIMULATION_DATA_DIRECTORY):
        warnings.warn(f"The SUMO data in {SIMULATION_DATA_DIRECTORY} has already been downloaded."
                      f"\nDelete the directory if you want to download it again.")
    else:
        url = r'https://drive.google.com/uc?id=1Wqhqrjyr4nwKO8PYBYGN3OZQPWRWOOyA'
        output = 'sumo_data.zip'
        gdown.cached_download(url, output, postprocess=gdown.extractall)
        os.remove(output)
        os.rename('sumo_data', SIMULATION_DATA_DIRECTORY)


def download_police_data():
    if os.path.exists(POLICE_DATA_DIRECTORY):
        warnings.warn(f"The police data in {POLICE_DATA_DIRECTORY} has already been downloaded."
                      f"\nDelete the directory if you want to download it again.")
    else:
        url = r'https://drive.google.com/uc?id=1VPV9fZssEfuVYD4zhAPRbGE-SjWmKkYy'
        output = 'police_data.zip'
        gdown.cached_download(url, output, postprocess=gdown.extractall)
        os.remove(output)
        os.rename('police_data', POLICE_DATA_DIRECTORY)


if __name__ == "__main__":

    # download_sumo_data()
    # download_police_data()
    download_data(r'https://drive.google.com/uc?id=1VPV9fZssEfuVYD4zhAPRbGE-SjWmKkYy', POLICE_DATA_DIRECTORY)
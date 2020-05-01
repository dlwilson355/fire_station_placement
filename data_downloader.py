"""This file downloads all the data sets."""

import gdown
import os

url = r'https://drive.google.com/uc?id=1Wqhqrjyr4nwKO8PYBYGN3OZQPWRWOOyA'
output = 'sumo_data.zip'
# gdown.download(url, output, quiet=False)

# url = r'https://drive.google.com/uc?id=1y6m6jHArNX5oDm6cGX_T_gJmp0GSKRjh'
# output = r'test.xlsx'
# gdown.download(url, output, quiet=False)

# md5 = 'fa837a88f0c40c513d975104edf3da17'
# gdown.cached_download(url, output, md5=md5, postprocess=gdown.extractall)
gdown.cached_download(url, output, postprocess=gdown.extractall)
os.remove(output)
#TODO clean code, add checksums, rename downloaded file using file_paths, add downloads for all data sources
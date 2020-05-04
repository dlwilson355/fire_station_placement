# fire_station_placement
The goal of this project is to optimize the placement of fire stations to minimize response times.

This project requires you to install SUMO.  Instructions can be found here: https://sumo.dlr.de/docs/index.html
Note that line sumo_exectuable = 'sumo.exe' in sumo_interface.py may have a different name for different operating
systems depending on what SUMO names it.

Gdown can be installed with conda.
conda install -c conda-forge gdown

All other dependencies are included with Anaconda by default.  Code works with python 3.7.

Running data_downloader.py downloads the datasets for this project.
Running sumo_interface.py runs a sample simulation in SUMO.
Running exploratory_data_analysis.py performs the exploratory analysis.
Running simulated_response_time_analysis.py performs the analysis comparing the response times of the simulated fire
department to the response times of the real department.
Running optimize.py performs the fire station optimization.
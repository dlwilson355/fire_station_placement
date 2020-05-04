"""This file generates plots of road networks."""

import os

from file_paths import get_simulation_data_file_path, get_output_file_path, get_sumo_tools_directory


tools_dir = os.path.join(get_sumo_tools_directory(), 'visualization')
net_filepath = os.path.join(get_simulation_data_file_path('staten_island_sample'), 'osm.net.xml')
output_file_path = get_output_file_path('road_speeds.png')

command = f"python \"{os.path.join(tools_dir, 'plot_net_speeds.py')}\" -n \"{net_filepath}\" " \
          f"--xlim 1000,6000 " \
          f"--ylim 1000,4000 " \
          f"--edge-width .5 " \
          f"-o {output_file_path} " \
          f"--minV 0 --maxV 60 " \
          f"--xticks 16 --yticks 16 " \
          f"--colormap jet"

os.system(command)

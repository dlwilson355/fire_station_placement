"""This file generates plots of road networks."""
# TODO: Improve this code.

import os

tools_dir = r'C:\Program Files (x86)\Eclipse\Sumo\tools\visualization'
net_filepath = r'C:\Users\Daniel\OneDrive\Documents\School Work\Data Science 2\HW\fire_station_placement\staten_island_sample\osm.net.xml'
output_file_path = os.path.join("plots", "road_speeds.png")

command = f"python \"{os.path.join(tools_dir, 'plot_net_dump.py')}\" -v -n \"{net_filepath}\" " \
         f"--xticks 7000,14001,2000,16 " \
         f"--yticks 9000,16001,1000,16 " \
         f"--measures entered,entered " \
         f"--xlabel [m] " \
         f"--ylabel [m] " \
         f"--default-width 1 " \
         f"-i base-jr.xml,base-jr.xml" \
         f"--xlim 7000,14000 " \
         f"--ylim 9000,16000 " \
         f"--default-width .5 --default-color #606060 " \
         f"--min-color-value -1000 --max-color-value 1000 " \
         f"--max-width-value 1000 --min-width-value -1000 " \
         f"--max-width 3 --min-width .5 " \
         f"--colormap #0:#0000c0,.25:#404080,.5:#808080,.75:#804040,1:#c00000"

command = f"python \"{os.path.join(tools_dir, 'plot_net_speeds.py')}\" -n \"{net_filepath}\" " \
          f"--xlim 1000,6000 " \
          f"--ylim 1000,4000 " \
          f"--edge-width .5 " \
          f"-o {output_file_path} " \
          f"--minV 0 --maxV 60 " \
          f"--xticks 16 --yticks 16 " \
          f"--colormap jet"
          # f"--xlabel [m] --ylabel [m] " \
          # f"--xlabelsize 16 --ylabelsize 16 " \

print(command)
os.system(command)

"""
This file starts the OSM wizard.
The wizard can be used to create a data set.
"""

import os

from file_paths import get_sumo_tools_directory


osm_wizard_path = os.path.join(get_sumo_tools_directory(), 'osmWebWizard.py')
os.system(f'python "{osm_wizard_path}"')

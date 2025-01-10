"""
The task is to create a house keeping script which will delete files in a specified directory that are x no. days
old from the current date.
"""

import os
import yaml
from datetime import datetime, timedelta
import re

with open("./cleaning_config.yaml", "r") as file:
    config = yaml.safe_load(file)

folders = []
number_of_days = []
patterns = []

for dict in config["input_paths"]:
    for key in dict.keys():
        if key == "dir":
            filename = dict.get(key)
            folders.append(os.path.abspath(filename))
        if key == "number_of_days":
            number_of_days.append(dict.get(key))
        if key == "pattern":
            patterns.append(dict.get(key))

current_date = datetime.now()
formatted_current_date = current_date.strftime("%Y%m%d")

for folder in folders:

    folder_index = folders.index(folder)
    
    old_date = current_date - timedelta(days=number_of_days[folder_index])
    formatted_old_date = old_date.strftime("%Y%m%d")

    pattern = f"r'{patterns[folder_index]}'"

    for filename in os.listdir(folder):
        match = re.match(pattern, filename)
        
        if match:

            date_str = match.group(1)
            print(date_str)
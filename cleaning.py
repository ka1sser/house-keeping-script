"""
The task is to create a house keeping script which will delete files in a specified directory that are x no. days
old from the current date.
"""

import os
import yaml

with open("./cleaning_config.yaml", "r") as file:
    config = yaml.safe_load(file)

folder = []
number_of_days = []
pattern = []

for dict in config["input_paths"]:
    for key in dict.keys():
        if key == "dir":
            filename = dict.get(key)
            folder.append(os.path.abspath(filename))
        if key == "number_of_days":
            number_of_days.append(dict.get(key))
        if key == "pattern":
            pattern.append(dict.get(key))


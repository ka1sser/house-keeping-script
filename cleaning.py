"""
The task is to create a house keeping script which will delete files in a specified directory that are x no. days
old from the current date.
"""

import os
import yaml
from datetime import datetime, timedelta
import glob
import logging
from logging.handlers import TimedRotatingFileHandler

with open("./cleaning_config.yaml", "r") as file:
    config = yaml.safe_load(file)

output_file_path = config["log_file"]["path"]
log_dir = os.path.abspath(output_file_path)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file_path = os.path.join(log_dir, "app.log")

time_logger = logging.getLogger("TimeBasedLogger")
time_logger.setLevel(logging.INFO)

#Change when and interval depending on the need
time_handler = TimedRotatingFileHandler(log_file_path, when="s", interval=30, backupCount=7)
time_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
time_handler.setFormatter(formatter)
time_logger.addHandler(time_handler)

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

    pattern = patterns[folder_index]

    if not os.listdir(folder):
            time_logger.info(f"Checking {folder}...")
            time_logger.warning(f"Folder is empty!")
            time_logger.info("Skipping...\n")
    
    else:

        for filename in os.listdir(folder):
            
            files = glob.glob(os.path.join(folder, pattern))

            if not files:
                time_logger.info(f"Checking {folder}...")
                time_logger.warning("No files matching the pattern.\n")

            else:
                for file in files:
                    time_logger.info(f"{os.path.basename(file)} matches {pattern}")
                    time_logger.warning(f"Deleting file: {os.path.basename(file)}")
                    time_logger.info("File successfully deleted.\n")
                    os.remove(file)
        

    


        
    
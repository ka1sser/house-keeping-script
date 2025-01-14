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

def load_yaml():
    with open("./cleaning_config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config

def check_path(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

def load_folders(config):
    folders = []
    for dict in config["input_paths"]:
        for key in dict.keys():
            if key == "dir":
                folders.append(dict.get(key))
    return folders

def load_number_of_days(config):
    number_of_days = []
    for dict in config["input_paths"]:
        for key in dict.keys():
            if key == "number_of_days":
                number_of_days.append(dict.get(key))
    return number_of_days

def load_patterns(config):
    patterns = []
    for dict in config["input_paths"]:
        for key in dict.keys():
            if key == "pattern":
                patterns.append(dict.get(key))
    return patterns

def delete_file(file):
    os.remove(file)

def main():
    config = load_yaml()

    current_date = datetime.now()
    formatted_current_date = current_date.strftime("%Y%m%d")

    folders = load_folders(config)
    number_of_days = load_number_of_days(config)
    patterns = load_patterns(config)

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
            all_files = [os.path.join(folder, f) for f in os.listdir(folder)]
            matching_files = glob.glob(os.path.join(folder, pattern))
            
            for file in all_files:
                if file not in matching_files:
                    time_logger.warning(f"{os.path.basename(file)} does not match the [{pattern}] pattern.")
                    time_logger.info("Skipping...\n")
                else:
                    time_logger.info(f"{os.path.basename(file)} matches the [{pattern}] pattern.")
                    time_logger.warning(f"Deleting file: {os.path.basename(file)}")
                    time_logger.info("File successfully deleted.\n")
                    delete_file(file)

if __name__ == "__main__":
    time_logger = logging.getLogger("TimeBasedLogger")
    time_logger.setLevel(logging.INFO)

    config = load_yaml()
    log_dir = config["log_file"]["path"]
    check_path(log_dir)
    log_file_path = os.path.join(log_dir, "app.log")
    #Change when and interval depending on the need
    time_handler = TimedRotatingFileHandler(log_file_path, when="s", interval=5, backupCount=7)
    time_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    
    time_handler.setFormatter(formatter)
    time_logger.addHandler(time_handler)
    
    time_logger.info("------------------------------------------------------------------------")
    time_logger.info("Housekeeping script called...")
    time_logger.info("------------------------------------------------------------------------")
    main()
    time_logger.info("------------------------------------------------------------------------")
    time_logger.info("Housekeeping script exited...")
    time_logger.info("------------------------------------------------------------------------")
    
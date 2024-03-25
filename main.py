import schedule
import time
from datetime import datetime
import os
import utils


######################################################################################
###
###  Beggining of the execution 
###
######################################################################################

reserved_names = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 
                          'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 
                          'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
number = 0
while True:
    user_input = input("Please enter how often (in seconds) the copy should be performed: ")
    try:
        number = int(user_input)
        if number > 0:
            break  # Exit the loop if the input is a positive integer
        else:
            print("Please enter a positive integer.")
    except ValueError:
        print("Please enter a valid integer.")

source_folder = ""
while True:
    source_folder = input("Please enter the complete path of the selected source folder: ")
    try:
        if os.path.isdir(source_folder):
            break  # Exit the loop if the input is valid
        else:
            print("Please enter a valid path of an existing folder.")
    except:
        print("Please enter a valid folder path. (other error)")
 
destination_folder = ""           
while True:
    destination_folder = input("Please enter the complete path of the selected destination folder (if not existing, it will be created): ")
    if not os.path.exists(destination_folder):
        try:
            if not destination_folder == "" or not destination_folder == source_folder:
                if not any(char in r'*?"<>|' for char in destination_folder):
                    if not destination_folder.upper() in reserved_names:
                        break  # Exit the loop if the input is valid
                    else:
                        print("Name not valid. The folder is using a reserved name")
                else:
                    print("Name not valid, the folder cannot contain special characters like '*?\"<>|'")
            else:
                print("Please enter a valid folder path and folder name.")
        except:
            print("Please enter a valid folder path. (other error)")  

log_file = ""
while True:
    log_file = input("Please enter the complete path of the desired log file (if not existing, it will be created) (if existing, will be appended to the end): ")
    if not os.path.exists(log_file):
        try:
            if not log_file == "" or not log_file == source_folder:
                if not any(char in r'*?"<>|' for char in log_file):
                    if not log_file.upper() in reserved_names:
                        break  # Exit the loop if the input is valid
                    else:
                        print("Name not valid. The file is using a reserved name")
                else:
                    print("Name not valid, the file cannot contain special characters like '*?\"<>|'")
            else:
                print("Please enter a valid file path and file name.")
        except:
            print("Please enter a valid file path. (other error)")


schedule.every(number).seconds.do(lambda: utils.periodic_task(source_folder, destination_folder, log_file))

while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep to reduce CPU usage

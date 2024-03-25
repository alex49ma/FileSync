import schedule
import time
import platform
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
    except Exception as e:
        print("Please enter a valid folder path: " + str(e))
 
destination_folder = ""           
while True:
    destination_folder = input("Please enter the complete path of the selected destination folder (if not existing, it will be created): ")
    if not os.path.exists(destination_folder):
        try:
            if not (destination_folder == "" or destination_folder == source_folder):
                if not any(char in r'*?"<>|' for char in destination_folder) and destination_folder.count(":") == 1:
                    if platform.system() == "Windows":
                        # If the system is Windows, it has several directory names that are restricted and cannot be modified
                        folder_names = destination_folder.upper().split("\\")
                        deny_access = False
                        for name in folder_names:
                            if name in reserved_names:
                                deny_access = True
                                print("Name not valid. The path is using a reserved name")
                                break  
                            # The flag deny_access will be true to not let you continue if you are using any of the reserved names in Windows
                        if not deny_access:
                            break
                    else:
                        break
                else:
                    print("Name not valid, the folder path cannot contain special characters like '*?\"<>|'")
            else:
                print("Please enter a valid folder path and folder name.")
        except Exception as e:
            print("Please enter a valid folder path: " + str(e))  

log_file = ""
while True:
    log_file = input("Please enter the complete path (and name) of the desired log file (if not existing, it will be created) (if existing, it will be appended to the end): ")
    if not os.path.exists(log_file):
        try:
            if not log_file == "":
                if not any(char in r'*?"<>|' for char in log_file) and destination_folder.count(":") == 1:
                    if platform.system() == "Windows": 
                        # If the system is Windows, it has several directory names that are restricted and cannot be modified
                        folder_names = destination_folder.upper().split("\\")
                        deny_access = False
                        for name in folder_names:
                            if name in reserved_names:
                                deny_access = True
                                print("Name not valid. The path is using a reserved name")
                                break  
                            # The flag deny_access will be true to not let you continue if you are using any of the reserved names in Windows
                        if not deny_access:
                            break
                    else:
                        break
                else:
                    print("Name not valid, the file path cannot contain special characters like '*?\"<>|'")
            else:
                print("Please enter a valid file path and file name.")
        except Exception as e:
            print("Please enter a valid file path: " + str(e))


schedule.every(number).seconds.do(lambda: utils.periodic_task(source_folder, destination_folder, log_file))

while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep to reduce CPU usage

import schedule
import time
import shutil
import sys
import os

######################################################################################
###
###  Functions
###
######################################################################################

            # Input:
            #       Two partially validated paths
            # Action:
            #       - Asks the recursive algorithm to perform a copy on the inputs
            #       - Saves in a Log file
            # Output:
            #       
def periodic_task(source_folder, destination_folder, log_file):
    recursive_folder_copy(source_folder, destination_folder)
    print("Backup performed onto '" + destination_folder + "'. \n Press 'Ctrl + C' to stop the periodic backup")
    log_save(log_file)


            # Input:
            #       
            # Action:
            #       Iterates through all files inside a folder. If it finds a folder, it recursively iterates through those too
            # Output:
            #       
def recursive_folder_copy(source_folder, destination_folder):

    # Make sure the destination folder exists or create it if it doesn't
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)             # Make sure to register this in the log in the future
        print("Directory " + destination_folder + " created")
    else:
        if os.listdir(destination_folder):
            for item in os.listdir(destination_folder):
                if not item in os.listdir(source_folder):
                    item_path = os.path.join(destination_folder, item)
                    if os.path.isdir(item_path):
                        recursively_delete(item_path)
                    else:
                        try:
                            os.remove(item_path)
                            print("File " +  item_path + " deleted")            # Make sure to register this in the log in the future
                        except:
                            print("File " +  item_path + "could not be deleted")            # Make sure to register this in the log in the future
    
    if not os.listdir(source_folder):
        print("Source folder is empty")
    else:
        for item in os.listdir(source_folder):
            source_path = os.path.join(source_folder, item)
            destination_path = os.path.join(destination_folder, item)
            print(destination_path)
            if os.path.isdir(source_path):
                recursive_folder_copy(source_path, destination_path)
                # use the recursion
                # not allowed: shutil.copytree(source_path, destination_path)
            else:
                pass
                # not allowed: shutil.copy2(source_path, destination_path)
            
def log_save(log_path):
    pass

def recursively_delete(path):
    pass

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

        destination_folder = "copy"   

log_file = ""
while True:
    log_file = input("Please enter the complete path of the desired log file (if not existing, it will be created): ")
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


schedule.every(number).seconds.do(lambda: periodic_task(source_folder, destination_folder, log_file)) #(source_folder, destination_folder)
print(number)


while True:
    schedule.run_pending()
    time.sleep(1)  # Optional: sleep to reduce CPU usage
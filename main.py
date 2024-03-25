import schedule
import time
from datetime import datetime
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
    print("Copy in process: copying folder " + source_folder + " onto folder " + destination_folder)
    to_save = "\n\n\tBackup at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n\n"
    to_save += recursive_folder_copy(source_folder, destination_folder)
    print("Backup performed onto '" + destination_folder + "'. \n Press 'Ctrl + C' to stop the periodic backup")
    log_save(log_file, to_save)


            # Input:
            #       
            # Action:
            #       Iterates through all files inside a folder. If it finds a folder, it recursively iterates through those too
            # Output:
            #       
def recursive_folder_copy(source_folder, destination_folder, to_save = ""):

    if not os.path.exists(destination_folder): # Make sure the destination folder exists or create it if it doesn't
        try:
            os.makedirs(destination_folder)
            to_save += "Directory " + destination_folder + " created.\n"
            print("Directory " + destination_folder + " created")            # Saving for the log file
        except:
            to_save += "Directory " + destination_folder + " could not be created.\n"
            print("Directory " + destination_folder + " could not be created")            # Saving for the log file

    else: # If the folder does exist, it may have files that do not exist in the source folder, and therefore, should be deleted
        if os.listdir(destination_folder):
            for item in os.listdir(destination_folder):
                if not item in os.listdir(source_folder):
                    item_path = os.path.join(destination_folder, item)
                    if os.path.isdir(item_path):
                        to_save += recursively_delete(item_path, to_save)
                    else:
                        try:
                            os.remove(item_path)
                            to_save += "File " +  item_path + " deleted.\n"
                            print("File " +  item_path + " deleted")            # Saving for the log file
                        except:
                            to_save += "File " +  item_path + " could not be deleted.\n"
                            print("File " +  item_path + "could not be deleted")            # Saving for the log file
    
    if os.listdir(source_folder): # The copy begins
        for item in os.listdir(source_folder):
            source_path = os.path.join(source_folder, item)
            destination_path = os.path.join(destination_folder, item)
            if os.path.isdir(source_path):
                # Recursion
                to_save += recursive_folder_copy(source_path, destination_path, to_save)
            else:
                match_files = copy_file(source_path, destination_path)
                if not match_files:
                    to_save += "File " + source_path + " copied to " + destination_path + " successfully.\n"            # Saving for the log file
    return to_save
            
def log_save(log_path, to_save):
    try:
        file = open(log_path, "a")
        file.write(to_save)
        file.close()
    except Exception as e:
        print("Log file could not be written: " + str(e))

def recursively_delete(folder_path, to_save = ""):
    if os.listdir(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                to_save += recursively_delete(item_path, to_save)
            else:
                try:
                    os.remove(item_path)
                    to_save += "File " +  item_path + " deleted"
                    print("File " +  item_path + " deleted")            # Saving for the log file
                except:
                    to_save += "File " +  item_path + "could not be deleted"
                    print("File " +  item_path + "could not be deleted")            # Saving for the log file
    return to_save

def copy_file(source_path, destination_path, buffer_size=1024*1024):  # 1MB buffer size
    try:
        match_files = os.path.exists(destination_path)          # To be able to mathc, it first has to exist. Afterwards we will compare the inside
        with open(source_path, 'rb') as source_file:
            with open(destination_path, 'wb') as destination_file:
                while True:
                    data = source_file.read(buffer_size)
                    if not data:
                        break
                    destination_file.write(data)
                    if match_files and data != destination_file.read(len(data)):
                        match_files = False  # Set to False if chunks don't match
        if not match_files:
            print(f"File '{source_path}' copied to '{destination_path}' successfully.")            # Saved after this function for the log file
        return match_files
    except Exception as e:
        print(f"Error: {e}")
        return False

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
    log_file = input("Please enter the complete path of the desired log file (if not existing, it will be created) (if existing, will be appended to the end): ")
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


schedule.every(number).seconds.do(lambda: periodic_task(source_folder, destination_folder, log_file))

while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep to reduce CPU usage

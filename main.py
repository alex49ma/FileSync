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
            #       Two validated paths
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
            #       Two validated paths and an optional string chain for the log
            # Action:
            #       Iterates through all files inside a folder. If it finds a folder, it recursively iterates through those too
            # Output:
            #       Returns the string chain to be stored in the log file
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
                    item_type = "File "
                    if os.path.isdir(item_path):
                        item_type = "Directory "
                        to_save += recursively_delete(item_path, to_save)       # We delete the things inside first to have a track of all the deleted elements in our log
                        
                    try:
                        os.remove(item_path)
                        to_save += item_type +  item_path + " deleted.\n"
                        print(item_type +  item_path + " deleted")            # Saving for the log file
                    except Exception as e:
                        to_save += item_type +  item_path + " could not be deleted.\n"
                        print(item_type +  item_path + "could not be deleted: " + str(e))            # Saving for the log file
    
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


            # Input:
            #       A string path for the log file and a string content
            # Action:
            #       Saves the string content in the path
            # Output:
            #               
def log_save(log_path, to_save):
    try:
        file = open(log_path, "a")
        file.write(to_save)
        file.close()
    except Exception as e:
        print("Log file could not be written: " + str(e))


            # Input:
            #       A string path for the folder to be deleted and an optional string chain for the log
            # Action:
            #       Iterates through all the folders to save the logs and deletes the files afterwards
            # Output:
            #       Returns the string chain to be stored in the log file
def recursively_delete(folder_path, to_save = ""):
    if os.listdir(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            item_type = "File "
            if os.path.isdir(item_path):
                item_type = "Directory "
                to_save += recursively_delete(item_path, to_save) # We delete the things inside first to have a track of all the deleted elements in our log
            try:
                os.remove(item_path)
                to_save += item_type +  item_path + " deleted.\n"
                print(item_type +  item_path + " deleted")            # Saving for the log file
            except:
                to_save += item_type +  item_path + "could not be deleted.\n"
                print(item_type +  item_path + "could not be deleted")            # Saving for the log file
    return to_save


            # Input:
            #       Two string paths, the first with a source file and the second one with the destination file. Also an optional buffer size for comparisons
            # Action:
            #       Iterates through the file source while copying on the destination
            # Output:
            #       Returns if the files were already identical at the begining of the operation
def copy_file(source_path, destination_path, buffer_size=1024*1024):  # 1MB buffer size
    try:
        match_files = compare_files(source_path, destination_path)
        if not match_files:
            with open(source_path, 'rb') as source_file:
                with open(destination_path, 'wb') as destination_file:
                    while True:
                        data = source_file.read(buffer_size)
                        if not data:
                            break
                        destination_file.write(data)
            print(f"File '{source_path}' copied to '{destination_path}' successfully.")            # Saved after this function for the log file
        return match_files
    except Exception as e:
        print(f"Error: {e}")
        return False


            # Input:
            #       Two string paths, the first with a source file and the second one with the destination file
            # Action:
            #       Iterates through the file source and destination comparing the content
            # Output:
            #       Returns if the files were already identical at the begining of the operation 
def compare_files(source_path, destination_path):
    try:
        with open(source_path, 'rb') as file1:
            with open(destination_path, 'rb') as file2:
                # Compare file contents chunk by chunk
                while True:
                    chunk1 = file1.read(4096)  # Read 4KB at a time
                    chunk2 = file2.read(4096)
                    if chunk1 != chunk2:
                        return False  # Files are different
                    if not chunk1 and not chunk2:
                        break  # Reached end of both files
        return True  # Files are identical
    except IOError as e:
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

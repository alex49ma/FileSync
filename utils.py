from datetime import datetime
import os
import filecmp


######################################################################################
###
###  Functions
###
######################################################################################

            # Input:
            #       Two validated paths
            # Action:
            #       - Asks the recursive algorithm to perform a copy on the inputs
            #       - Saves in a Log file with current date and time
            # Output:
            #       
def periodic_task(source_folder, destination_folder, log_file):
    print("Copy in process: copying folder " + source_folder + " onto folder " + destination_folder)
    to_save = "\n\n\tBackup at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n\n"
    ret = recursive_folder_copy(source_folder, destination_folder)
    if ret == "":
        ret = "No changes performed to the destination directory.\n"
    to_save += ret
    print("Backup performed onto '" + destination_folder + "'. \n Press 'Ctrl + C' to stop the periodic backup")
    log_save(log_file, to_save)


            # Input:
            #       Two validated paths and an optional string chain for the log
            # Action:
            #       Iterates through all files inside a folder. If it finds a folder, it recursively iterates through those too
            # Output:
            #       Returns the string chain to be stored in the log file
def recursive_folder_copy(source_folder, destination_folder, to_save = ""):

    if not os.path.exists(destination_folder): 
        # Make sure the destination folder exists or create it if it doesn't
        try:
            os.makedirs(destination_folder)
            # Updating the variable for the log file content and printing console output
            to_save += "Directory '" + destination_folder + "' created.\n"
            print("Directory '" + destination_folder + "' created")
        except:
            # Updating the variable for the log file content and printing console output
            to_save += "Directory '" + destination_folder + "' could not be created.\n"            
            print("Directory '" + destination_folder + "' could not be created")

    else: 
        # If the folder does exist, it may have files that do not exist in the source folder, and therefore, should be deleted
        if os.listdir(destination_folder):
            for item in os.listdir(destination_folder):
                if not item in os.listdir(source_folder):                   
                    # If an item is not in the source folder, it will be deleted
                    item_path = os.path.join(destination_folder, item)
                    try:
                        item_type = "File '"
                        if os.path.isdir(os.path.join(destination_folder, item)):
                            item_type = "Directory '"
                            to_save = recursively_delete(item_path, to_save)
                            os.rmdir(item_path)
                        else:
                            os.remove(item_path)
                            # Updating the variable for the log file content and printing console output
                        to_save += item_type +  item_path + "' deleted.\n"
                        print(item_type +  item_path + "' deleted")            
                    except:
                        # Updating the variable for the log file content and printing console output
                        to_save += "Item '" +  item_path + "' could not be deleted.\n"
                        print("Item '" +  item_path + "' could not be deleted")            
    
    if os.listdir(source_folder): 
        # The copy begins
        for item in os.listdir(source_folder):
            source_path = os.path.join(source_folder, item)
            destination_path = os.path.join(destination_folder, item)
            if os.path.isdir(source_path):          
                # If it is a directory, we perform the backup of that directory onto the copy folder
                to_save += recursive_folder_copy(source_path, destination_path)
            else:
                match_files = compare_files(source_path, destination_path)
                if not match_files:
                    success_copy = copy_file(source_path, destination_path)
                    if not isinstance(success_copy, Exception):
                        # Updating the variable for the log file content and printing console output
                        print("File '" + source_path + "' copied to '" + destination_path + "' successfully.")  
                        to_save += "File '" + source_path + "' copied to '" + destination_path + "' successfully.\n"            
                    else:
                        # Updating the variable for the log file content and printing console output
                        print("File '" + source_path + "' could not be copied to '" + destination_path + "': " + str(success_copy))  
                        to_save += "File '" + source_path + "' could not be copied to '" + destination_path + "': " + str(success_copy) + "\n"            
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
            #       A string path pointing the folder to be deleted and an optional string chain for the log
            # Action:
            #       Iterates through all the folders to save the logs and deletes the files afterwards
            # Output:
            #       Returns the string chain to be stored in the log file
def recursively_delete(folder_path, to_save = ""):
    if os.listdir(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            item_type = "File '"
            try:
                if os.path.isdir(item_path):
                    item_type = "Directory '"
                    to_save += recursively_delete(item_path, to_save)       
                    # We delete the things inside first to have a track of all the deleted elements in our log and because rmdir can only delete empty folders
                    os.rmdir(item_path)
                else:
                    os.remove(item_path)
                    # Updating the variable for the log file content and printing console output
                to_save += item_type +  item_path + "' deleted.\n"
                print(item_type +  item_path + "' deleted")            
            except:
                # Updating the variable for the log file content and printing console output
                to_save += "Item '" +  item_path + "' could not be deleted.\n"
                print("Item '" +  item_path + "' could not be deleted")            
    return to_save


            # Input:
            #       Two string paths, the first one pointing to a source file and the second one to a destination file
            # Action:
            #       Iterates through the file source while copying on the destination
            # Other alternatives:
            #       Using the method os.popen() or os.system() to perform system commands would be another effective way to copy the files, but 
            #           it would be system dependent, due to the fact that not all systems use the same commands (cp in Linux, copy in Windows).
            #           we have decided not to implement that option but could be done easily if required in the future.
            # Output:
            #       Returns True if the copy was completed succesfuly. Returns a type Exception if there was a problem during the copy
def copy_file(source_path, destination_path, buffer_size=1024*1024):
    try:
        with open(source_path, 'rb') as source_file:
            with open(destination_path, 'wb') as destination_file:
                while True:
                    data = source_file.read(buffer_size)
                    if not data:
                        break
                    destination_file.write(data)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return e


            # Input:
            #       Two string paths, the first one pointing to a source file and the second one to a destination file
            # Action:
            #       Iterates through the file source and destination comparing the content
            # Other alternatives:
            #       There are other libraries that perform file comparison, we can feel free to choose the one that suits better our project
            # Output:
            #       Returns if the files were already identical at the begining of the operation 
def compare_files(source_path, destination_path):
    try:
        result = filecmp.cmp(source_path, destination_path)
        return result
    except Exception:
        return False
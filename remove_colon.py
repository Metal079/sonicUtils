import os
import glob

def rename_files_in_dir(directory):
    # Get all files in the directory
    for filepath in glob.glob(os.path.join(directory, '*')):
        # Extract the directory and filename separately
        directory, filename = os.path.split(filepath)
        # Check if filename contains a colon
        if ':' in filename:
            # Create new filename by replacing colon with nothing
            new_filename = filename.replace(':', '')
            # Join the directory back with the new filename
            new_filepath = os.path.join(directory, new_filename)
            # Rename file
            os.rename(filepath, new_filepath)

# Use function on desired directory
rename_files_in_dir('C:\\Users\\metal\\Downloads\\sonic_training\\gamma_train_set')

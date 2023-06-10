import os
import shutil

from create_labels_json import tags_list, valid_image_extensions

# Define the list of strings you want to search for in the text files
# Convert all search strings to lower case
search_strings = [tag.lower() for tag in tags_list]

# Set the paths to the source and destination directories
source_dir = r'C:\Users\metal\Downloads\sonic_training\datasets\gamma_train_set - Copy'

# Flag for moving .txt files
move_txt_files = True

# Iterate through all the files in the source directory
for file in os.listdir(source_dir):
    if file.lower().endswith('.txt'):
        txt_file_path = os.path.join(source_dir, file)
        
        # Read the tags from the text file
        with open(txt_file_path, 'r') as txt_file:
            tags = [tag.strip().lower() for tag in txt_file.read().split(',')]
        
        # Check if any of the search strings are in the tags
        for string in search_strings:
            if string in tags:
                # Move the corresponding image file to the destination folder
                file_base = os.path.splitext(file)[0]
                for ext in valid_image_extensions:
                    image_file = file_base + ext
                    if os.path.exists(os.path.join(source_dir, image_file.lower())) or os.path.exists(os.path.join(source_dir, image_file.upper())):
                        break
                else:
                    print(f"Error, cannot find: {file_base}")
                    continue
                
                try:
                    source_image_path = os.path.join(source_dir, image_file)
                    dest_folder = os.path.join(source_dir, string)
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                    dest_image_path = os.path.join(dest_folder, image_file)
                    shutil.move(source_image_path, dest_image_path)

                    # If the flag is set, move the .txt file
                    if move_txt_files:
                        source_txt_path = os.path.join(source_dir, file)
                        dest_txt_path = os.path.join(dest_folder, file)
                        shutil.move(source_txt_path, dest_txt_path)
                except Exception as e:
                    print(f"Error while moving files: {str(e)}")
                    continue
                break  # Stop checking other strings if one is found

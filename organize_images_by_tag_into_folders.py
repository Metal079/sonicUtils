import os
import shutil

from create_labels_json import tags_list

# Define the list of strings you want to search for in the text files
search_strings = tags_list

# Set the paths to the source and destination directories
source_dir = '/media/pablo/6ED0B21ED0B1EC89/Users/metal/Downloads/sonic_training/datasets/charlie_train_set'

# Iterate through all the files in the source directory
for file in os.listdir(source_dir):
    if file.endswith('.txt'):
        txt_file_path = os.path.join(source_dir, file)
        
        # Read the tags from the text file
        with open(txt_file_path, 'r') as txt_file:
            tags = [tag.strip() for tag in txt_file.read().split(',')]
        
        # Check if any of the search strings are in the tags
        for string in search_strings:
            if string in tags:
                # Move the corresponding image file to the destination folder
                if os.path.exists(os.path.join(source_dir, os.path.splitext(file)[0] + ".jpg")):
                    image_file = os.path.splitext(file)[0] + ".jpg"
                elif os.path.exists(os.path.join(source_dir, os.path.splitext(file)[0] + ".png")):
                    image_file = os.path.splitext(file)[0] + ".png"
                elif os.path.exists(os.path.join(source_dir, os.path.splitext(file)[0] + ".jfif")):
                    image_file = os.path.splitext(file)[0] + ".jfif"
                else:
                    print(f"Error, cannot find: {os.path.splitext(file)[0]}")
                try:
                    source_image_path = os.path.join(source_dir, image_file)
                    dest_folder = os.path.join(source_dir, string)

                except:
                    continue
                
                # Create the destination folder if it doesn't exist
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                
                dest_image_path = os.path.join(dest_folder, image_file)
                try:
                    shutil.move(source_image_path, dest_image_path)
                except:
                    continue
                break  # Stop checking other strings if one is found

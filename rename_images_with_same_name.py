import os
import random
import string
from create_labels_json import valid_image_extensions

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

source_dir = r'C:\Users\metal\Downloads\sonic_training\datasets\gamma_train_set'  # replace with your directory

# Group files by their base name (name without extension)
file_dict = {}
for file in os.listdir(source_dir):
    base_name, ext = os.path.splitext(file)
    if ext.lower() in valid_image_extensions:  # only consider .txt and image files
        if base_name not in file_dict:
            file_dict[base_name] = [file]
        else:
            file_dict[base_name].append(file)

# Rename image files that have the same base name
renamed_count = 0  # Initialize counter for renamed files

for base_name, files in file_dict.items():
    image_files = [file for file in files if os.path.splitext(file)[1].lower() in valid_image_extensions]
    if len(image_files) > 1:  # if there are image files with the same base name
        for file in image_files:
            old_path = os.path.join(source_dir, file)
            _, ext = os.path.splitext(file)
            new_name = get_random_string(10) + ext  # generate a new random name, preserving the original extension
            new_path = os.path.join(source_dir, new_name)
            
            while os.path.exists(new_path):  # check if the random name already exists
                new_name = get_random_string(10) + ext  # if so, generate a new one
                new_path = os.path.join(source_dir, new_name)
            
            os.rename(old_path, new_path)
            renamed_count += 1  # Increment counter when a file is renamed

# Print out the number of files renamed
print(f"Renamed {renamed_count} files.")

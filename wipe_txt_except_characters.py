import os
import re
from create_labels_json import all_tags

# Flatten all_tags into a single list
all_tags = [tag for sublist in all_tags for tag in sublist]

# Prepare regex pattern
# Prepare regex pattern with re.IGNORECASE flag
pattern = re.compile(r'\b(' + '|'.join(all_tags) + r')\b', re.IGNORECASE)


# Function to clean the file
def clean_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Find all matches in the content
    matches = pattern.findall(content)

    # Write the matches back to the file, separated by comma and space
    with open(file_path, 'w') as file:
        file.write(', '.join(matches))


# Directory to be cleaned
directory = r"C:\Users\metal\Downloads\sonic_training\datasets\gamma_train_set"

# Iterate over every file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        clean_file(os.path.join(directory, filename))

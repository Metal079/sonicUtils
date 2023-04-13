import os
import shutil

folder_path = r"/media/pablo/6ED0B21ED0B1EC89/Users/metal/Downloads/sonic_training/datasets/delta_train_set"
# dst_folder = r"C:\Users\metal\gallery-dl\twitter_cleaned"

for root, dir, files in os.walk(folder_path):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        if file_name.endswith('.txt'):     
            os.remove(file_path)
        #elif file_name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.jfif')):
            #shutil.move(file_path, dst_folder)
import os

def delete_txt_without_corresponding_image(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.jfif', '.webp']
    
    # Get all filenames in the folder
    all_files = os.listdir(folder_path)

    # Filter txt and image files
    txt_files = [f for f in all_files if f.endswith('.txt')]
    image_files = [f for f in all_files if os.path.splitext(f)[1].lower() in image_extensions]

    # Remove file extension from image filenames
    image_files_without_ext = [os.path.splitext(f)[0] for f in image_files]

    # Check for txt files without corresponding image and delete them
    for txt_file in txt_files:
        txt_file_without_ext = os.path.splitext(txt_file)[0]
        if txt_file_without_ext not in image_files_without_ext:
            os.remove(os.path.join(folder_path, txt_file))
            print(f"Deleted: {txt_file}")

if __name__ == "__main__":
    folder_path = r"C:\Users\metal\Downloads\sonic_training\datasets\gamma_train_set"
    delete_txt_without_corresponding_image(folder_path)

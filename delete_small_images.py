from PIL import Image
import os

# specify the path to the folder containing the images
folder_path = r"C:\Users\metal\gallery-dl\aesthetic_test\charlie_train_set"

# loop through all files in the folder
counter = 0
for filename in os.listdir(folder_path):
    # check if the file is an image (JPEG, PNG, etc.)
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.tfif'):
        # open the image file using Pillow
        img = Image.open(os.path.join(folder_path, filename))
        # get the dimensions of the image
        width, height = img.size
        img.close()
        # check if the image is smaller than 512 in either dimension
        if width < 768 or height < 768:
            # delete the image file
            image_path = os.path.join(folder_path, filename)
            os.remove(image_path)
            if os.path.exists(os.path.splitext(image_path)[0] + '.txt'):
                os.remove(os.path.splitext(image_path)[0] + '.txt')
            counter += 1

print(f"Deleted {counter} images")
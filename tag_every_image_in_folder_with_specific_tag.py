import os
from pathlib import Path

# Replace the path with the folder path where your images are located
folder_path = '/home/pablo/Downloads/Scourge the hedgehog-20230516T031200Z-001/Scourge the hedgehog/Masterpiece Quality'

# Replace the content of TAG variable with the desired text
TAG = 'Scourge the hedgehog'

def create_txt_file(image_path, tag):
    txt_path = image_path.with_suffix('.txt')
    with open(txt_path, 'w') as txt_file:
        txt_file.write(tag)

def main():
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

    for entry in os.scandir(folder_path):
        if entry.is_file() and entry.path.lower().endswith(image_extensions):
            create_txt_file(Path(entry.path), TAG)

if __name__ == '__main__':
    main()

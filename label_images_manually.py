import os
from tkinter import *
import shutil

from PIL import Image, ImageTk

from create_labels_json import check_for_tags, valid_image_extensions

def on_key_press(event):
    if event.keysym == 'Right':
        load_next_image()
    elif event.keysym == 'Left':
        load_prev_image()

def load_next_image():
    global current_image, active_tags
    current_image += 1
    if current_image >= len(image_files):
        current_image = 0
    load_image()
    active_tags = check_for_tags(os.path.splitext(image_files[current_image])[0] + '.txt')
    buttons_to_update = [button for button in root.children][2:]
    update_button_colors(buttons_to_update)

def update_button_colors(buttons_to_update):
    for button in buttons_to_update:
        button_text = root.children[button]['text']
        if button_text == 'Delete' or button_text == 'Move to classifier' or button_text == 'Toggle Tagless Mode':
            continue
        elif active_tags[button_text] == True:
            root.children[button].config(bg='green', relief=RAISED)
        else:
            root.children[button].config(bg='red', relief=RAISED)

def load_prev_image():
    global current_image, active_tags
    current_image -= 1
    if current_image < 0:
        current_image = len(image_files) - 1
    load_image()
    active_tags = check_for_tags(os.path.splitext(image_files[current_image])[0] + '.txt')
    buttons_to_update = [button for button in root.children][2:]
    update_button_colors(buttons_to_update)

def load_image():
    global current_image, image_files
    if len(image_files) == 0:  # Check if image_files is empty
        file_path_var.set("No images without tags were found.")  # Display a message to the user
        label.config(image=None)  # Clear the image label
        return  # Exit the function early
    image = Image.open(image_files[current_image])
    image = image.resize((800,800))
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo
    update_file_path()  # Call this to update the displayed file path

def update_file_path():
    global current_image, image_files, file_path_var
    file_path_var.set(image_files[current_image])

def on_button_press(button_text):
    global active_tags

    # Flip tag
    active_tags[button_text] = not active_tags[button_text] 


    # Prepare tags to write to label file
    tag_string = ""
    for key, value in active_tags.items():
        if value == True:
            tag_string += key
            tag_string += ", "

    # Update label file
    with open(os.path.splitext(image_files[current_image])[0] + '.txt', 'w', encoding="utf8") as file:
        tag_string = tag_string[:-1]
        file.write(tag_string)

    # Get button from button_text
    buttons  = [button for button in root.children][2:]
    button = None
    for b in buttons:
        if root.children[b]['text'].lower() == button_text.lower():
            button = root.children[b]
            break

    if button is None:
        print("This shouldnt happen...")
        quit()

    update_button_color(active_tags[button_text], button)

def update_button_color(color, button):
    if color:
        button.config(bg='green', relief=SUNKEN)
    else:
        button.config(bg='red', relief=RAISED)

def delete_image():
    global current_image
    os.remove(image_files[current_image])
    try:
        os.remove(os.path.splitext(image_files[current_image])[0] + '.txt') 
    except:
        pass
    load_next_image()
    image_files.pop(current_image-1)
    current_image -= 1

def move_to_classifier():
    global current_image
    shutil.copy(image_files[current_image], "/home/pablo/Documents/gallery-dl/deviantart/Tags_labeled_archive/from_charlie")  
    try:
        shutil.copy(os.path.splitext(image_files[current_image])[0] + '.txt', "/home/pablo/Documents/gallery-dl/deviantart/Tags_labeled_archive/from_charlie") 
    except:
        pass   

def filter_images_without_tags(image_files):
    filtered_images = []
    for image_file in image_files:
        tag_file = os.path.splitext(image_file)[0] + '.txt'
        if not os.path.exists(tag_file):
            filtered_images.append(image_file)
        else:
            with open(tag_file, 'r') as file:
                if file.read().strip() == "":
                    filtered_images.append(image_file)
    return filtered_images

def filter_mode():
    global image_files, current_image
    image_files = filter_images_without_tags(image_files)
    current_image = 0
    load_image()

def filter_images():
    global image_files, tagless_mode, original_image_files
    if tagless_mode:
        # Restore original list of image files
        image_files = original_image_files.copy()
        tagless_mode = False
    else:
        # Filter for images without tags
        image_files = [f for f in original_image_files if not has_tags(f)]
        tagless_mode = True

    # Reload current image
    load_image()

def has_tags(image_file):
    tag_file = os.path.splitext(image_file)[0] + '.txt'
    if not os.path.exists(tag_file):
        return False
    tags = check_for_tags(tag_file)

    # Check if all values in tags are False
    if any(tags.values()):
        return True
    else:
        return False


tagless_mode = False  # Add this before defining functions

folder = r"C:\Users\metal\Downloads\sonic_training\datasets\gamma_train_set"
image_files = [os.path.join(folder, f) for f in os.listdir(folder) if (f.lower().endswith('.jpg') or f.lower().endswith('.png') or f.lower().endswith('.jfif') or f.lower().endswith('.webp') or f.lower().endswith('.jpeg') or f.lower().endswith('.gif') or f.lower().endswith('.bmp'))]
image_files = sorted(image_files)
original_image_files = image_files.copy()

if not image_files:
    raise Exception('No images found in the specified folder.')

current_image = 0

root = Tk()
root.geometry('1000x1000')

file_path_var = StringVar() 
file_path_label = Label(root, textvariable=file_path_var)
file_path_label.grid(row=1, column=0, columnspan=8)

label = Label(root)
label.grid(row=2, column=0, sticky="N", columnspan=8)

active_tags = check_for_tags(os.path.splitext(image_files[current_image])[0] + '.txt')

row = 2
column = 1
for tag in active_tags.keys():
    button = Button(root, text=tag, command=lambda t=tag: on_button_press(t))
    if active_tags[tag] == True:
        button.config(bg='green', relief=RAISED)
    else:
        button.config(bg='red', relief=RAISED)
    if column < 8:
        button.grid(row=row, column=column, sticky="s")
        column += 1
    else:
        button.grid(row=row+1, column=0, sticky="S")
        row += 1
        column = 1

button = Button(root, text="Delete", command=delete_image)
button.config(bg='grey', relief=RAISED)
button.grid(row=row, column=column, sticky="S")
column += 1

button_move = Button(root, text="Move to classifier", command=move_to_classifier)
button_move.config(bg='pink', relief=RAISED)
button_move.grid(row=row, column=column, sticky="S")
column += 1  # Add a column counter

button_filter = Button(root, text="Toggle Tagless Mode", command=filter_images)
button_filter.config(bg='blue', relief=RAISED)
button_filter.grid(row=row, column=column, sticky="S")

load_image()

root.bind("<Key>", on_key_press)
root.mainloop()
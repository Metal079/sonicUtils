import os
from tkinter import *
import shutil

from PIL import Image, ImageTk

from create_labels_json import check_for_tags

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
    buttons_to_update = [button for button in root.children][1:]
    update_button_colors(buttons_to_update)

def update_button_colors(buttons_to_update):
    for button in buttons_to_update:
        if root.children[button]['text'] == 'Delete':
            continue
        elif active_tags[root.children[button]['text']] == True:
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
    buttons_to_update = [button for button in root.children][1:]
    update_button_colors(buttons_to_update)

def load_image():
    global current_image, image_files
    image = Image.open(image_files[current_image])
    image = image.resize((800,800))
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo

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
    buttons  = [button for button in root.children][1:]
    button = None
    for b in buttons:
        if root.children[b]['text'] == button_text:
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

def image_has_no_tags(image_path):
    txt_path = os.path.splitext(image_path)[0] + '.txt'
    if not os.path.exists(txt_path):
        return True
    with open(txt_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return len(content.strip()) == 0

folder = r"C:\Users\metal\Downloads\sonic_training\datasets\gamma_train_set"
image_files = [os.path.join(folder, f) for f in os.listdir(folder) if (f.endswith('.jpg') or f.endswith('.png')  or f.endswith('.jfif'))]
image_files = sorted(image_files)

# Filter image_files to keep only the images without tags
image_files = list(filter(image_has_no_tags, image_files))

current_image = 0

root = Tk()
root.geometry('1000x1000')
label = Label(root)
label.grid(row=0, column=0, sticky="N", columnspan=8)

# Get tags of current image
active_tags = check_for_tags(os.path.splitext(image_files[current_image])[0] + '.txt')

# Format buttons
color = True
row = 1
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

# button_move = Button(root, text="Move to classifier", command=move_to_classifier)
# button_move.config(bg='pink', relief=RAISED)
# button_move.grid(row=row, column=column, sticky="S")

load_image()

root.bind("<Key>", on_key_press)
root.mainloop()

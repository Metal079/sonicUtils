import os
import shutil
from tkinter import *
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
    global current_image, image_files, image_dir
    image = Image.open(image_files[current_image])
    image = image.resize((800,800))
    image_dir = image_files[current_image]
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo

def on_button_press(button_text):
    global image_dir

    # Copy image to appropriate folder
    #dest_dir_path = r"C:\Users\metal\gallery-dl\aesthetic\goodbad" + "\\" + button_text
    dest_dir_path = r"C:\Users\metal\gallery-dl\deviantart\Tags\mobian"
    shutil.copy(image_dir, dest_dir_path)
    with open(os.path.splitext(image_files[current_image])[0] + '.txt', 'w', encoding="utf8") as file:
        tag_string = 'mobian, '
        file.write(tag_string)
    shutil.copy(os.path.splitext(image_files[current_image])[0] + '.txt', dest_dir_path)

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

    update_button_color(False, button)

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

folder = r"C:\Users\metal\gallery-dl\aesthetic_test\good_marked"
#image_files = [os.path.join(folder, f) for f in os.listdir(folder) if (f.endswith('.jpg') or f.endswith('.png')  or f.endswith('.jfif'))]

image_files = []
for f in os.listdir(folder):
    if f.endswith('.jpg') or f.endswith('.png')  or f.endswith('.jfif'):
        if not os.path.exists(os.path.splitext(os.path.join(folder, f))[0] + '.txt'):
            image_files.append(os.path.join(folder, f))

current_image = 0

root = Tk()
root.geometry('1000x1000')
label = Label(root)
label.grid(row=0, column=0, sticky="N", columnspan=8)
load_image()

# Format buttons
color = True
row = 1
column = 1
categories = ['aesthetic', 'bad', 'idw']
for tag in categories:
    button = Button(root, text=tag, command=lambda t=tag: on_button_press(t))
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



root.bind("<Key>", on_key_press)
root.mainloop()

import os
from pathlib import Path
import copy


from create_labels_json import check_for_tags

def format_tag_file():
    formatted_text = []
    txt = Path(text_file_path).read_text()
    txt = txt.split(",")
    for index, word in enumerate(txt):
        txt[index] = word.strip()
        if txt[index] != '':
            formatted_text.append(txt[index])
    return formatted_text

remove_tags = {
    "common":['furry', "animal ears", "furry female", "furry male", "sideways mouth", "animal nose", "body fur", "no humans", 'tail'],
    "Rouge the bat":["white hair", "bat wings", "makeup", "blue eyes", "Rogue the bat", "wings"],
    "Blaze the cat": ["forehead jewel", "two-tone hair", "yellow eyes", "cat ears", "cat girl", "cat tail", "purple hair"],
    "Sally Acorn": ["blue eyes", "brown hair", "red hair", "two-tone fur"],
    "Tails the fox": ["multiple tails", "two tails", "blue eyes"],
    #"Whisper the wolf": [''],
    "Honey the cat": ["black hair"],
    "Sonic the hedgehog": ["green eyes"],
    "Amy Rose": ["green eyes", "pink fur", "pink skin"],
    "Tangle the lemur": ["grey fur", "multicolored fur", "white fur", "blue fur"]
    }

folder_path = r"/media/pablo/6ED0B21ED0B1EC89/Users/metal/Downloads/sonic_training/gallery-dl/aesthetic_test/charlie_train_set"

# Go through every txt file in given folder
for root, dir, files in os.walk(folder_path):
    for file_name in files:
        if file_name.endswith('.txt'):
            file_path = os.path.join(root, file_name)
            
            # Get existing tags in txt file
            image_tags = check_for_tags(file_path)
            found_tags = [tag for tag in image_tags if image_tags[tag] == True]
            found_tags.append("common")

            text_file_path = os.path.splitext(file_path)[0] + ".txt"

            txt = format_tag_file()
            cleaned_text = copy.deepcopy(txt)
            for tag in txt:
                for character in found_tags:
                    try:
                        if tag in remove_tags[character]:
                            cleaned_text.remove(tag)
                            if tag == "Rogue the bat":
                                cleaned_text.append("Rouge the bat")
                    except:
                        #print(f"Didnt find {character} in remove_tags")
                        pass

            with open(text_file_path, 'w', encoding="utf8") as file:
                text_to_write = ""
                for tag in cleaned_text:
                    text_to_write += tag + ", "

                file.write(text_to_write)

print("Done!")


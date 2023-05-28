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
    "common":['furry', "animal ears", "furry female", "furry male", "sideways mouth", "animal nose", "body fur", "no humans", 'tail', "pokemon (creature)", "body fur", "colored skin"],
    "Rouge the bat":["white hair", "bat wings", "makeup", "blue eyes", "Rogue the bat", "wings", 'eyeshadow'],
    "Blaze the cat": ["forehead jewel", "two-tone hair", "yellow eyes", "cat ears", "cat girl", "cat tail", "purple hair"],
    "Sally Acorn": ["blue eyes", "brown hair", "red hair", "two-tone fur"],
    "Tails the fox": ["multiple tails", "two tails", "blue eyes"],
    #"Whisper the wolf": [''],
    "Honey the cat": ["black hair"],
    "Sonic the hedgehog": ["green eyes"],
    "Amy Rose": ["green eyes", "pink fur", "pink skin", "two-tone fur"],
    "Tangle the lemur": ["grey fur", "multicolored fur", "white fur", "blue fur"],
    "Nicole the Lynx": ["black hair", "dark skin", "dark-skinned female", "green eyes"],
    "Mina Mongoose": ["earrings", "multiple earrings", "two-tone fur", "purple hair", "whiskers"],
    "Metal Sonic": ["robot", "humanoid robot", "mecha"],
    "Rosemary Prower": ["red hair", "blue eyes"],
    "Fiona Fox": ["red hair", "red fur", "two-tone fur", "orange fur", "white fur"],
    "zoey the fox": ["bangs", "blue eyes", "two-tone fur", "yellow fur", "blonde hair"],
    "Jewel the beetle": ["wings", "blue hair", "purple eyes", "pink eyes"],
    "Sonia the hedgehog": ["two-tone fur", ],
    "Lupe the wolf": ["long hair", "snout", "two-tone hair", "aqua eyes", "blue eyes", "streaked hair", "multicolored hair", "grey hair", "black hair"],
    "Clover the pronghorn": ["snout", "green hair", "antlers", "purple eyes"],
    "Rosy the rascal": ["pink fur", "pink hair", "bangs", "two-tone fur"],
    "Eggman": ["bald", "mustache", "fat", "facial hair", "sunglasses", "goggles", "round eyewear", "fat man"],
    "Shadow the hedgehog": ["red eyes"],
    "Ray the flying squirrel": ["yellow fur"],
    "Scourge the hedgehog": ["blue eyes", "green fur", "sharp teeth", "scar"],
    }

folder_path = r"/home/pablo/Downloads/Sally-20230515T043854Z-001/Sally/Normal Quality"

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


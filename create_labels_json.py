import os
import json

folder_path = r'/media/pablo/6ED0B21ED0B1EC89/Users/metal/Downloads/sonic_training/deviantart/Tags_labeled_archive'

tails_tags = ["tails_the_fox", "tailsthefox", "tailsmilesprower", "tails", "milesprower", "milestailsprower", "miles_tails_prower", "Tails the fox"]
amy_tags = ["amyrose", "amy", "amy_rose", "amyrosethehedgehog", "Amy Rose"]
knuckles_tags = ["knuckles", "knuckles_the_edchidna", "knucklestheechidna", "Knuckles the echidna"]
whisper_tags = ["whisper_the_wolf", "whisperthewolf", "whisper", "Whisper the wolf"]
rouge_tags = ["rouge_the_bat", "rougethebat", "rouge", "Rogue the bat", "Rouge the bat"]
silver_tags = ["silver_the_hedgehog", "silverthehedgehog", "silver", "Silver the hedgehog"]
blaze_tags = ["blaze_the_cat", "blazethecat", "blaze", "Blaze the cat"]
vanilla_tags = ["vanilla_the_rabbit", "vanillatherabbit", "vanilla", "Vanilla the rabbit"]
cream_tags = ["creamtherabbit", "cream_the_rabbit", "cream", "Cream the rabbit"]
shadow_tags = ["shadow_the_hedgehog", "shadowthehedgehog", "shadow", "Shadow the hedgehog"]
sonic_tags = ["sonic_the_hedgehog", "Sonic the hedgehog"]
sally_tags = ["sallyacorn", "princesssally", "princess_sally", "Sally Acorn"]
tangle_tags = ["tangle_the_lemur", "tanglethelemur", "Tangle the lemur"]
mobian_tags = ['sonicOC', 'OC', "sonic_oc", "mobian"]
cosmo_tags = ["cosmotheseedrian", "cosmo", "Cosmo the seedrian"]
big_the_tags = ["bigthecat", "big_the_cat", "big", "Big the cat"]
sticks_tags = ["sticksthebadger", "sticks_the_badger", "sticks", "Sticks the badger"]
tikal_tags = ["tikal_the_echidna", "tikaltheechidna", "tikal", "Tikal the echidna"]
wave_tags = ["wave_the_swallow", "wavetheswallow", "wave", "Wave the swallow"]
jet_tags = ["jetthehawk", "jet_the_hawk", "jet", "Jet the hawk"]
honey_tags = ["honeythecat", "honey_the_cat", "honey", "Honey the cat"]
surge_tags = ["surgethetenrec", "surge_the_tenrec", "surge", "Surge the tenrec"]
starline_tags = ["starlinetheplatypus", "starline", "starline_the_platypus", "Starline the platypus"]
mighty_tags = ["mightythearmadillo", "mighty_the_armadillo", "mighty", "Mighty the armadillo"]
vector_tags = ["vector", "vectorthecrocodile", "vector_the_crocodile", "Vector the crocodile"]
charmy_tags = ["charmy", "charmythebee", "charmy_the_bee", "charmythebee", "charmy_the_bee", "Charmy the bee"]
espio_tags = ["espio", "espiothechameleon", "espio_the_chameleon", "Espio the chameleon"]
eggman_tags = ["Eggman"]
Bunnierabbot_tags = ["bunnierabbot", "bunnie_rabbot", "bunnie", "Bunnie Rabbot"]
marine_tags = ["marinetheraccoon", "marine_the_raccoon", "marine", "Marine the Raccoon"]
storm_tags = ["stormthealbatross", "storm", "storm_the_albatross", "Storm the albatross"]
maria_tags = ["mariarobotnik", "maria_robotnik", "maria", "Maria Robotnik"]
# super_form_tags = ['super', 'super form']
nicole_tags = ["Nicole_the_lynx", 'Nicole', 'Nicole the Holo-Lynx', 'Nicole the Lynx']
lanolin_tags = ["Lanolin the sheep"]
metal_sonic_tags = ["Metal Sonic"]
shard_the_metal_Sonic = ["Shard the metal Sonic"]
mina = ["Mina Mongoose"]
shade = ["Shade the echidna"]
barby_the_koala = ["Barby the koala"]
Breezie_the_hedgehog = ["Breezie the hedgehog"]
Clove_the_pronghorn = ["Clove the Pronghorn"]
Fiona_fox = ["Fiona Fox"]
Hershey_the_cat = ["Hershey the cat"]
Jewel_the_beetle = ["Jewel the beetle"]
Julie_su = ["Julie-Su"]
Lara_Su = ["Lara-Su"]
Lien_Da = ["Lien-Da"]
Lupe_the_wolf = ["Lupe the wolf"]
Nack_the_weasel = ["Nack the Weasel, Fang the sniper"]
Ray_the_flying_squirrel = ["Ray the flying squirrel"]
Rosemary_prower = ["Rosemary Prower"]
Rosy_the_rascal = ["Rosy the rascal"]
Sonia_the_hedgehog = ["Sonia the hedgehog"]
zoey_the_fox = ["Zoey the fox"]
Scourge_the_hedgehog = ["Scourge the hedgehog"]


Ratchet = ["Ratchet"]
Clank = ["Clank"]
rivet = ["Rivet"]

all_tags = [tails_tags,
            amy_tags,
            knuckles_tags,
            whisper_tags,
            rouge_tags,
            silver_tags,
            blaze_tags,
            vanilla_tags,
            cream_tags,
            shadow_tags,
            sonic_tags,
            sally_tags,
            tangle_tags,
            mobian_tags,
            cosmo_tags,
            big_the_tags,
            sticks_tags,
            tikal_tags,
            wave_tags,
            jet_tags,
            honey_tags,
            surge_tags,
            starline_tags,
            mighty_tags,
            vector_tags,
            charmy_tags,
            espio_tags,
            eggman_tags,
            Bunnierabbot_tags,
            marine_tags,
            storm_tags,
            maria_tags,
            # super_form_tags,
            nicole_tags,
            lanolin_tags,
            metal_sonic_tags,
            shard_the_metal_Sonic,
            mina,
            shade,
            barby_the_koala,
            Breezie_the_hedgehog,
            Clove_the_pronghorn,
            Fiona_fox,
            Hershey_the_cat,
            Jewel_the_beetle,
            Julie_su,
            Lara_Su,
            Lien_Da,
            Lupe_the_wolf,
            Nack_the_weasel,
            Ray_the_flying_squirrel,
            Rosemary_prower,
            Rosy_the_rascal,
            Sonia_the_hedgehog,
            Ratchet,
            Clank,
            zoey_the_fox,
            rivet,
            Scourge_the_hedgehog
            ]
tags_list = [list[-1] for list in all_tags] # String list of last string of all list above (for class names)
character_tag_count = {tag:0 for tag in tags_list} # To track how many of each class is found

def main():
    files_written = 0
    for root, dir, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                tags_found = check_for_tags(file_path)

                # Prepare tags to write to file
                tag_string = ""
                for key, value in tags_found.items():
                    if value == True:
                        tag_string += key
                        tag_string += ", "

                # Write to tag file
                # with open(file_path, 'w', encoding="utf8") as file:
                #     tag_string = tag_string[:-1]
                #     file.write(tag_string)
                #     files_written += 1

                json_formated = {}
                
                complete_tag_list = [tag for tag in tags_list]
                
                found_tags_list = []
                for tag in complete_tag_list:
                    if tags_found[tag] == True:
                        character_tag_count[tag] += 1
                        found_tags_list.append(1)
                    else:
                        found_tags_list.append(0)

                if os.path.exists(os.path.splitext(file_path)[0] + ".jpg"):
                    image_path = os.path.splitext(file_path)[0] + ".jpg"
                elif os.path.exists(os.path.splitext(file_path)[0] + ".png"):
                    image_path = os.path.splitext(file_path)[0] + ".png"
                elif os.path.exists(os.path.splitext(file_path)[0] + ".jfif"):
                    image_path = os.path.splitext(file_path)[0] + ".jfif"
                else:
                    print(f"Error, cannot find: {os.path.splitext(file_path)[0]}")

                json_formated = {"image": image_path,
                                "labels": found_tags_list}
                json_data = json.dumps(json_formated)

                # Writing to json
                with open(folder_path + '/train.json', "a") as outfile:
                    outfile.write(json_data)

    print(f"Done! tags files changed: {files_written}")
    print(character_tag_count)

def check_for_tags(file_path):
    tags_found = {tag:False for tag in tags_list}

   # If .txt file doesnt exist just return default dictionary
    if not os.path.exists(os.path.splitext(file_path)[0] + '.txt'):
        print(f"Corresponding .txt file not found for image {os.path.splitext(file_path)[0]}")
        return tags_found

    with open(os.path.splitext(file_path)[0] + '.txt', 'r', encoding="utf8") as file:
        image_tag = file.read()

         # Check for tags in file
        for i, tag_list in enumerate(all_tags):
            for tag in tag_list:
                if tag.upper() in image_tag.upper():
                    tags_found[tags_list[i]] = True
                    break

    return tags_found

if __name__ == '__main__':
    main()
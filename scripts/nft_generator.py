

############################## User parameters ######################################

# 1 :__________ Number of Combinations ___________#

# number_of_combinations = 2  # 250

# 2 : _________ image dimentions in pixel  ________#
# let it None if you want to save the default size



######################## CUSTUM FEATURES ################
# ______________ foler names  __________________#
# if you don't to apply the percentages , let it 'none' for the folder name
# body, clothes and skin


body_folder_name = 'None'
skin_folder_name = 'None'
clothes_folder_name = 'None'
# Caps and Hair
hair_folder_name = 'None'
caps_folder_name = 'None'
# acccessories
accessories_folder_name = 'None'
# ears
ears_folder_name = '02.Rare Background'
# hat
hat_folder_name = 'None'
# neck
neck_folder_name = '09.Head'

######################################################################################


######## WARINIG : Don't change anything bellow this line , otherwise the code can be crashed.

import os
from PIL import Image
import re
import simplejson
import random
import sys
from math import ceil
import json

# default_params_dict = {
#     "collection_name": ["None"], "collection_description": ["None"], "number_of_combinations": ["5"],
#     "width": ["512"], "height": ["512"]
# }
#
# default_rarity_setting_dict = {
#     "body_only": 100,
#     "body_skin_clothes": 100,
#     "skin_body_without_clothes": 100,
#     "hair_only": 100,
#     "caps_only": 100,
#     "no_hair_no_caps": 100,
#     "hat": 100,
#     "accessories": 100,
#     "ears": 100,
#     "neck": 100
# }
#
# with open('rarity.json', 'w') as file:
#     json.dump(default_rarity_setting_dict, file)
#
# with open('params.json', 'w') as file:
#     json.dump(default_params_dict, file)


with open("params.json", "r") as read_file:
    params_data = json.load(read_file)
    print(params_data)

with open('rarity.json', 'r') as read_file:
    rarity_data = json.load(read_file)
    print(rarity_data)
    try:
        for i in rarity_data:
            for j in rarity_data[i]:
                rarity_data[i] = int(j)
    except TypeError:
        print(rarity_data)

number_of_combinations = int(params_data['number_of_combinations'][0])
weight = int(params_data['width'][0])
height = int(params_data['height'][0])

# 3 : _________ layer of rarity (special edition SE) ________#
SE_folder_name = '12.Special Edition [se]'

# 4 : _________ about the collection for the metada file ______________#

collection_name = params_data['collection_name'][0]
collection_description = params_data['collection_description'][0]

try:
    body_only = rarity_data['body_only']
    body_skin_clothes = rarity_data['body_skin_clothes']
    skin_body_without_clothes = rarity_data['skin_body_without_clothes']
    # Caps and hair
    hair_only = rarity_data['hair_only']
    caps_only = rarity_data['caps_only']
    no_hair_no_caps = rarity_data['no_hair_no_caps']
    # Accessories and Ears
    hat = rarity_data['hat']
    accessories = rarity_data['accessories']
    ears = rarity_data['ears']
    # Neck
    neck = rarity_data['neck']
except KeyError:
    body_only = 100
    body_skin_clothes = 100
    skin_body_without_clothes = 100
    # Caps and hair
    hair_only = 100
    caps_only = 100
    no_hair_no_caps = 100
    # Accessories and Ears
    hat = 100
    accessories = 100
    ears = 100
    # Neck
    neck = 100

pattern = re.compile(r"^\d+\.")
body_folder_name = pattern.sub("" ,body_folder_name).strip().lower()
skin_folder_name = pattern.sub("" ,skin_folder_name).strip().lower()
clothes_folder_name = pattern.sub("" ,clothes_folder_name).strip().lower()

hair_folder_name = pattern.sub("" ,hair_folder_name).strip().lower()
caps_folder_name = pattern.sub("" ,caps_folder_name).strip().lower()

accessories_folder_name = pattern.sub("" ,accessories_folder_name).strip().lower()
ears_folder_name = pattern.sub("" ,ears_folder_name).strip().lower()
hat_folder_name =pattern.sub('' ,hat_folder_name).strip().lower()

neck_folder_name = pattern.sub("" ,neck_folder_name).strip().lower()

SE_folder_name   = pattern.sub("" ,SE_folder_name).strip().lower()



## Body and Clothes
body_only_number = ceil((body_only /100 ) *number_of_combinations)
body_skin_clothes_number = ceil((body_skin_clothes /100 ) *number_of_combinations)
skin_body_without_clothes_number = ceil((skin_body_without_clothes /100 ) *number_of_combinations)
## Caps and hair
hair_only_number = ceil((hair_only /100 ) *number_of_combinations)
caps_only_number = ceil((caps_only /100 ) *number_of_combinations)
no_hair_no_caps_number = ceil((no_hair_no_caps /100 ) *number_of_combinations)
## Accessories and Ears
accessories_number = ceil((accessories /100 ) *number_of_combinations)
ears_number = ceil((ears /100 ) *number_of_combinations)
hat_number =ceil((hat /100 ) *number_of_combinations)
## Neck
neck_number = ceil((neck /100 ) *number_of_combinations)
## Special Edition
# Special Edition
SE = 20
SE_number = ceil((SE /100 ) *number_of_combinations)

# List
## Body and Clothes
body_only_counter = 0
body_skin_clothes_counter = 0
skin_body_without_clothes_counter = 0
## Caps and hair
hair_only_counter = 0
caps_only_counter = 0
no_hair_no_caps_counter = 0
## Accessories and Ears
accessories_counter = 0
ears_counter = 0
hat_counter = 0
## Neck
neck_counter = 0
## Special Edition
SE_counter = 0

## idx for starting spe
spe_idx = 0
extracted_data = []

# conter
cont_bd_sk_cl = 0
cont_bd_sk = 0
# already taken SE
already_picked_SE = []
def check_paths():
    if not os.path.exists('Output'):
        os.mkdir('Output')
    if not os.path.exists('Output/generated_images') :
        os.mkdir('Output/generated_images')
    if not os.path.exists('Output/meta_data'):
        os.mkdir('Output/meta_data')
    if not os.path.exists('Output/_metadata'):
        os.mkdir('Output/_metadata')


# global metadata file
# global_metada_data = []
def make_art() :
    check_paths()
    pattern = re.compile(r"^\d+\.")
    while len(extracted_data) < number_of_combinations :
        make_unique_combinaison()
    print("------- Extracted data ---------->" ,len(extracted_data))
    for j ,unique_merged_img in enumerate(extracted_data)  :
        # print(unique_merged_img)
        is_SE = False
        meta_data ={}
        attributes = []
        merged_img = Image.open(unique_merged_img[0]).convert('RGBA')
        merged_img_layer_name = os.path.split(os.path.split(unique_merged_img[0])[0])[1]
        merged_img_layer_name = pattern.sub("", merged_img_layer_name).strip()
        attributes.append({'trait_type': merged_img_layer_name,
                           'value': os.path.split(unique_merged_img[0])[1].split(".")[0]})
        if SE_folder_name in merged_img_layer_name.lower():
            is_SE = True
        for i in range(1, len(unique_merged_img)):
            try:
                merged_img_layer_name = os.path.split(os.path.split(unique_merged_img[i])[0])[1]
                merged_img_layer_name = pattern.sub("", merged_img_layer_name).strip()
                attributes.append({'trait_type': merged_img_layer_name,
                                   'value': os.path.split(unique_merged_img[i])[1].split(".")[0]})
                if SE_folder_name in merged_img_layer_name.lower():
                    is_SE = True
            except:
                print("------- error -------")
                print(i)
                print(unique_merged_img)
                sys.exit()
            imgg = Image.open(unique_merged_img[i]).convert('RGBA')
            merged_img = Image.alpha_composite(merged_img, imgg)
        # print(unique_merged_img[i])
        if not is_SE:
            meta_data['name'] = f"{collection_name} {j + 1}"
        else:
            meta_data['name'] = f"{collection_name} SE-{j + 1}"
        meta_data['description'] = collection_description
        meta_data['tokenID'] = f"{j + 1}"
        meta_data['attributes'] = attributes
        # save the image and its metadata
        if not is_SE:
            export_path_for_meta_data = os.path.join('Output', 'meta_data', f'{j + 1}.json')
            export_path_for_image = os.path.join('Output', 'generated_images', f'{j + 1}.png')
            if weight and height:
                try:
                    merged_img.resize((weight, height)).save(export_path_for_image, format="png")
                except:
                    print("Image--Dim 1")
            else:
                merged_img.save(export_path_for_image, format="png")
            with open(export_path_for_meta_data, 'w') as f:
                f.write(simplejson.dumps(meta_data, indent=4, sort_keys=True))
        else:
            export_path_for_image = os.path.join('Output', 'generated_images', f'{j + 1}-SE.png')
            export_path_for_meta_data = os.path.join('Output', 'meta_data', f'{j + 1}-SE.json')
            if weight and height:
                try:
                    merged_img.resize((weight, height)).save(export_path_for_image, format="png")
                except:
                    print("Image--Dim 1")
            else:
                merged_img.save(export_path_for_image, format="png")
            with open(export_path_for_meta_data, 'w') as f:
                f.write(simplejson.dumps(meta_data, indent=4, sort_keys=True))
        # write to _metadata
        export_path_for_meta_data_global = os.path.join(os.getcwd(), 'Output', '_metadata', '_metadata.json')
        with open(export_path_for_meta_data_global, 'a') as f:

            f.write(f"{simplejson.dumps(meta_data, indent=4)}")
            if j < len(extracted_data) - 1:
                f.write(",")
            f.write("\n")
        merged_img = None
        print(j)


def get_sp_idx():
    if SE < 50:
        return random.randint(0, number_of_combinations // 2)
    elif (SE > 50) and (SE < 70):
        return random.randint(0, number_of_combinations // 4)
    elif (SE > 70) and (SE < 80):
        return random.randint(0, number_of_combinations // 6)
    return 0


def check_percentage_condition(body_only_counter, body_skin_clothes_counter, skin_body_without_clothes_counter,
                               accessories_counter, ears_counter, neck_counter, SE_counter):
    return (body_only_number <= body_only_counter) and (body_skin_clothes_number <= body_skin_clothes_counter) and (
                skin_body_without_clothes_number <= skin_body_without_clothes_counter) and (
                       accessories_number <= accessories_counter) and (ears_number <= ears_counter) and (
                       neck_number <= neck_counter) and (SE_number <= SE_counter)


def make_unique_combinaison():
    global spe_idx
    ##  body and clothes
    global body_only_counter
    global body_skin_clothes_counter
    global skin_body_without_clothes_counter
    ## accessories and ears
    global accessories_counter
    global ears_counter
    ## neck
    global neck_counter
    # hat
    global hat_counter
    # counter
    global cont_bd_sk_cl
    global cont_bd_sk
    # hair and cap
    global hair_only_counter
    global caps_only_counter
    global no_hair_no_caps_counter
    # already exist SE
    global already_picked_SE
    all_layers = sorted(os.listdir(os.path.join(os.getcwd(), 'media/Input')))
    all_images_of_each_layers = []
    for layer in all_layers:
        layer_path = os.path.join(os.getcwd(), 'media/Input', layer)
        layer_images_name = os.listdir(layer_path)
        all_layer_images_path = [os.path.join(layer_path, img) for img in layer_images_name]
        all_layer_images_path = sorted(all_layer_images_path)
        all_images_of_each_layers.append(all_layer_images_path)

    unique_combainaison = []
    spe_idx += 1
    while 1:
        for layer in all_images_of_each_layers:
            print(layer)
            random_img = layer[random.randint(0, len(layer) - 1)]
            folder_info = os.path.split(random_img)[0].lower()
            folder_info = os.path.split(folder_info)[1]
            ## body and clothes
            if (body_only) and (body_folder_name in folder_info) and (body_only_number > body_only_counter):
                body_only_counter += 1
                unique_combainaison.append(random_img)
            elif (body_only_counter >= body_only_number) and (body_skin_clothes) and (
                    (body_folder_name in folder_info) or (clothes_folder_name in folder_info) or (
                    skin_folder_name in folder_info)) and (body_skin_clothes_number > body_skin_clothes_counter):
                cont_bd_sk_cl += 1
                if cont_bd_sk_cl == 3:
                    cont_bd_sk_cl = 0
                    body_skin_clothes_counter += 1
                unique_combainaison.append(random_img)
            elif (body_skin_clothes_counter >= body_skin_clothes_number) and (skin_body_without_clothes) and (
                    (body_folder_name in folder_info) or (skin_folder_name in folder_info)) and (
                    skin_body_without_clothes_number > skin_body_without_clothes_counter):
                # (body_skin_clothes_counter>=body_skin_clothes_number) and
                if cont_bd_sk == 2:
                    cont_bd_sk = 0
                    skin_body_without_clothes_counter += 1
                unique_combainaison.append(random_img)
            # hat
            elif (hat) and (hat_folder_name in folder_info) and (hat_number > hat_counter):
                hat_counter += 1
                unique_combainaison.append(random_img)
                # caps and hair
            elif (hair_folder_name in folder_info) and (hair_only_counter < hair_only_number):
                hair_only_counter += 1
                unique_combainaison.append(random_img)
            elif (hair_only_counter >= hair_only_number) and (caps_folder_name in folder_info) and (
                    caps_only_counter < caps_only_number):
                caps_only_counter += 1
                unique_combainaison.append(random_img)
            elif ((hair_folder_name in folder_info) or (caps_folder_name in folder_info)) and (
                    hair_only_counter >= hair_only_number) and (caps_only_counter >= caps_only_number) and (
                    no_hair_no_caps_counter < no_hair_no_caps_number * 2):
                no_hair_no_caps_counter += 1
            elif (no_hair_no_caps_counter >= no_hair_no_caps_number) and (
                    (hair_folder_name in folder_info) or (caps_folder_name in folder_info)):
                unique_combainaison.append(random_img)
            ## Ears and Accessories
            elif (accessories) and (accessories_folder_name in folder_info) and (
                    accessories_number > accessories_counter):
                accessories_counter += 1
                unique_combainaison.append(random_img)
            elif (accessories_counter >= accessories_number) and (ears) and (ears_folder_name in folder_info) and (
                    ears_number > ears_counter):
                ears_counter += 1
                unique_combainaison.append(random_img)
                ## neck
            elif (neck) and (neck_folder_name in folder_info) and (neck_number > neck_counter):
                neck_counter += 1
                unique_combainaison.append(random_img)
                ## SE
            elif (SE) and (get_sp_idx() >= spe_idx) and (SE_folder_name in folder_info) and (
                    random_img not in already_picked_SE):

                already_picked_SE.append(random_img)
                unique_combainaison.append(random_img)
            elif (body_folder_name not in folder_info) and (hat_folder_name not in folder_info) and (
                    hair_folder_name not in folder_info) and (caps_folder_name not in folder_info) and (
                    neck_folder_name not in folder_info) and (ears_folder_name not in folder_info) and (
                    accessories_folder_name not in folder_info) and (clothes_folder_name not in folder_info) and (
                    skin_folder_name not in folder_info) and (SE_folder_name not in folder_info):
                unique_combainaison.append(random_img)
                # check_percentage_condition(body_only_counter,body_skin_clothes_counter,skin_body_without_clothes_counter,accessories_counter,ears_counter,neck_counter,SE_counter)
        if unique_combainaison not in extracted_data:
            extracted_data.append(unique_combainaison)
            break
        unique_combainaison = []


if __name__ == '__main__':
    check_paths()
    export_path_for_meta_data_global = os.path.join(os.getcwd(), 'Output', '_metadata', '_metadata.json')
    with open(export_path_for_meta_data_global, 'a') as f:
        f.write('[\n')
    make_art()
    with open(export_path_for_meta_data_global, 'a') as f:
        f.write(']')




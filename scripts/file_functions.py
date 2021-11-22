from pathlib import Path
from brownie import network
import os
import json
import random

from scripts.helpful_scripts import is_mainnet


NFT_IMAGES_DIR = "./img/gif/"


def clean_directory():
    dir = "./tokens_to_upload/" + network.show_active() + "/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dirs = "./metadata/" + network.show_active() + "/"
    for dir in os.listdir(dirs):
        if os.path.isdir(dir):
            os.remove(os.path.join(dirs, dir))


def get_character_name(index):
    dir_path = NFT_IMAGES_DIR
    image_file_name = os.listdir(dir_path)[index]
    character_file_name = remove_extension(image_file_name)
    full_file_path = dir_path + image_file_name
    return (character_file_name, full_file_path)


def get_any_character():
    list_of_images = os.listdir(NFT_IMAGES_DIR)
    image_file_name = random.choice(list_of_images)
    return get_character_name(list_of_images.index(image_file_name))


def move_to_used(character_file_name):
    if is_mainnet():
        old_path = f"{NFT_IMAGES_DIR}{character_file_name}.gif"
        new_path = f"./img/used_gifs/{character_file_name}.gif"
        os.rename(old_path, new_path)


def move_used_img_back():
    if is_mainnet():
        for f in os.listdir("./img/used_gifs/"):
            old_path = f"./img/used_gifs/{f}"
            new_path = f"{NFT_IMAGES_DIR}{f}"
            os.rename(old_path, new_path)


def remove_extension(file_name):
    return os.path.splitext(file_name)[0]


def update_prompts(prompt_used, test_mode=False):
    if network.show_active() == "mainnet" or test_mode:
        filepath = None
        if test_mode:
            filepath = f"./metadata/TEST_used_prompts.json"
        else:
            filepath = f"./metadata/used_prompts.json"
        file_data = None
        with open(filepath, "rb") as file:
            file_data = json.load(file)
        file_data.append(prompt_used)
        with open(filepath, "w") as file:
            json.dump(file_data, file, sort_keys=True, indent=4)


def update_group_uris(group_uri, cid):
    filepath = f"./metadata/network_to_cid.json"
    group_uri = str(group_uri)
    data = None
    with open(filepath, "rb") as file:
        data = json.load(file)
    with open(filepath, "w") as file:
        data[network.show_active()]["group_uris"][group_uri] = cid
        json.dump(data, file, sort_keys=True, indent=4)


def read_group_uris():
    filepath = f"./metadata/network_to_cid.json"
    with open(filepath, "rb") as file:
        data = json.load(file)
        return data[network.show_active()]["group_uris"]


def update_edition(edit):
    filepath = f"./metadata/network_to_cid.json"
    data = None
    with open(filepath, "rb") as file:
        data = json.load(file)
    with open(filepath, "w") as file:
        data[network.show_active()]["current_edition"] = edit
        json.dump(data, file, sort_keys=True, indent=4)


def read_edition():
    filepath = f"./metadata/network_to_cid.json"
    with Path(filepath).open("rb") as fp:
        return json.load(fp)[network.show_active()]["current_edition"]


def update_dictionary(new_dictionary):
    dump_location = f"./metadata/{network.show_active()}/token_dictionary.json"
    with open(dump_location, "w") as file:
        json.dump(new_dictionary, file, sort_keys=True, indent=4)


def read_dictionary():
    filepath = f"./metadata/{network.show_active()}/token_dictionary.json"
    with Path(filepath).open("rb") as fp:
        return json.load(fp)


def update_archived_tokens(new_dictionary):
    dump_location = f"./metadata/{network.show_active()}/archived_tokens.json"
    with open(dump_location, "w") as file:
        json.dump(new_dictionary, file, sort_keys=True, indent=4)


def read_archived_tokens():
    filepath = f"./metadata/{network.show_active()}/archived_tokens.json"
    with Path(filepath).open("rb") as fp:
        return json.load(fp)


def rename_gifs(character_names):
    count = 0
    dir_path = NFT_IMAGES_DIR
    for file in os.listdir(dir_path):
        os.rename(
            dir_path + file,
            dir_path + character_names[count].replace(" ", "_") + ".gif",
        )
        count = count + 1


def number_of_gifs():
    return len(os.listdir(NFT_IMAGES_DIR))

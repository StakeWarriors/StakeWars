import os
import json
from dotenv import load_dotenv


from scripts.file_functions import number_of_gifs, rename_gifs
from scripts.ipfs_functions import upload_to_ipfs_client
from metadata.template_metadata import metadata_template
from scripts.ipfs_rarity.colors import create_variant
from scripts.ipfs_rarity.name_generator import fantasy_name

load_dotenv()


def rename_gif_files():
    numOfGifs = number_of_gifs()
    characterNames = []
    for i in range(numOfGifs):
        characterNames.append(fantasy_name())
    rename_gifs(characterNames)


def make_variants():
    dir_path = "./img/gif/"
    tmp_dir_path = "./img/tmp_gif/"
    for file in os.listdir(dir_path):
        for i in range(6):
            og_file_path = dir_path + file
            new_file_path = tmp_dir_path + fantasy_name().replace(" ", "_") + ".gif"
            create_variant(og_file_path, new_file_path, i)
    # for file in os.listdir(tmp_dir_path):
    #     os.rename(tmp_dir_path + file, dir_path + file)


def get_size(start_path="./img/tmp_gif/"):
    total_size = 0
    breeds = set()
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                breeds.add(os.path.getsize(fp))
    print(f"{len(breeds)} ==> {breeds}")


def create_default_art():
    (base_uri, full_uri) = upload_to_ipfs_client(
        1,
        "StakeWarsPreReleaseCoverArt.png",
        "./img/png/StakeWarsPreReleaseCoverArt.png",
    )
    metadata_file_name = f"./metadata/StakeWarsPreReleaseCoverArt.json"
    metadata_template["name"] = "Stake Wars PreRelease Cover Art"
    metadata_template[
        "description"
    ] = "This cover art will be replace when these NFTs are released with a unique character, that will have a variety of traits and characteristics."
    metadata_template["image"] = full_uri
    with open(metadata_file_name, "w") as file:
        json.dump(metadata_template, file)
    (base_uri, full_uri) = upload_to_ipfs_client(
        1, "StakeWarsPreReleaseCoverArt.json", metadata_file_name
    )


def main():
    get_size()

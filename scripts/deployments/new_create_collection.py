from brownie import StakeWarsFactoryUpgradable, StakeWarsInternals, Contract, network
from dotenv import load_dotenv
from copy import deepcopy
import json
import os

from scripts.deployments.stakewars_helper import (
    archive_tokens_to_metadata,
    toClassEnglish,
    toLandEnglish,
    toRarityEnglish,
)
from scripts.helpful_scripts import get_account
from metadata.template_metadata import metadata_template
from scripts.file_functions import (
    NFT_IMAGES_DIR,
    get_any_character,
    move_to_used,
    read_address,
    read_dictionary,
    update_dictionary,
    update_group_uris,
)
from scripts.ipfs_rarity.colors import get_traits
from scripts.ipfs_rarity.name_generator import character_bios
from scripts.ipfs_rarity.size import get_creature_name
from scripts.pinata import (
    get_file_pinata_client,
    upload_pinata,
)

load_dotenv()


def create_collection(account=None):
    account = account if account else get_account()
    stake_wars = read_address(
        "StakeWarsFactoryUpgradableProxy", StakeWarsFactoryUpgradable
    )
    numOwnedWarriors = stake_wars.warriorsToBeDetailedLength()
    SECRET = os.getenv("SECRET_LARGE_PRODUCT")
    tokens = []

    uri_group = -1
    # Solely Create Metadata
    super_rare_counter = 0
    rare_counter = 0
    bios_counter = 0
    print(f"Creating {numOwnedWarriors} Collections")
    for warriorIndex in range(numOwnedWarriors):
        warrior = stake_wars.warriorsToBeDetailed(warriorIndex)
        character = Contract.from_abi(
            StakeWarsInternals._name, warrior, StakeWarsInternals.abi
        )

        tokenId = character.tokenId()
        edition = character.edition()
        uri_group = character.uriGroup()

        (rarity_number, rarity_index) = character.getRarity(SECRET, {"from": account})
        rarity_name = toRarityEnglish(rarity_number)
        clazz = toClassEnglish(character.clazz(0))
        land = toLandEnglish(character.land(0))
        (character_file_name, full_file_path) = get_any_character()

        character_name = character_file_name.replace("_", " ")
        (bios, bios_counter, super_rare_counter, rare_counter) = character_bios(
            bios_counter,
            rare_counter,
            super_rare_counter,
            rarity_number,
            character_name,
            clazz,
            land,
        )

        token = deepcopy(metadata_template)
        token["name"] = character_name
        token["tokenId"] = tokenId
        token["description"] = (
            """# Character Bio:<br />
"""
            + bios
            + """
            """
            + token["description"]
        )
        token["image"] = get_file_pinata_client(
            character_file_name + ".gif",
            "QmTr8HW2etSPQrhhpEetn8wcFw9CzLmNpNngYWcK6K54Tf",  # Photo Gallary
        )
        token["attributes"][0]["value"] = edition
        token["attributes"][1]["value"] = rarity_name
        token["attributes"][2]["value"] = rarity_number
        token["attributes"][3]["value"] = clazz
        token["attributes"][4]["value"] = land
        token["attributes"][5]["value"] = get_creature_name(full_file_path)
        traits = get_traits(NFT_IMAGES_DIR + character_file_name + ".gif")
        token["attributes"][6]["value"] = int(
            100 * (len(traits) / 13)
        )  # Hard-coded Max Value
        for trait in traits:
            token["attributes"].append(
                {"trait_type": "Personality Trait", "value": trait["field"]}
            )
            if trait["degree"] > 0:
                token["attributes"].append(
                    {"trait_type": trait["field"], "value": trait["degree"]}
                )

        # File Changes
        move_to_used(character_file_name)
        metadata_file_name = f"./tokens_to_upload/{network.show_active()}/"
        tokens.append(token)
        os.makedirs(metadata_file_name, exist_ok=True)
        with open(f"{metadata_file_name}{tokenId}.json", "w") as file:
            print("Storing Metadata File")
            json.dump(token, file, sort_keys=True, indent=4)
    return (tokens, uri_group)


def upload_collections():
    (tokens, uri_group) = create_collection()
    token_uris = []
    if len(tokens) == 0:
        return token_uris

    print(f"Uploading {len(tokens)} Collection(s)")
    cid = upload_pinata()["IpfsHash"]
    update_group_uris(uri_group, cid)

    # uriGroup
    for token in tokens:
        edition = token["attributes"][0]["value"]
        tokenId = token["tokenId"]
        old_path = f"./tokens_to_upload/{network.show_active()}/{tokenId}.json"
        new_path = f"./metadata/{network.show_active()}/ed.{edition}/"
        os.makedirs(new_path, exist_ok=True)
        os.rename(old_path, new_path + f"{tokenId}.json")
    archive_tokens_to_metadata(tokens)
    return token_uris


def save_collection():
    dictionary = read_dictionary()
    token_uris = upload_collections()
    print(f"Saving {len(token_uris)} Collection URIs")
    for token_uri in token_uris:
        dictionary.append(f"https://gateway.pinata.cloud/ipfs/{token_uri}")
    update_dictionary(dictionary)


def main():
    save_collection()

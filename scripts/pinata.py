import typing as tp
import os
import requests
from brownie import network, config
import json

from pinatapy import PinataPy

# from scripts.PyPinata import PinataPy
from scripts.helpful_scripts import is_local

PINATA_BASE_URL = "https://api.pinata.cloud/"
PINATA_PIN_API = "pinning/pinFileToIPFS"
PINATA_API_KEY = config["api"]["pinata"]["public"]
PINATA_SECRET_API_KEY = config["api"]["pinata"]["secret"]
headers = {
    "pinata_api_key": PINATA_API_KEY,
    "pinata_secret_api_key": PINATA_SECRET_API_KEY,
}


def upload_to_pinata(token, cid):
    if is_local():
        return
    token_id = token["tokenId"]
    uri = f"{cid}/{token_id}.json"
    response = requests.post(
        PINATA_BASE_URL + PINATA_PIN_API,
        files={"file": (uri, json.dumps(token))},
        headers=headers,
    )
    hash = response.json()["IpfsHash"]
    return (hash, uri)


def upload_dir_pinata(dir):
    pinata = PinataPy(PINATA_API_KEY, PINATA_SECRET_API_KEY)
    pinata.pin_file_to_ipfs(path_to_file=dir)


def gen_edition_cid(edition):
    if is_local():
        return
    response = requests.post(
        PINATA_BASE_URL + PINATA_PIN_API,
        files={
            "file": (
                f"{network.show_active()}_ed.{edition}/ReadMe.txt",
                "Thanks",
            )
        },
        headers=headers,
    )
    return response.json()["IpfsHash"]


def get_file_pinata_client(
    file_name="",
    folder_cid="QmUiMJGyUghqsR7PqSmvoDJ1g5sakwHEzofSVKHF1VjVHB",  # Photo Gallary
):
    return f"https://gateway.pinata.cloud/ipfs/{folder_cid}/{file_name}"


API_ENDPOINT: str = "https://api.pinata.cloud/"
# Custom tpe hints
ResponsePayload = tp.Dict[str, tp.Any]
OptionsDict = tp.Dict[str, tp.Any]
Headers = tp.Dict[str, str]


def upload_pinata():
    pinata_ = PinataPy(PINATA_API_KEY, PINATA_SECRET_API_KEY)
    return_val = pinata_.pin_file_to_ipfs(
        path_to_file=f"./tokens_to_upload/{network.show_active()}/"
    )
    print(return_val)
    return return_val


def main():
    upload_pinata()

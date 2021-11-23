import os
from brownie import StakeWarsCharacterUpgradable, StakeWarsFactoryUpgradable
from dotenv import load_dotenv

from scripts.file_functions import (
    read_address,
    read_edition,
    update_edition,
)
from scripts.helpful_scripts import get_account, print_weblink

load_dotenv()


def go_for_launch(swf, swc):
    if swf == None:
        swf = read_address(
            "StakeWarsFactoryUpgradableProxy", StakeWarsFactoryUpgradable
        )
    if swc == None:
        swc = read_address(
            "StakeWarsCharacterUpgradableProxy", StakeWarsCharacterUpgradable
        )
    master_account = get_account()
    curr_edition = read_edition()
    _securityKey = os.getenv("SECRET_LARGE_PRODUCT")
    swf._launchNFTs(_securityKey, {"from": master_account})
    swc._launchNFTs(_securityKey, {"from": master_account})
    print("Launch")
    update_edition(curr_edition + 1)
    print_weblink()


def main():
    go_for_launch()

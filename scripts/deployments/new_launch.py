import os
from brownie import StakeWarsFactoryUpgradable, StakeWarsCharacterUpgradable, network
from dotenv import load_dotenv

from scripts.file_functions import read_edition, read_group_uris, update_edition
from scripts.helpful_scripts import get_account, print_weblink

load_dotenv()


def go_for_launch():
    master_account = get_account()
    swf = StakeWarsFactoryUpgradable[-1]
    swc = StakeWarsCharacterUpgradable[-1]
    curr_edition = read_edition()
    _securityKey = os.getenv("SECRET_LARGE_PRODUCT")
    swf._launchNFTs(_securityKey, {"from": master_account})
    swc._launchNFTs(_securityKey, {"from": master_account})
    print("Launch")
    update_edition(curr_edition + 1)
    print_weblink()


def main():
    go_for_launch()

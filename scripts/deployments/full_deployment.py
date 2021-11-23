from scripts.file_functions import read_address
import time
from brownie import (
    ZERO_ADDRESS,
    network,
    StakeWarsFactoryUpgradable,
    StakeWarsCharacterUpgradable,
)
from scripts.deployments.new_deploy import all_deploy
from scripts.deployments.new_create_collection import save_collection
from scripts.deployments.new_launch import go_for_launch
from scripts.deployments.new_mint import run_mint, run_reserve
from scripts.helpful_scripts import get_account, print_weblink


def normal_user_register(user_account, swf, swc):
    if swf == None:
        swf = read_address(
            "StakeWarsFactoryUpgradableProxy", StakeWarsFactoryUpgradable
        )
    if swc == None:
        swc = read_address(
            "StakeWarsCharacterUpgradableProxy", StakeWarsCharacterUpgradable
        )
    warriors = swf.GetMyTokenWallet(user_account)
    rarities = []
    for w in range(len(warriors)):
        warrior_addr = swf.GetMyStakeWarrior(user_account, w)
        rarities.append(swc.GetRarity(warrior_addr, {"from": user_account}))
    return rarities


def user_prompts():
    value = input("[mint] Would you like to create a reserve:(#/y/n) ")
    if value.isnumeric():
        remint = value
    elif value == "y" or value == "Y":
        remint = 1
    else:
        remint = 0
    print(f"Minting {remint} Token(s)")

    have_normal_user = input(
        "[normal_user] Would you like to a normal user/mint:(#/y/n) "
    )
    if have_normal_user.isnumeric():
        have_normal_user = have_normal_user
    elif have_normal_user == "y" or have_normal_user == "Y":
        have_normal_user = 1
    else:
        have_normal_user = 0

    launch = input("[launch] Would you like to Launch:(y/n) ")
    launch = launch == "y" or launch == "Y"

    return (int(remint), int(have_normal_user), launch)


# Replicate a general use case
def main():
    master_account = get_account()
    (remint, have_normal_user, launch) = user_prompts()
    (swf, swc) = all_deploy()
    if network.show_active() != "development":
        time.sleep(60)
    print("Pre-Sale")
    if remint > 0:
        run_reserve(remint)

    if not swf.SaleActive():
        tx = swf._toggleSaleActive({"from": master_account})
        print("Sales Activated")
        tx.wait(1)
    else:
        print("Sales Already Activated")
    user_account = None
    if network.show_active() == "development":
        user_account = get_account(index=1)
    else:
        user_account = get_account("")
    if have_normal_user > 0:
        run_mint(have_normal_user, user_account)
    print("Pre-Launch")
    save_collection()

    if launch:
        go_for_launch(swf, swc)
        if have_normal_user > 0:
            normal_user_register(user_account, swf, swc)
    else:
        print_weblink(swc, swf)

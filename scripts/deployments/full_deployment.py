from brownie import ZERO_ADDRESS, StakeWarsFactory, StakeWarsCharacter
import time
from scripts.deployments.create_collection import save_collection
from scripts.deployments.deploy import (
    deployStakeWarsCharacter,
    deployStakeWarsFactory,
)
from scripts.deployments.launch import go_for_launch
from scripts.deployments.mint import run_mint, run_reserve
from scripts.deployments.reset_deployment import reset
from scripts.helpful_scripts import get_account, print_weblink


def normal_user_register(user_account):
    swf = StakeWarsFactory[-1]
    swc = StakeWarsCharacter[-1]
    warriors = swf.GetMyTokenWallet(user_account)
    for w in range(len(warriors)):
        warrior_addr = swf.GetMyStakeWarrior(user_account, w)
        if swc._registeredStakeWarriors(warrior_addr) == ZERO_ADDRESS:
            swc.RegisterStakeWarrior(warrior_addr, {"from": user_account})
        print(swc.GetRarity(warrior_addr, {"from": user_account}))


def user_prompts():
    reset_and_redeploy = input("[Reset?] Would you like to reset and redeploy:(y/n) ")
    reset_and_redeploy = reset_and_redeploy == "y" or reset_and_redeploy == "Y"

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

    return (reset_and_redeploy, int(remint), int(have_normal_user), launch)


# Replicate a general use case
def main():
    master_account = get_account()
    (reset_and_redeploy, remint, have_normal_user, launch) = user_prompts()
    if reset_and_redeploy:
        reset()
        deployStakeWarsFactory(100, master_account)
        deployStakeWarsCharacter(master_account)
        print_weblink()
        time.sleep(90)

    swf = StakeWarsFactory[-1]
    swc = StakeWarsCharacter[-1]
    print("Pre-Sale")
    if remint > 0:
        run_reserve(remint)

    if not swf.saleActive():
        tx = swf._toggleSaleActive({"from": master_account})
        print("Sales Activated")
        tx.wait(1)
    else:
        print("Sales Already Activated")
    user_account = get_account(key="from_green_key")
    if have_normal_user > 0:
        run_mint(have_normal_user, user_account)
    print("Pre-Launch")
    save_collection()

    if launch:
        go_for_launch()
        if have_normal_user > 0:
            normal_user_register(user_account)
    else:
        print_weblink()

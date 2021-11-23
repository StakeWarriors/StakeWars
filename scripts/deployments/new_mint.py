from brownie import StakeWarsFactoryUpgradable
from scripts.file_functions import read_address

from scripts.helpful_scripts import get_account


def run_reserve(iterations):
    account = get_account()
    stake_wars = read_address(
        "StakeWarsFactoryUpgradableProxy", StakeWarsFactoryUpgradable
    )
    print(f"Now Reserving: {iterations} token(s)")
    for i in range(iterations):
        stake_wars._reserve({"from": account}).wait(1)


def run_mint(iterations, account):
    if account == None:
        print("Failed to Provide Account")
        return
    stake_wars = read_address(
        "StakeWarsFactoryUpgradableProxy", StakeWarsFactoryUpgradable
    )
    amount = stake_wars.price()
    print(f"Now Minting: {iterations} token(s) at {amount} Wei")
    for i in range(iterations):
        stake_wars.mint({"from": account, "amount": amount}).wait(1)
        # pass


def main():
    # Solely Reserve
    value = input("[mint] Would you like to create a mint:(#/y/n) ")
    if value.isnumeric():
        remint = value
    elif value == "y" or value == "Y":
        remint = 1
    else:
        remint = 0
    run_reserve(int(remint))
    # run_mint(int(remint), get_account())

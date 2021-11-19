import os
from brownie import (
    StakeWarsFactoryUpgradable,
    StakeWarsCharacterUpgradable,
    VRFCoordinatorMock,
    config,
    network,
)
from dotenv import load_dotenv
from scripts.file_functions import (
    read_edition,
)

from scripts.helpful_scripts import (
    POLY_BLOCKCHAIN_ENVIRONMENTS,
    fund_link,
    get_contract,
    get_account,
    print_weblink,
)

load_dotenv()


def deploy_swfu(totalSupply, account=None):
    account = account if account else get_account()
    name = "StakeWars"
    symbol = "5WARS"
    edition = read_edition()
    default_uri = config["all_networks"]["default_uri"]
    _maxSupply = totalSupply
    _vrfCoordinator = get_contract("vrf_coordinator")
    _linkToken = get_contract("link_token")
    _linkFee = config["networks"][network.show_active()]["link_fee"]
    _keyhash = config["networks"][network.show_active()]["keyhash"]
    _securityKey = os.getenv("SECRET_LARGE_PRODUCT")

    stakewars_factory = None
    if network.show_active() in POLY_BLOCKCHAIN_ENVIRONMENTS:
        stakewars_factory = StakeWarsFactoryUpgradable.deploy(
            {"from": account},
        )
    else:
        stakewars_factory = StakeWarsFactoryUpgradable.deploy(
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "verify", False
            ),
        )

    stakewars_factory.__StakeWarsFactory_init(
        name,
        symbol,
        edition,
        default_uri,
        _maxSupply,
        _vrfCoordinator,
        _linkToken,
        _linkFee,
        _keyhash,
        _securityKey,
        {"from": account},
    )

    fund_link(stakewars_factory.address, account=account)
    crowd_safe_proxy = config["networks"][network.show_active()]["crowd_safe_proxy"]
    stakewars_factory._setCrowdSafeAddress(crowd_safe_proxy)
    print("StakeWarsFactoryUpgradable Deployed")
    return stakewars_factory


def deploy_swcu(account=None):
    account = account if account else get_account()
    _securityKey = os.getenv("SECRET_LARGE_PRODUCT")
    stakewars_character = StakeWarsCharacterUpgradable.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    stakewars_character.__StakeWarsCharacter_init(
        read_edition(),
        _securityKey,
        {"from": account},
    )
    print("StakeWarsCharacterUpgradable Deployed")

    return stakewars_character


def prompt():
    value = input(
        "[StakeWarsFactoryUpgradable] Would you like to StakeWarsFactoryUpgradable redeploy:(y/n) "
    )
    redeploySWF = value == "y" or value == "Y"
    value = input(
        "[StakeWarsCharacterUpgradable] Would you like to StakeWarsCharacterUpgradable redeploy:(y/n) "
    )
    redeploySWC = value == "y" or value == "Y"
    return (redeploySWF, redeploySWC)


def main():
    # Solely Deploy
    master_account = get_account()
    (redeploySWF, redeploySWC) = prompt()
    if redeploySWC:
        deploy_swcu(master_account)
    if redeploySWF:
        deploy_swfu(100, master_account)
    print_weblink()

import os
from brownie import StakeWarsFactory, StakeWarsCharacter, config, network
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
TOKENS_TO_MINT = 1

# "StakeWars", "5WARS", 1,"https://gateway.pinata.cloud/ipfs/QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn",100, "0xf0d54349aDdcf704F77AE15b96510dEA15cb7952", "0x514910771AF9Ca656af840dff83E8264EcF986CA",16000000000000000,"0xAA77729D3466CA35AE8D28B3BBAC7CC36A5031EFDC430821C02BC31A238AF445"
def deployStakeWarsFactory(totalSupply, account=None):
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

    if network.show_active() in POLY_BLOCKCHAIN_ENVIRONMENTS:
        stakewars_factory = StakeWarsFactory.deploy(
            name,
            symbol,
            edition,
            default_uri,
            _maxSupply,
            _vrfCoordinator,
            _linkToken,
            _linkFee,
            _keyhash,
            {"from": account},
        )

    else:
        stakewars_factory = StakeWarsFactory.deploy(
            name,
            symbol,
            edition,
            default_uri,
            _maxSupply,
            _vrfCoordinator,
            _linkToken,
            _linkFee,
            _keyhash,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "verify", False
            ),
        )

    fund_link(stakewars_factory.address, account=account)
    stakewars_factory._setSecurityKey(
        os.getenv("SECRET_LARGE_PRODUCT"), {"from": account}
    )
    crowd_safe_proxy = config["networks"][network.show_active()]["crowd_safe_proxy"]
    stakewars_factory._setCrowdSafeAddress(crowd_safe_proxy)
    print("StakeWarsFactory Deployed")
    return stakewars_factory


def deployStakeWarsCharacter(account=None):
    account = account if account else get_account()
    stakewars_character = StakeWarsCharacter.deploy(
        read_edition(),
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    stakewars_character._setSecurityKey(
        os.getenv("SECRET_LARGE_PRODUCT"), {"from": account}
    )
    print("StakeWarsCharacter Deployed")

    return stakewars_character


def prompt():
    value = input(
        "[StakeWarsFactory] Would you like to StakeWarsFactory redeploy:(y/n) "
    )
    redeploySWF = value == "y" or value == "Y"
    value = input(
        "[StakeWarsCharacter] Would you like to StakeWarsCharacter redeploy:(y/n) "
    )
    redeploySWC = value == "y" or value == "Y"
    return (redeploySWF, redeploySWC)


def main():
    # Solely Deploy
    master_account = get_account()
    (redeploySWF, redeploySWC) = prompt()
    if redeploySWC:
        deployStakeWarsCharacter(master_account)
    if redeploySWF:
        deployStakeWarsFactory(100, master_account)
    print_weblink()

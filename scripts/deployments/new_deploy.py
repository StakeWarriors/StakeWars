import os
from brownie import (
    StakeWarsFactoryUpgradable,
    Contract,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    StakeWarsCharacterUpgradable,
    config,
    network,
)
from dotenv import load_dotenv
from scripts.file_functions import (
    read_edition,
)

from scripts.helpful_scripts import (
    encode_function_data,
    fund_link,
    get_contract,
    get_account,
    print_weblink,
)

load_dotenv()


def deploy_admin():
    if config["networks"][network.show_active()].get("proxy_admin", 0) == 0:
        account = get_account()

        proxy_admin = ProxyAdmin.deploy({"from": account})
        print(f"Deploying new ProxyAdmin to f{proxy_admin}")
        return proxy_admin
    return config["networks"][network.show_active()]["proxy_admin"]


def deploy_swfu(conrtact=StakeWarsFactoryUpgradable):
    account = get_account()
    to_publish = config["networks"][network.show_active()].get("verify", False)
    stakewars_factory = conrtact.deploy({"from": account}, publish_source=to_publish)
    print("StakeWarsFactoryUpgradable Deployed")
    return stakewars_factory


def deploy_swcu(conrtact=StakeWarsCharacterUpgradable):
    account = get_account()
    to_publish = config["networks"][network.show_active()].get("verify", False)
    stakewars_character = conrtact.deploy({"from": account}, publish_source=to_publish)
    print("StakeWarsCharacterUpgradable Deployed")
    return stakewars_character


def deploy_swfu_proxy(totalSupply, stakewars_factory, proxy_admin, _vrfCoordinator):
    account = get_account()
    name = "StakeWars"
    symbol = "5WARS"
    edition = read_edition()
    default_uri = config["all_networks"]["default_uri"]
    _maxSupply = totalSupply
    _linkToken = get_contract("link_token")
    _linkFee = config["networks"][network.show_active()]["link_fee"]
    _keyhash = config["networks"][network.show_active()]["keyhash"]
    _securityKey = os.getenv("SECRET_LARGE_PRODUCT")

    swfactory_encode_initializer_function = encode_function_data(
        stakewars_factory.__StakeWarsFactory_init,
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
    )

    proxy = TransparentUpgradeableProxy.deploy(
        stakewars_factory.address,
        proxy_admin.address,
        swfactory_encode_initializer_function,
        {"from": account, "gas_limit": 1200000},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    proxy_stakewars_factory = Contract.from_abi(
        "StakeWarsFactoryUpgradable", proxy.address, StakeWarsFactoryUpgradable.abi
    )

    fund_link(proxy_stakewars_factory.address, account=account)
    crowd_safe_proxy = config["networks"][network.show_active()]["crowd_safe_proxy"]
    proxy_stakewars_factory._setCrowdSafeAddress(crowd_safe_proxy, {"from": account})
    return proxy, proxy_admin, proxy_stakewars_factory


def deploy_swcu_proxy(stakewars_character, proxy_admin):
    account = get_account()
    edition = read_edition()
    _securityKey = os.getenv("SECRET_LARGE_PRODUCT")
    swfactory_encode_initializer_function = encode_function_data(edition, _securityKey)

    proxy = TransparentUpgradeableProxy.deploy(
        stakewars_character.address,
        proxy_admin.address,
        swfactory_encode_initializer_function,
        {"from": account, "gas_limit": 1200000},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    proxy_stakewars_character = Contract.from_abi(
        "StakeWarsFactoryUpgradable", proxy.address, StakeWarsFactoryUpgradable.abi
    )
    return proxy, proxy_admin, proxy_stakewars_character


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
    proxy_admin = deploy_admin()
    (redeploySWF, redeploySWC) = prompt()
    proxy_stakewars_character = None
    proxy_stakewars_factory = None
    if redeploySWC:
        stakewars_character = deploy_swcu()
        (proxy, proxy_admin, proxy_stakewars_character) = deploy_swcu_proxy(
            stakewars_character, proxy_admin
        )
    if redeploySWF:
        swf = deploy_swfu()
        _vrfCoordinator = get_contract("vrf_coordinator")
        totalSupply = config["networks"][network.show_active()]["total_supply"]
        (proxy, proxy_admin, proxy_stakewars_factory) = deploy_swfu_proxy(
            totalSupply, swf, proxy_admin, _vrfCoordinator
        )

    print_weblink(proxy_stakewars_character, proxy_stakewars_factory)

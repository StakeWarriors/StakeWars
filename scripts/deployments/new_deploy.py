import os
from brownie import (
    Contract,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    StakeWarsFactoryUpgradable,
    StakeWarsCharacterUpgradable,
    config,
    network,
)
from dotenv import load_dotenv
from scripts.deployments.new_mocks import deploy_link, deploy_vrfc
from scripts.file_functions import read_edition, update_address
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
        update_address("ProxyAdmin", proxy_admin)
        return proxy_admin
    return config["networks"][network.show_active()]["proxy_admin"]


def deploy_swfu(contract=StakeWarsFactoryUpgradable):
    account = get_account()
    to_publish = config["networks"][network.show_active()].get("verify", False)
    stakewars_factory = contract.deploy({"from": account}, publish_source=to_publish)
    print("StakeWarsFactoryUpgradable Deployed")
    update_address("StakeWarsFactory", stakewars_factory)
    return stakewars_factory


def deploy_swcu(contract=StakeWarsCharacterUpgradable):
    account = get_account()
    to_publish = config["networks"][network.show_active()].get("verify", False)
    stakewars_character = contract.deploy({"from": account}, publish_source=to_publish)
    print("StakeWarsCharacterUpgradable Deployed")
    update_address("StakeWarsCharacter", stakewars_character)
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
    update_address("StakeWarsFactoryUpgradableProxy", proxy_stakewars_factory)
    return proxy, proxy_admin, proxy_stakewars_factory


def deploy_swcu_proxy(stakewars_character, proxy_admin):
    account = get_account()
    edition = read_edition()
    _securityKey = os.getenv("SECRET_LARGE_PRODUCT")
    swcharacter_encode_initializer_function = encode_function_data(
        stakewars_character.__StakeWarsCharacter_init, edition, _securityKey
    )

    proxy = TransparentUpgradeableProxy.deploy(
        stakewars_character.address,
        proxy_admin.address,
        swcharacter_encode_initializer_function,
        {"from": account, "gas_limit": 1200000},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    proxy_stakewars_character = Contract.from_abi(
        "StakeWarsCharacterUpgradable", proxy.address, StakeWarsCharacterUpgradable.abi
    )
    update_address("StakeWarsCharacterUpgradableProxy", proxy_stakewars_character)
    return proxy, proxy_admin, proxy_stakewars_character


def all_deploy():
    proxy_admin = deploy_admin()
    swf = deploy_swfu()
    _vrfCoordinator = None
    if network.show_active() == "development":
        link_token_mock = deploy_link()
        _vrfCoordinator = deploy_vrfc(link_token_mock)
        print("Mocking Coordinator")
    else:
        _vrfCoordinator = get_contract("vrf_coordinator")

    totalSupply = config["networks"][network.show_active()]["total_supply"]
    (proxy, proxy_admin, proxy_stakewars_factory) = deploy_swfu_proxy(
        totalSupply, swf, proxy_admin, _vrfCoordinator
    )
    _vrfCoordinator.callBackWithRandomness(0, 1, proxy_stakewars_factory)

    stakewars_character = deploy_swcu()
    (proxy, proxy_admin, proxy_stakewars_character) = deploy_swcu_proxy(
        stakewars_character, proxy_admin
    )

    print_weblink(proxy_stakewars_character, proxy_stakewars_factory)
    return (proxy_stakewars_factory, proxy_stakewars_character)


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

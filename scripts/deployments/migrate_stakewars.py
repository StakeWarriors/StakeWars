from brownie import (
    network,
    StakeWarsFactoryUpgradableV2,
    StakeWarsCharacterUpgradableV2,
    ProxyAdmin,
    Contract,
    TransparentUpgradeableProxy,
    config,
)
from scripts.deployments.new_deploy import deploy_swcu, deploy_swfu
from scripts.helpful_scripts import (
    get_account,
    encode_function_data,
    get_contract,
    print_weblink,
)


def do_factory_upgrade(contract, proxy, proxy_admin):
    account = get_account()
    proxy_swfactory = Contract.from_abi(
        "StakeWarsFactoryUpgradableV2",
        proxy.address,
        StakeWarsFactoryUpgradableV2.abi,
    )
    proxy_admin.upgrade(proxy.address, contract.address, {"from": account})
    return proxy, proxy_admin, proxy_swfactory


def migrate_factory_contract():
    contract = deploy_swfu()
    proxy = get_contract("TransparentUpgradeableProxy")
    proxy_admin = get_contract("ProxyAdmin")
    (proxy, proxy_admin, proxy_swfactory) = do_factory_upgrade(
        contract, proxy, proxy_admin
    )

    print_weblink()
    return proxy, proxy_admin, proxy_swfactory


def do_character_upgrade(contract, proxy, proxy_admin):
    account = get_account()
    proxy_character = Contract.from_abi(
        "StakeWarsCharacterUpgradableV2",
        proxy.address,
        StakeWarsCharacterUpgradableV2.abi,
    )
    proxy_admin.upgrade(proxy.address, contract.address, {"from": account})
    return proxy, proxy_admin, proxy_character


def migrate_character_contract():
    contract = deploy_swcu(StakeWarsCharacterUpgradableV2)
    proxy = get_contract("TransparentUpgradeableProxy")
    proxy_admin = get_contract("ProxyAdmin")
    (proxy, proxy_admin, proxy_swfactory) = do_factory_upgrade(
        contract, proxy, proxy_admin
    )

    print_weblink()
    return proxy, proxy_admin, proxy_swfactory


def fetch_last():
    # (proxy, proxy_admin, proxy_swfactory)=migrate_contract()
    proxy_admin = get_contract("ProxyAdmin")
    proxy = get_contract("TransparentUpgradeableProxy")
    proxy_swfactory = get_contract("StakeWarsFactoryUpgradable")
    proxy_swcharacter = get_contract("StakeWarsCharacterUpgradable")
    print_weblink()
    return proxy, proxy_admin, proxy_swfactory, proxy_swcharacter


def main():
    (proxy, proxy_admin, proxy_swfactory, proxy_swcharacter) = fetch_last()
    (proxy, proxy_admin, proxy_swfactory) = do_factory_upgrade(
        proxy_swfactory, proxy, proxy_admin
    )
    print(f"{proxy} {proxy_admin} {proxy_swfactory} {proxy_swcharacter}")

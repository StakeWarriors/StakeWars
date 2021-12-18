from brownie import (
    TransparentUpgradeableProxy,
    config,
    Contract,
    network,
    StakeWarsFactoryUpgradableMock,
)
import os
from brownie.network.contract import Contract
from dotenv import load_dotenv
from scripts.deployments.new_deploy import (
    deploy_admin,
    deploy_swcu,
    deploy_swcu_proxy,
    deploy_swfu,
    deploy_swfu_proxy,
)
from scripts.deployments.new_mocks import deploy_link, deploy_swfum, deploy_vrfc
from scripts.file_functions import read_edition, update_address, update_edition
from scripts.helpful_scripts import (
    encode_function_data,
    fund_link,
    get_account,
    get_contract,
)


load_dotenv()
TOKENS_TO_MINT = 1
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
FAKE_ADDRESS = "0x0000000000000000000000000000000000000001"


def setup_prep():
    update_edition(0)
    link_token_mock = deploy_link()
    proxy_admin = deploy_admin()
    swfactory = deploy_swfu()
    vrf_coordinator_mock = deploy_vrfc(link_token_mock)
    (proxy, proxy_admin, proxy_stakewars_factory) = deploy_swfu_proxy(
        10, swfactory, proxy_admin, vrf_coordinator_mock
    )
    stakewars_character = deploy_swcu()
    (proxy, proxy_admin, proxy_stakewars_character) = deploy_swcu_proxy(
        stakewars_character, proxy_admin
    )

    vrf_coordinator_mock.callBackWithRandomness(0, 1, proxy_stakewars_factory)
    return (proxy_stakewars_factory, proxy_stakewars_character)


def deploy_swfum_proxy(totalSupply, stakewars_factory, proxy_admin, _vrfCoordinator):
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
        "StakeWarsFactoryUpgradableMock",
        proxy.address,
        StakeWarsFactoryUpgradableMock.abi,
    )

    fund_link(proxy_stakewars_factory.address, account=account)
    crowd_safe_proxy = config["networks"][network.show_active()]["crowd_safe_proxy"]
    proxy_stakewars_factory._setCrowdSafeAddress(crowd_safe_proxy, {"from": account})
    update_address("StakeWarsFactoryUpgradableProxy", proxy_stakewars_factory)
    return proxy, proxy_admin, proxy_stakewars_factory


def setup_prep_mocks():
    update_edition(0)
    link_token_mock = deploy_link()
    proxy_admin = deploy_admin()
    swfactory = deploy_swfum()
    vrf_coordinator_mock = deploy_vrfc(link_token_mock)
    (proxy, proxy_admin, proxy_stakewars_factory) = deploy_swfum_proxy(
        10, swfactory, proxy_admin, vrf_coordinator_mock
    )
    stakewars_character = deploy_swcu()
    (proxy, proxy_admin, proxy_stakewars_character) = deploy_swcu_proxy(
        stakewars_character, proxy_admin
    )

    vrf_coordinator_mock.callBackWithRandomness(0, 1, proxy_stakewars_factory)
    return (proxy_stakewars_factory, proxy_stakewars_character)

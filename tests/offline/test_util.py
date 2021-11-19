import os
from brownie import (
    StakeWarsFactoryUpgradable,
    VRFCoordinatorMock,
    LinkToken,
    config,
    network,
)
from dotenv import load_dotenv
from scripts.file_functions import (
    read_edition,
)

from scripts.helpful_scripts import ZERO_ADDRESS, fund_link, get_contract, get_account

load_dotenv()
TOKENS_TO_MINT = 1
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
FAKE_ADDRESS = "0x0000000000000000000000000000000000000001"


def deploy_link():
    account = get_account()
    link_token_mock = LinkToken.deploy({"from": account})
    print("Mock Link Token Deployed")

    return link_token_mock


def deploy_vrfc(link_token_mock):
    account = get_account()
    vrf_coordinator_mock = VRFCoordinatorMock.deploy(link_token_mock, {"from": account})
    print("VRFCoordinatorMock Deployed")

    return vrf_coordinator_mock


def deploy_mock_swfu(totalSupply, vrf_mock):
    account = get_account()
    name = "StakeWars"
    symbol = "5WARS"
    edition = read_edition()
    default_uri = config["all_networks"]["default_uri"]
    maxSupply = totalSupply
    vrfCoordinator = vrf_mock
    linkToken = get_contract("link_token")
    linkFee = config["networks"][network.show_active()]["link_fee"]
    keyhash = config["networks"][network.show_active()]["keyhash"]
    securityKey = os.getenv("SECRET_LARGE_PRODUCT")

    stakewars_factory = StakeWarsFactoryUpgradable.deploy({"from": account})

    stakewars_factory.__StakeWarsFactory_init(
        name,
        symbol,
        edition,
        default_uri,
        maxSupply,
        vrfCoordinator,
        linkToken,
        linkFee,
        keyhash,
        securityKey,
        {"from": account},
    )

    fund_link(stakewars_factory.address, account=account)
    crowd_safe_proxy = config["networks"][network.show_active()]["crowd_safe_proxy"]
    stakewars_factory._setCrowdSafeAddress(crowd_safe_proxy).wait(1)
    print("StakeWarsFactoryUpgradable Deployed")
    return stakewars_factory


def setup_prep():
    link_token_mock = deploy_link()
    vrf_coordinator_mock = deploy_vrfc(link_token_mock)
    stakewars_factory = deploy_mock_swfu(10, vrf_coordinator_mock)
    vrf_coordinator_mock.callBackWithRandomness(0, 1234, stakewars_factory)

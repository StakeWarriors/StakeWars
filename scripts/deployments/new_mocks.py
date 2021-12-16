from brownie import VRFCoordinatorMock, LinkToken, StakeWarsFactoryUpgradableMock

from dotenv import load_dotenv

from scripts.helpful_scripts import get_account

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


def deploy_swfum(contract=StakeWarsFactoryUpgradableMock):
    account = get_account()
    stakewars_factory = contract.deploy({"from": account})
    print("StakeWarsFactoryUpgradableMock Deployed")
    return stakewars_factory

from brownie import (
    network,
    config,
    accounts,
    VRFCoordinatorMock,
    StakeWarsCharacterUpgradable,
    StakeWarsFactoryUpgradable,
    LinkToken,
    Contract,
)
import webbrowser

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
POLY_BLOCKCHAIN_ENVIRONMENTS = ["mumbai_moralis", "polygon-main"]

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

DECIMALS = 8
STARTING_PRICE = 200000000000
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_address(address):
    return config["networks"][network.show_active()][address]


def deploy_mocks(decimals=DECIMALS, starting_price=STARTING_PRICE):
    account = get_account()
    print(account)
    linkAddress = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(linkAddress.address, {"from": account})
    print("Mocks Deployed!")


def fund_link(contract_address, account=None, link_token=None, amount=None):
    amount = amount if amount else config["networks"][network.show_active()]["link_fee"]
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(
        contract_address, amount, {"from": account, "gas_limit": 1300000}
    )

    tx.wait(1)
    print("Contracted Funded")
    return tx


def get_contract(contract_name):
    """
    This function will get either the contract or a mock contract
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    active_account = config["networks"][network.show_active()]["active_account"]
    return accounts.add(config["wallets"][active_account])


def is_local(includeMockedBC=True):
    return network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or (
        includeMockedBC and network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    )


def is_mainnet():
    return network.show_active() in ["polygon-main", "mainnet"]


def page_open(Contract):
    if not is_local():
        webbrowser.open(
            f"https://{network.show_active()}.etherscan.io/address/{Contract[-1].address}",
            new=2,
            autoraise=True,
        )


def print_weblink():
    if not is_local():
        if network.show_active() in POLY_BLOCKCHAIN_ENVIRONMENTS:
            prefix = ""
            if not is_mainnet():
                prefix = "mumbai."
            # Running this command without deploying will show most recent deployments
            print(
                f"https://{prefix}polygonscan.com/address/{StakeWarsFactoryUpgradable[-1].address}"
            )
            print(
                f"https://{prefix}polygonscan.com/address/{StakeWarsCharacterUpgradable[-1].address}"
            )
        else:
            prefix = ""
            if not is_mainnet():
                prefix = f"{network.show_active()}."
            # Running this command without deploying will show most recent deployments
            print(
                f"https://{prefix}etherscan.io/address/{StakeWarsFactoryUpgradable[-1].address}"
            )
            print(
                f"https://{prefix}etherscan.io/address/{StakeWarsCharacterUpgradable[-1].address}"
            )

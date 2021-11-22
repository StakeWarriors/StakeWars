from brownie import StakeWarsFactoryUpgradable, exceptions
import pytest

from scripts.helpful_scripts import get_account
from tests.offline.test_util import setup_prep


def test_reserve_minting_valid():
    setup_prep()
    account = get_account()
    swf = StakeWarsFactoryUpgradable[-1]
    # Prep
    swf._reserve({"from": account}).wait(1)

    tokens = list(swf.GetMyTokenWallet(account, {"from": account}))
    assert len(tokens) == 1


def test_reserve_minting_invalid():
    setup_prep()
    account = get_account(index=2)
    swf = StakeWarsFactoryUpgradable[-1]

    with pytest.raises(exceptions.VirtualMachineError):
        swf._reserve({"from": account})


def test_presale_minting_valid():
    setup_prep()
    admin = get_account()
    account = get_account(index=2)
    swf = StakeWarsFactoryUpgradable[-1]
    price = swf.Price()

    assert swf.PresaleActive() == False
    with pytest.raises(exceptions.VirtualMachineError):
        swf.mintPresale({"from": account, "amount": price})

    swf._togglePreSaleActive({"from": admin})

    assert swf.PresaleActive() == True
    with pytest.raises(exceptions.VirtualMachineError):
        swf.mintPresale({"from": account, "amount": price})

    swf._addPresaleWhitelist(account, 3, {"from": admin})
    swf.mintPresale({"from": account, "amount": price})
    swf.mintPresale({"from": account, "amount": price})
    swf.mintPresale({"from": account, "amount": price})

    with pytest.raises(exceptions.VirtualMachineError):
        swf.mintPresale({"from": account, "amount": price})


def test_sale_minting_valid():
    setup_prep()
    admin = get_account()
    account = get_account(index=2)
    swf = StakeWarsFactoryUpgradable[-1]
    price = swf.Price()

    assert swf.SaleActive() == False
    with pytest.raises(exceptions.VirtualMachineError):
        swf.mint({"from": account, "amount": price})
    swf._toggleSaleActive({"from": admin})
    assert swf.SaleActive() == True
    swf.mint({"from": account, "amount": price})

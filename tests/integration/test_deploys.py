from brownie import StakeWarsFactory, exceptions
import pytest
import time

from scripts.helpful_scripts import get_account, is_local
from scripts.deployments.deploy import deployStakeWarsFactory
from scripts.helpful_scripts import get_account


def test_deployment_wallet_update():
    if is_local():
        pytest.skip()
    # Prep
    account = get_account()
    deployStakeWarsFactory(1, account=account)
    time.sleep(60)
    swf = StakeWarsFactory[-1]

    # Test
    assert len(swf.GetMyTokenWallet(account, {"from": account})) == 0

    # Prep
    swf._reserve({"from": account}).wait(1)
    # Test
    assert len(swf.GetMyTokenWallet(account, {"from": account})) == 1

    # Prep
    swf._reserve({"from": account}).wait(1)
    # Test
    assert len(swf.GetMyTokenWallet(account, {"from": account})) == 2


def test_donate_above_minimum():
    if not is_local():
        pytest.skip()
    # Prep
    master_account = get_account()
    user_account = get_account(1)
    deployStakeWarsFactory(100, master_account)
    swf = StakeWarsFactory[-1]
    user_origanal_balance = user_account.balance()
    master_origanal_balance = master_account.balance()

    # Act
    swf.Donate({"from": user_account, "value": swf.price() / 10}).wait(1)
    swf._withdraw({"from": master_account}).wait(1)

    assert user_account.balance() == user_origanal_balance - swf.price() / 10
    assert master_account.balance() == master_origanal_balance + swf.price() / 10


def test_donate_below_minimum():
    if not is_local():
        pytest.skip()
    # Prep
    master_account = get_account()
    user_account = get_account(1)
    deployStakeWarsFactory(100, master_account)
    swf = StakeWarsFactory[-1]

    # Act
    with pytest.raises(exceptions.VirtualMachineError):
        swf.Donate({"from": user_account, "value": swf.price() / 100}).wait(1)

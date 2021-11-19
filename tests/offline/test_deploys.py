from brownie import StakeWarsFactoryUpgradable, exceptions
import pytest

from scripts.helpful_scripts import get_account
from scripts.deployments.new_deploy import deploy_swfu
from scripts.helpful_scripts import get_account
from tests.offline.test_util import setup_prep


def test_deployment_wallet_update():
    # Prep
    account = get_account()
    setup_prep()
    swf = StakeWarsFactoryUpgradable[-1]

    # Test
    assert len(swf.GetMyTokenWallet(account, {"from": account})) == 0

    # Prep
    swf._reserve({"from": account}).wait(1)
    # Test
    tokens = list(swf.GetMyTokenWallet(account, {"from": account}))
    assert len(tokens) == 1
    assert tokens[0] == 0
    assert (
        swf.GetMyStakeWarrior(account, 0)
        == "0x725dfaf0E481653Ab86b2B071027e5DAA05cE8b4"
    )
    # Prep
    swf._reserve({"from": account}).wait(1)
    # Test
    tokens = list(swf.GetMyTokenWallet(account, {"from": account}))
    assert tokens[1] == 1
    assert len(tokens) == 2
    assert (
        swf.GetMyStakeWarrior(account, 1)
        == "0x23cB95f7AeF76c73fC189051400917eB3D764fF0"
    )


def test_donate_above_minimum():
    # Prep
    master_account = get_account()
    user_account = get_account(1)
    deploy_swfu(100, master_account)
    swf = StakeWarsFactoryUpgradable[-1]
    user_origanal_balance = user_account.balance()
    master_origanal_balance = master_account.balance()

    # Act
    swf.Donate({"from": user_account, "value": swf.Price() / 10}).wait(1)
    swf._withdraw({"from": master_account}).wait(1)

    assert user_account.balance() == user_origanal_balance - swf.Price() / 10
    assert master_account.balance() == master_origanal_balance + swf.Price() / 10


def test_donate_below_minimum():
    # Prep
    master_account = get_account()
    user_account = get_account(1)
    deploy_swfu(100, master_account)
    swf = StakeWarsFactoryUpgradable[-1]

    # Act
    with pytest.raises(exceptions.VirtualMachineError):
        swf.Donate({"from": user_account, "value": swf.Price() / 100}).wait(1)

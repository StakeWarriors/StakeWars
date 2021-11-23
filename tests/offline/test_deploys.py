import unittest
from brownie import StakeWarsFactoryUpgradable, exceptions
import pytest

from scripts.helpful_scripts import get_account
from scripts.deployments.new_deploy import deploy_swfu
from scripts.helpful_scripts import get_account
from tests.offline.test_util import setup_prep


class FooTestCase(unittest.TestCase):
    def test_deployment_wallet_update(self):
        # Prep
        account = get_account()
        (swf, swc) = setup_prep()

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
            == "0x321824B9e41754539061F1d5110d8e77f6F2D467"
        )
        # Prep
        swf._reserve({"from": account}).wait(1)
        # Test
        tokens = list(swf.GetMyTokenWallet(account, {"from": account}))
        assert tokens[1] == 1
        assert len(tokens) == 2
        assert (
            swf.GetMyStakeWarrior(account, 1)
            == "0x6278A188394E3e6aCb982ED522FF0E9a8B78ff11"
        )

    def test_donate_above_minimum(self):
        # Prep
        master_account = get_account()
        user_account = get_account(1)
        (swf, swc) = setup_prep()
        user_origanal_balance = user_account.balance()
        master_origanal_balance = master_account.balance()

        # Act
        swf.Donate({"from": user_account, "value": swf.Price() / 10}).wait(1)
        swf._withdraw({"from": master_account}).wait(1)

        assert user_account.balance() == user_origanal_balance - swf.Price() / 10
        assert master_account.balance() == master_origanal_balance + swf.Price() / 10

    def test_donate_below_minimum(self):
        # Prep
        user_account = get_account(1)
        (swf, swc) = setup_prep()

        # Act
        with pytest.raises(exceptions.VirtualMachineError):
            swf.Donate({"from": user_account, "value": swf.Price() / 100}).wait(1)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(FooTestCase("test_deployment_wallet_update"))
    suite.addTest(FooTestCase("test_donate_above_minimum"))
    suite.addTest(FooTestCase("test_donate_below_minimum"))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())

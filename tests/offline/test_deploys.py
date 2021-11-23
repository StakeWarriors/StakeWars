import unittest
from brownie import StakeWarsCharacterUpgradable, StakeWarsFactoryUpgradable, exceptions
import pytest
from scripts.file_functions import read_address

from scripts.helpful_scripts import get_account
from scripts.helpful_scripts import get_account
from tests.offline.test_util import setup_prep


class FooTestCase(unittest.TestCase):
    def test_deployment_addresses_updated(self):
        # Prep
        (swf, swc) = setup_prep()
        given_swc = read_address(
            "StakeWarsCharacterUpgradableProxy", StakeWarsCharacterUpgradable
        )
        assert given_swc == swc
        given_swf = read_address(
            "StakeWarsFactoryUpgradableProxy", StakeWarsFactoryUpgradable
        )
        assert given_swf == swf

    def test_deployment_wallet_update(self):
        # Prep
        account = get_account()
        (swf, swc) = setup_prep()
        # Test
        assert len(swf.GetMyTokenWallet(account, {"from": account})) == 0

        # Prep
        swf._reserve({"from": account}).wait(1)
        tokens = list(swf.GetMyTokenWallet(account, {"from": account}))
        # Test
        assert len(tokens) == 1
        assert tokens[0] == 0
        # Prep
        swf._reserve({"from": account}).wait(1)
        tokens = list(swf.GetMyTokenWallet(account, {"from": account}))
        # Test
        assert tokens[1] == 1
        assert len(tokens) == 2

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
    suite.addTest(FooTestCase("test_deployment_addresses_updated"))
    suite.addTest(FooTestCase("test_donate_above_minimum"))
    suite.addTest(FooTestCase("test_donate_below_minimum"))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())

import unittest
import os
import pytest

from scripts.deployments.new_mocks import FAKE_ADDRESS
from scripts.helpful_scripts import get_account
from tests.offline.test_util import setup_prep_mocks


class CharacterTestCase(unittest.TestCase):
    def get_minted_token(self):
        (swf, swc) = setup_prep_mocks()
        account = get_account(1)
        master_account = get_account()
        swf._setPrice("1 ether", {"from": master_account})
        swf._toggleSaleActive({"from": master_account})
        print(f"balance ={account.balance()}")
        price = swf.Price()
        swf.mint({"from": account, "amount": price})
        assert swf.totalSupply() > 0
        return (swf.GetMyStakeWarrior(account, 0), swf, swc)

    # All of these fields have been modified for troubleshooting and should be reverted afterwards
    def test_should_be_private_or_internal(self):
        (swf, swc) = setup_prep_mocks()
        with pytest.raises(AttributeError):
            swf._providedSeed()

    def test__launchNFTs(self):
        # and test_getEdition():
        (swf, swc) = setup_prep_mocks()
        master_account = get_account()
        assert swc.Edition() == 0
        _securityKey = os.getenv("SECRET_LARGE_PRODUCT")
        swc._launchNFTs(_securityKey, {"from": master_account})
        assert swc.Edition() == 1

    def test__raritySeed(self):
        (my_token, swf, swc) = self.get_minted_token()
        master_account = get_account()
        (seed) = swc._raritySeed(my_token, {"from": master_account})

        assert seed == 0

    def test_nontrivial_seed(self):
        (my_token, swf, swc) = self.get_minted_token()
        master_account = get_account()
        account = get_account(1)

        swf.setBlockTimestamp(1, {"from": account})
        price = swf.Price()
        swf.mint({"from": account, "amount": price})
        my_next_token = swf.GetMyStakeWarrior(account, 1)
        (seed) = swc._raritySeed(my_next_token, {"from": master_account})
        assert seed == 176186238879358457371830500600305455299267039231006607144962

        (rarity, rarityIndex) = swc._rarity(my_next_token, {"from": master_account})
        (clazz, clazzIndex) = swc._class(my_next_token, 0, {"from": account})
        (land, landIndex) = swc._land(my_next_token, 0, {"from": account})

        assert rarity == "Common"
        assert rarityIndex == 0
        assert clazz == "Psion"
        assert clazzIndex == 11
        assert land == "Convergence"
        assert landIndex == 3

    def test__rarity(self):
        (my_token, swf, swc) = self.get_minted_token()
        master_account = get_account()
        (rarity, rarityIndex) = swc._rarity(my_token, {"from": master_account})

        assert rarity == "Common"
        assert rarityIndex == 0

    def test_getRarityCount(self):
        """
        If this test fails, check the following areas are accurate:
            StakeWarsCharacterUpgradable.getRarityCount
            StakeWarsCharacterUpgradable._rarity
            StakeWarsInternals.rarityList
            stakewars_helper.toRarityEnglish
        """
        (my_token, swf, swc) = self.get_minted_token()
        assert swc.getRarityCount() == 14

    def test__class(self):
        (my_token, swf, swc) = self.get_minted_token()
        account = get_account(1)
        (clazz, clazzIndex) = swc._class(my_token, 0, {"from": account})

        assert clazz == "Artificer"
        assert clazzIndex == 0

    def test_getClassCount(self):
        """
        If this test fails, check the following areas are accurate:
            StakeWarsCharacterUpgradable.getClassCount
            StakeWarsCharacterUpgradable._class
            StakeWarsInternals.classList
            stakewars_helper.toClassEnglish
        """
        (swf, swc) = setup_prep_mocks()
        assert swc.getClassCount() == 21

    def test__land(self):
        (my_token, swf, swc) = self.get_minted_token()
        account = get_account(1)
        master_account = get_account()
        (land, landIndex) = swc._land(my_token, 0, {"from": account})

        assert land == "Abyss"
        assert landIndex == 0

    def test_getLandCount(self):
        """
        If this test fails, check the following areas are accurate:
            StakeWarsCharacterUpgradable.getLandCount
            StakeWarsCharacterUpgradable._land
            StakeWarsInternals.landList
            stakewars_helper.toLandEnglish
        """
        (swf, swc) = setup_prep_mocks()
        assert swc.getLandCount() == 19

    def test_GetLevels(self):
        (my_token, swf, swc) = self.get_minted_token()
        master_account = get_account()
        assert (
            swc.GetLevels(my_token, FAKE_ADDRESS, {"from": master_account})
            == "0x0000000000000000000000000000000000000000000000000000000000000000"
        )

    def test__setClass(self):
        (my_token, swf, swc) = self.get_minted_token()
        master_account = get_account()
        (clazz, clazz_index) = swc._class(my_token, 0, {"from": master_account})
        new_class_index = 2

        assert clazz_index == 0
        swc._setClass(my_token, new_class_index, 0, {"from": master_account})
        (clazz, clazz_index) = swc._class(my_token, 0, {"from": master_account})
        assert clazz_index == new_class_index

    def test__addClass(self):
        (my_token, swf, swc) = self.get_minted_token()
        master_account = get_account()

        swc._setClass(my_token, 4, 1, {"from": master_account})
        (clazz, clazz_index) = swc._class(my_token, 1, {"from": master_account})
        assert clazz_index == 4

    def test__setLand(self):
        (my_token, swf, swc) = self.get_minted_token()

        master_account = get_account()
        (land, land_index) = swc._land(my_token, 0, {"from": master_account})
        assert land_index == 0
        new_land = 2
        swc._setLand(my_token, new_land, 0, {"from": master_account})
        (land, land_index) = swc._land(my_token, 0, {"from": master_account})
        assert land_index == new_land

    def test__addLand(self):
        (my_token, swf, swc) = self.get_minted_token()
        master_account = get_account()

        swc._setLand(my_token, 4, 1, {"from": master_account})
        (land, land_index) = swc._land(my_token, 1, {"from": master_account})
        assert land_index == 4

    def test__updateExperience(self):
        (my_token, swf, swc) = self.get_minted_token()

        master_account = get_account()
        assert swc.GetExperience(my_token, FAKE_ADDRESS, {"from": master_account}) == 0
        swc._updateExperience(my_token, FAKE_ADDRESS, 1, True, {"from": master_account})
        assert swc.GetExperience(my_token, FAKE_ADDRESS, {"from": master_account}) == 1

    def test__setLevel(self):
        (my_token, swf, swc) = self.get_minted_token()

        master_account = get_account()
        assert (
            swc.GetLevels(my_token, FAKE_ADDRESS, {"from": master_account})
            == "0x0000000000000000000000000000000000000000000000000000000000000000"
        )
        new_level = "0x0000000000000000000000000000000000000000000000000000000000000001"
        swc._setLevel(my_token, FAKE_ADDRESS, new_level, {"from": master_account})
        assert (
            swc.GetLevels(my_token, FAKE_ADDRESS, {"from": master_account}) == new_level
        )


def suite(self):
    suite = unittest.TestSuite()
    suite.addTest(CharacterTestCase("test_deployment_wallet_update"))
    suite.addTest(CharacterTestCase("test_should_be_private_or_internal"))
    suite.addTest(CharacterTestCase("test_nontrivial_seed"))
    suite.addTest(CharacterTestCase("test__launchNFTs"))
    suite.addTest(CharacterTestCase("test__raritySeed"))
    suite.addTest(CharacterTestCase("test__rarity"))
    suite.addTest(CharacterTestCase("test_getRarityCount"))
    suite.addTest(CharacterTestCase("test__class"))
    suite.addTest(CharacterTestCase("test_getClassCount"))
    suite.addTest(CharacterTestCase("test__land"))
    suite.addTest(CharacterTestCase("test_getLandCount"))
    suite.addTest(CharacterTestCase("test_GetLevels"))
    suite.addTest(CharacterTestCase("test__setClass"))
    suite.addTest(CharacterTestCase("test__addClass"))
    suite.addTest(CharacterTestCase("test__setLand"))
    suite.addTest(CharacterTestCase("test__addLand"))
    suite.addTest(CharacterTestCase("test__updateExperience"))
    suite.addTest(CharacterTestCase("test__setLevel"))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())

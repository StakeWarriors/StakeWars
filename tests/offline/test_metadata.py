import os
from pathlib import Path
from brownie import StakeWarsFactoryUpgradable
from scripts.helpful_scripts import get_account
from dotenv import load_dotenv

from scripts.ipfs_rarity.colors import get_traits
from tests.offline.test_util import setup_prep

load_dotenv()


def test_get_traits():
    test_file = None
    img_dir_opt1 = "img/gif/Abbus_Nykama.gif"
    img_dir_opt2 = "img/used_gifs/Abbus_Nykama.gif"
    if Path(img_dir_opt1).exists():
        test_file = Path(img_dir_opt1)
    else:
        test_file = Path(img_dir_opt2)

    traits = get_traits(test_file)
    assert len(traits) == 7


# This Test Requires a Reset
def test_get_base_uri_valid():
    # Setup
    fro = {"from": get_account()}
    setup_prep()
    stake_wars = StakeWarsFactoryUpgradable[-1]
    stake_wars._reserve(fro).wait(1)

    # Test Metadata Release Prep
    assert stake_wars.Edition() == 0
    assert stake_wars.getBaseURILength() == 0

    # Metadata Release Prep
    fake_base_uri = "/fake/base"
    stake_wars._setBaseURI(0, fake_base_uri, fro)
    # Test Metadata Release After Prep
    assert stake_wars.getBaseURILength() == 1
    assert stake_wars.defaultURI() == stake_wars.tokenURI(0)

    # Metadata Release
    _securityKey = os.getenv("SECRET_LARGE_PRODUCT")
    stake_wars._launchNFTs(_securityKey, fro).wait(1)

    # Test After Metadata Release
    assert stake_wars.Edition() == 1
    assert stake_wars.getBaseURILength() == 1
    assert stake_wars.tokenURI(0) == "/fake/base/0.json"  # Index = 0

    # Purchase After Release
    stake_wars._reserve({"from": get_account()})

    # Test Purchase After Release
    assert stake_wars.defaultURI() == stake_wars.tokenURI(1)

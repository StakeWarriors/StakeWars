from pathlib import Path
from brownie import (
    StakeWarsFactory,
    Contract,
    StakeWarsInternals,
)
from scripts.helpful_scripts import get_account

from scripts.ipfs_rarity.colors import get_traits
from tests.integration.test_util import setup_prep


def test_get_traits():
    test_file = None
    img_dir_opt1 = "img/gif/Ingerantsrin_Nirud.gif"
    img_dir_opt2 = "img/used_gifs/Ingerantsrin_Nirud.gif"
    if Path(img_dir_opt1).exists():
        test_file = Path(img_dir_opt1)
    else:
        test_file = Path(img_dir_opt2)

    traits = get_traits(test_file)
    assert len(traits) == 6


# This Test Requires a Reset
def test_get_base_uri_valid():
    # Prep
    setup_prep()
    stake_wars = StakeWarsFactory[-1]

    # Test
    # Before the Release
    assert stake_wars.defaultURI() == stake_wars.tokenURI(0)

    # Prep
    fake_base_uri = "/fake/base"
    stake_wars._launchNFTs(fake_base_uri, {"from": get_account()})

    # Test
    # After the Release
    assert stake_wars.tokenURI(0).index(f"{fake_base_uri}/ed.1/") == 0  # Index = 0


# This Test Requires a Reset
def test_get_base_uri_not_updated():
    # Prep
    setup_prep()
    stake_wars = StakeWarsFactory[-1]

    # Test
    # Before the Release

    # Prep
    fake_base_uri = "/fake/base"
    stake_wars._launchNFTs(fake_base_uri, {"from": get_account()})
    #  Newly minted Tokens are on new editions, not yet released
    stake_wars._reserve({"from": get_account()})

    # Test
    # After the Release
    assert stake_wars.defaultURI() == stake_wars.tokenURI(1)

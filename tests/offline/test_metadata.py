import brownie
import os
from pathlib import Path
from brownie import StakeWarsFactoryUpgradable

from scripts.deployments.new_create_collection import create_collection
from scripts.deployments.reset_deployment import reset
from scripts.file_functions import read_address
from scripts.helpful_scripts import get_account
from dotenv import load_dotenv

from scripts.ipfs_rarity.colors import get_traits
from tests.offline.test_util import setup_prep, setup_prep_mocks

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
    assert len(traits) >= 5


# This Test Requires a Reset
def test_get_base_uri_valid():
    # Setup
    fro = {"from": get_account()}
    setup_prep()
    stake_wars = read_address(
        "StakeWarsFactoryUpgradableProxy", StakeWarsFactoryUpgradable
    )
    stake_wars._reserve(fro).wait(1)

    # Test Metadata Release Prep
    assert stake_wars.Edition() == 0
    assert stake_wars.getBaseURILength(fro) == 0

    # Metadata Release Prep
    fake_base_uri = "/fake/base"
    stake_wars._setBaseURI(0, fake_base_uri, fro)
    # Test Metadata Release After Prep
    assert stake_wars.getBaseURILength(fro) == 1
    assert stake_wars.defaultURI() == stake_wars.tokenURI(0)

    # Metadata Release
    _securityKey = os.getenv("SECRET_LARGE_PRODUCT")
    stake_wars._launchNFTs(_securityKey, fro).wait(1)

    # Test After Metadata Release
    assert stake_wars.Edition() == 1
    assert stake_wars.getBaseURILength(fro) == 1
    assert stake_wars.tokenURI(0) == "/fake/base/0.json"  # Index = 0

    # Purchase After Release
    stake_wars._reserve({"from": get_account()})

    # Test Purchase After Release
    assert stake_wars.defaultURI() == stake_wars.tokenURI(1)


def test_generated_metadata():
    fro = {"from": get_account()}
    setup_prep_mocks()
    stake_wars = read_address(
        "StakeWarsFactoryUpgradableProxy", StakeWarsFactoryUpgradable
    )
    stake_wars._reserve(fro).wait(1)
    (tokens, uri_group) = create_collection()
    assert uri_group == 0
    assert len(tokens[0]["name"]) > 0
    assert len(tokens[0]["attributes"]) > 7

    assert tokens[0]["attributes"][0]["trait_type"] == "Edition"
    assert tokens[0]["attributes"][0]["value"] == 0

    assert tokens[0]["attributes"][1]["trait_type"] == "Rarity"
    assert type(tokens[0]["attributes"][1]["value"]) == str
    assert len(tokens[0]["attributes"][1]["value"]) > 0

    assert tokens[0]["attributes"][2]["trait_type"] == "Rarity Level"
    assert type(tokens[0]["attributes"][2]["value"]) == brownie.convert.datatypes.Wei

    assert tokens[0]["attributes"][3]["trait_type"] == "Base Class"
    assert type(tokens[0]["attributes"][3]["value"]) == str
    assert len(tokens[0]["attributes"][3]["value"]) > 0

    assert tokens[0]["attributes"][4]["trait_type"] == "Base Land"
    assert type(tokens[0]["attributes"][4]["value"]) == str
    assert len(tokens[0]["attributes"][4]["value"]) > 0

    assert tokens[0]["attributes"][5]["trait_type"] == "Creature"
    assert type(tokens[0]["attributes"][5]["value"]) == str
    assert len(tokens[0]["attributes"][5]["value"]) > 0

    assert tokens[0]["attributes"][6]["trait_type"] == "Intelligence"
    assert type(tokens[0]["attributes"][6]["value"]) == int
    reset()

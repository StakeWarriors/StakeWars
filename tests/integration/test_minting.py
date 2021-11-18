from brownie import (
    StakeWarsFactory,
    Contract,
    StakeWarsInternals,
)
from scripts.deployments.stakewars_helper import archive_tokens_to_metadata

from scripts.file_functions import read_archived_tokens, update_archived_tokens
from tests.integration.test_util import setup_prep


def get_tokens():
    stake_wars = StakeWarsFactory[-1]
    tokens = []
    numOwnedWarriors = stake_wars.warriorsToBeDetailedLength()
    for warriorIndex in range(numOwnedWarriors):
        warrior = stake_wars.warriorsToBeDetailed(warriorIndex)
        character = Contract.from_abi(
            StakeWarsInternals._name, warrior, StakeWarsInternals.abi
        )
        tokens.append(character.tokenId())
    return tokens


def test_archiving():
    # Prep
    setup_prep()
    # Has to be local because _reserve requires _providedSeed
    update_archived_tokens([])
    tokens = get_tokens()

    # Test
    assert len(tokens) == 1

    # Prep
    archive_tokens_to_metadata(tokens)
    tokens = get_tokens()

    # Test
    assert len(tokens) == 0
    assert len(read_archived_tokens()) == 1

    # Revert
    update_archived_tokens([])

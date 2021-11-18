import time
from brownie import StakeWarsFactory
import pytest
from scripts.deployments.deploy import deployStakeWarsFactory
from scripts.file_functions import update_edition

from scripts.helpful_scripts import get_account, is_local


def setup_prep():
    if is_local():
        pytest.skip()
    update_edition(1)
    # Has to be local because _reserve requires _providedSeed
    account = get_account()
    deployStakeWarsFactory(10, account=account)
    stake_wars = StakeWarsFactory[-1]
    time.sleep(90)
    stake_wars._reserve({"from": account})

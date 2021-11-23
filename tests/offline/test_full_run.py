from brownie import Contract, StakeWarsInternals
from scripts.deployments.new_deploy import all_deploy
from scripts.deployments.new_create_collection import create_collection
from scripts.deployments.new_launch import go_for_launch
from scripts.deployments.new_mint import run_mint
from scripts.deployments.reset_deployment import reset
from scripts.helpful_scripts import get_account


def test_get_rarity():
    reset()
    master_account = get_account()
    (swf, swc) = all_deploy()
    swf._toggleSaleActive({"from": master_account})
    user_account = get_account(index=1)
    run_mint(1, user_account)
    create_collection(master_account)
    go_for_launch(swf, swc)
    warriors = swf.GetMyTokenWallet(user_account)
    # rarities = normal_user_register(user_account, swf, swc)
    warrior_addr = swf.GetMyStakeWarrior(user_account, warriors[0])
    character = Contract.from_abi(
        StakeWarsInternals._name, warrior_addr, StakeWarsInternals.abi
    )
    assert character.edition() == 0
    assert swc.getEdition(warrior_addr) == 0
    assert swc.Edition() == 1

    swc.GetRarity(warrior_addr, {"from": user_account})

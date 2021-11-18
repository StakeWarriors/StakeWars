import os
from brownie import StakeWarsFactoryUpgradable, StakeWarsInternals, Contract, network
from scripts.file_functions import (
    read_archived_tokens,
    read_group_uris,
    update_archived_tokens,
)
from scripts.helpful_scripts import get_account
from dotenv import load_dotenv


load_dotenv()


def set_base_uri():
    master_account = get_account()
    swf = StakeWarsFactoryUpgradable[-1]
    uri_group = StakeWarsFactoryUpgradable[-1]._uriGroup()
    print(uri_group)
    cid_hash = read_group_uris().get(str(uri_group))
    print(cid_hash)
    assert len(cid_hash) > 0
    ipfs_uri = f"https://gateway.pinata.cloud/ipfs/{cid_hash}/{network.show_active()}"
    swf._setBaseURI(uri_group, ipfs_uri, {"from": master_account})


def archive_tokens_to_metadata(tokens):
    account = get_account()
    stake_wars = StakeWarsFactoryUpgradable[-1]
    archived_tokens = read_archived_tokens()
    print(f"Archiving {len(tokens)} Token(s)")
    for token in tokens:
        archivable = {
            "tid": token["tokenId"],
            "rarity": token["attributes"][1]["value"],
        }
        archived_tokens.append(archivable)
    update_archived_tokens(archived_tokens)
    set_base_uri()
    stake_wars._resetWarriorsToBeDetails({"from": account})


def get_rarities(account=None):
    account = account if account else get_account()
    stake_wars = StakeWarsFactoryUpgradable[-1]
    numOwnedWarriors = stake_wars.warriorsToBeDetailedLength()
    public_token_uris = []
    rarities_numbers = []
    rarities_names = []
    clazzes = []
    edition = []
    tokens = []
    lands = []
    SECRET = os.getenv("SECRET_LARGE_PRODUCT")
    for warriorIndex in range(numOwnedWarriors):
        warrior = stake_wars.warriorsToBeDetailed(warriorIndex)
        character = Contract.from_abi(
            StakeWarsInternals._name, warrior, StakeWarsInternals.abi
        )
        land = toLandEnglish(character.land(0))
        lands.append(land)
        clazz = toClassEnglish(character.clazz(0))
        clazzes.append(clazz)
        (rarity_name, rarity_number) = character.getRarity(SECRET, {"from": account})
        rarities_numbers.append(rarity_number)
        rarities_names.append(toRarityEnglish(rarity_name))

        public_token_uri = character.publicUriKey({"from": account})
        public_token_uri = str(public_token_uri)
        tokens.append(character.tokenId())
        edition.append(character.edition())
        public_token_uris.append(public_token_uri)
    return (
        rarities_numbers,
        rarities_names,
        clazzes,
        lands,
        tokens,
        edition,
        public_token_uris,
    )


#
# Not sure if this is respectable, it saves quite a bit of gas and has the same effect. However
# it means that the metadata isn't explicitly writing the off-chain metadata for the IPFS.
# Though, nothing off-chain can truly be trustless. Future iterations will allow for on-chain to
# IPFS. But that will have to come after a time when such transactions are affordable
#
def toRarityEnglish(rarity):
    if rarity == 1:
        return "Fairly Common"
    elif rarity == 2:
        return "Keeper"
    elif rarity == 3:
        return "Shiny"
    elif rarity == 4:
        return "Bronze"
    elif rarity == 5:
        return "Silver"
    elif rarity == 6:
        return "Gold"
    elif rarity == 7:
        return "Platnium"
    elif rarity == 8:
        return "Unobtainium"
    elif rarity == 9:
        return "Super Rare"
    elif rarity == 10:
        return "Truly Rare"
    elif rarity == 11:
        return "Forgotten"
    elif rarity == 12:
        return "Secret"
    elif rarity == 13:
        return "Singles"
    return "Common"


def toLandEnglish(land):
    if land == 1:
        return "Arceus"
    elif land == 2:
        return "Avilon"
    elif land == 3:
        return "Convergence"
    elif land == 4:
        return "The Deep"
    elif land == 5:
        return "Genogia"
    elif land == 6:
        return "Firebrink"
    elif land == 7:
        return "Gilbatree"
    elif land == 8:
        return "Glacia"
    elif land == 9:
        return "Greater Portsmouth"
    elif land == 10:
        return "Hell"
    elif land == 11:
        return "Norvak"
    elif land == 12:
        return "Orlal"
    elif land == 13:
        return "Sartook"
    elif land == 14:
        return "Second Landing"
    elif land == 15:
        return "Tabishan"
    elif land == 16:
        return "Tellbourogh"
    elif land == 17:
        return "North Highlands"
    elif land == 18:
        return "Forgotten"
    else:
        return "Abyss"


def toClassEnglish(index):
    if index == 1:
        return "Avenger"
    elif index == 2:
        return "Ardent"
    elif index == 3:
        return "Barbarian"
    elif index == 4:
        return "Bard"
    elif index == 5:
        return "Cleric"
    elif index == 6:
        return "Druid"
    elif index == 7:
        return "Fighter"
    elif index == 8:
        return "Monk"
    elif index == 9:
        return "Paladin"
    elif index == 10:
        return "Player"
    elif index == 11:
        return "Psion"
    elif index == 12:
        return "Ranger"
    elif index == 13:
        return "Rogue"
    elif index == 14:
        return "Priest"
    elif index == 15:
        return "Shaman"
    elif index == 16:
        return "Sorcerer"
    elif index == 17:
        return "Warden"
    elif index == 18:
        return "Warlock"
    elif index == 19:
        return "Warlord"
    elif index == 20:
        return "Wizard"
    else:
        return "Artificer"

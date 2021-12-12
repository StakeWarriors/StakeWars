import json
import pytest
from scripts.helpful_scripts import is_local
from scripts.pinata import gen_edition_cid, upload_to_pinata
from brownie import network

correct_answers = {
    "kovan": {
        "test_can_generate_cid": "QmRHUMbQSJBaNvLjpcnNY4Qi1hdvsCh4RmQY6FEFiaZdSW",
        "test_can_upload_pinata": "QmUTA3V3wgZAxXbcKrNbeRPFuPcTtc1FJJJwUaMKFkhe8c",
    }
}


def test_can_generate_cid():
    if is_local():
        pytest.skip()
    cid = gen_edition_cid(1)
    assert cid == correct_answers[network.show_active()]["test_can_generate_cid"]


def test_can_upload_pinata():
    hash = "QmRHUMbQSJBaNvLjpcnNY4Qi1hdvsCh4RmQY6FEFiaZdSW"
    token = """
    {
  "name": "Ois Nyhas",
  "description": "StakeWars\u2122 is a Non-Fungible Token (NFT) Saga. These NFT's have been designed for both collectible interests as well as future gaming capabilities. With the future proofing design of the StakeWise Smart contract, every SWARS token minted will be able to participate in StakeWise Games. But not all SWARS Tokens are created equal, every NFT has their own quirks, powers and characteristics. Some will be quite rare and powerful, so get grab them up where you can find them. StakeWise\u2122 is the NFT driven gaming collectible entirely detailed on the Ethereum blockchain.",
  "image": "https://ipfs.io/ipfs/QmX8QhVJo6e8n1MmySFirSymVz1ZRSgxM9ZBHJfD4zWih9/?filename=Ois_Nyhas.gif",
  "attributes": [
    { "trait_type": "Edition", "display_type": "number", "value": 1 },
    { "trait_type": "Rarity", "display_type": "number", "value": "Silver" },
    {
      "trait_type": "Character Bio",
      "value": "I just want to be a notorious banker."
    },
    { "trait_type": "Base Class", "value": "Psion" },
    { "trait_type": "Base Land", "value": "Orlal" },
    { "trait_type": "Intelligence", "display_type": "number", "value": 0.462 },
    { "trait_type": "Trait", "value": "Has a child" },
    { "trait_type": "Trait", "value": "Poor" },
    { "trait_type": "Trait", "value": "Honorable" },
    { "trait_type": "Trait", "value": "Caring" },
    { "trait_type": "Trait", "value": "Lonely" },
    { "trait_type": "Trait", "value": "Merciless" }
  ]
}
    """
    (return_hash, ign) = upload_to_pinata(json.loads(token), hash)
    expected_hash = correct_answers[network.show_active()]["test_can_upload_pinata"]
    print(return_hash, expected_hash)
    assert return_hash == expected_hash

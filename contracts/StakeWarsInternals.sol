// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

import "./interfaces/IStakeWarsInternals.sol";

contract StakeWarsInternals is IStakeWarsInternals {
    uint256 public edition;
    uint256 public tokenId;
    uint256 public uriGroup;

    uint256 private _securityKey;
    uint256 private raritySeed;
    uint256 private creationTime;

    mapping(uint8 => uint8) public land;
    mapping(uint8 => uint8) public clazz;
    mapping(address => uint256) public experience;
    mapping(address => bytes32) private levels;

    constructor(
        uint256 _edition,
        uint256 _raritySeed,
        uint256 _tokenId,
        uint256 _uriGroup,
        uint256 securityKey
    ) {
        edition = _edition;
        _securityKey = securityKey;
        tokenId = _tokenId;
        uriGroup = _uriGroup;
        raritySeed = _raritySeed;

        uint48 rare48 = uint48(raritySeed);
        (clazz[0], ) = determineClass(rare48);
        (land[0], ) = determineLand(rare48);
        creationTime = block.timestamp;
    }

    function getRaritySeed(uint256 securityKey)
        public
        view
        override
        securityCheck(securityKey)
        returns (uint256)
    {
        return raritySeed;
    }

    function getRarity(uint256 securityKey)
        public
        view
        override
        securityCheck(securityKey)
        returns (uint16, uint16)
    {
        unchecked {
            uint16 length = uint16(rarityList.length);
            uint16 rareValue = uint16((raritySeed * creationTime) % 2**length);
            for (uint16 i = length - 1; i > 0; i--) {
                if (rareValue >= 2**i) {
                    return (rarityList[length - 1 - i], uint16(length - 1 - i));
                }
            }
            return (rarityList[0], 0);
        }
    }

    function getLand(uint8 index) public view override returns (uint8) {
        return land[index];
    }

    function getClass(uint8 index) public view override returns (uint8) {
        return clazz[index];
    }

    function getLevels(address game, uint256 securityKey)
        public
        view
        override
        securityCheck(securityKey)
        returns (bytes32)
    {
        return levels[game];
    }

    function GetExperience(address game, uint256 securityKey)
        public
        view
        override
        securityCheck(securityKey)
        returns (uint256)
    {
        return experience[game];
    }

    function setClass(
        uint8 newClass,
        uint8 index,
        uint256 securityKey
    ) public override securityCheck(securityKey) {
        clazz[index] = newClass;
    }

    function setLand(
        uint8 newLand,
        uint8 index,
        uint256 securityKey
    ) public override securityCheck(securityKey) {
        land[index] = newLand;
    }

    function setLevel(
        address game,
        bytes32 value,
        uint256 securityKey
    ) public override securityCheck(securityKey) {
        levels[game] = value;
    }

    function updateExperience(
        address game,
        uint256 amount,
        bool increase,
        uint256 securityKey
    ) public override securityCheck(securityKey) {
        if (increase) {
            experience[game] = uint256(experience[game]) + amount;
        } else {
            experience[game] = uint256(experience[game]) - amount;
        }
    }

    function determineClass(uint48 value)
        public
        view
        override
        returns (uint8, uint8)
    {
        uint8 index;
        unchecked {
            index = uint8(value % classList.length);
        }
        return (classList[index], index);
    }

    function determineLand(uint48 value)
        public
        view
        override
        returns (uint8, uint8)
    {
        uint8 index;
        unchecked {
            index = uint8(value % landList.length);
        }
        return (landList[index], index);
    }

    modifier securityCheck(uint256 securityKey) {
        require(securityKey == _securityKey);
        _;
    }

    uint8[] rarityList = [
        0, // "Common",
        1, // "Fairly Common",
        2, // "Keeper",
        3, // "Shiny",
        4, // "Bronze",
        5, // "Silver",
        6, // "Gold",
        7, // "Platnium",
        8, // "Super Rare",
        9, // "Unobtainium"
        10, // "Truly Rare",
        11, // "Forgotten",
        12, // "Secret",
        13 // "Singles"
    ];

    uint8[] classList = [
        0, // "Artificer",
        1, // "Avenger",
        2, // "Ardent",
        3, // "Barbarian",
        4, // "Bard",
        5, // "Cleric",
        6, // "Druid",
        7, // "Fighter",
        8, // "Monk",
        9, // "Paladin",
        10, // "Player",
        11, // "Psion",
        12, // "Ranger",
        13, // "Rogue",
        14, // "Priest",
        15, // "Shaman",
        16, // "Sorcerer",
        17, // "Warden",
        18, // "Warlock",
        19, // "Warlord",
        20 // "Wizard"
    ];

    uint8[] landList = [
        0, //"Abyss"
        1, // "Arceus"
        2, // "Avilon"
        3, // "Convergence"
        4, // "The Deep"
        5, // "Genogia"
        6, // "Firebrink"
        7, // "Gilbatree"
        8, // "Glacia"
        9, // "Greater Portsmouth"
        10, // "Hell"
        11, // "Norvak"
        12, // "Orlal"
        13, // "Sartook"
        14, // "Second Landing"
        15, // "Tabishan"
        16, // "Tellbourogh"
        17, // "North Highlands"
        18 // "Forgotten"
    ];
}

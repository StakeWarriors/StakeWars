// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

import "./interfaces/IStakeWarsInternals.sol";
import "./vendor/upgradeable/openzeppelin/access/AccessControlUpgradeable.sol";

contract StakeWarsCharacterUpgradable is AccessControlUpgradeable {
    uint256 public Edition; //Length is = to Edition -+1
    uint256[] private _securityKey;
    //Addresses to supported games
    mapping(address => bool) public _registeredGames;

    function __StakeWarsCharacter_init(uint256 _edition, uint256 securityKey)
        public
        initializer
    {
        __AccessControl_init();
        __StakeWarsCharacter_init_unchained(_edition, securityKey);
    }

    function __StakeWarsCharacter_init_unchained(
        uint256 _edition,
        uint256 securityKey
    ) public initializer {
        _securityKey.push(securityKey);
        Edition = _edition;
    }

    function _launchNFTs(uint256 securityKey)
        public
        onlyRole(DEFAULT_ADMIN_ROLE)
    {
        Edition++;
        _securityKey.push(securityKey);
    }

    function getEdition(address warriorAddr) public view returns (uint256) {
        return IStakeWarsInternals(warriorAddr).edition();
    }

    /**
     * Character Functions
     */
    function _raritySeed(address characterAddr)
        public
        view
        onlyAdminOrGC
        returns (uint256)
    {
        IStakeWarsInternals character = IStakeWarsInternals(characterAddr);
        return character.getRaritySeed(_securityKey[character.edition()]);
    }

    function GetRarity(address characterAddr)
        public
        view
        onlyAfterRelease(characterAddr)
        returns (string memory)
    {
        (string memory ret, ) = _rarity(characterAddr);
        return ret;
    }

    function _rarity(address characterAddr)
        public
        view
        onlyAfterRelease(characterAddr)
        returns (string memory, uint16)
    {
        IStakeWarsInternals character = IStakeWarsInternals(characterAddr);
        uint256 secret = _securityKey[character.edition()];
        (uint16 rarity, uint16 index) = character.getRarity(secret);
        if (rarity == 1) return ("Fairly Common", index);
        else if (rarity == 2) return ("Keeper", index);
        else if (rarity == 3) return ("Shiny", index);
        else if (rarity == 4) return ("Bronze", index);
        else if (rarity == 5) return ("Silver", index);
        else if (rarity == 6) return ("Gold", index);
        else if (rarity == 7) return ("Platnium", index);
        else if (rarity == 8) return ("Unobtainium", index);
        else if (rarity == 9) return ("Super Rare", index);
        else if (rarity == 10) return ("Truly Rare", index);
        else if (rarity == 11) return ("Forgotten", index);
        else if (rarity == 12) return ("Secret", index);
        else if (rarity == 13) return ("Singles", index);
        return ("Common", index);
    }

    function getRarityCount() public pure returns (uint8) {
        return 14;
    }

    function GetClass(address warriorAddr, uint8 index)
        public
        view
        returns (string memory)
    {
        (string memory ret, ) = _class(warriorAddr, index);
        return ret;
    }

    function _class(address warriorAddr, uint8 index)
        public
        view
        returns (string memory, uint8)
    {
        uint8 classIndex = IStakeWarsInternals(warriorAddr).getClass(index);
        if (classIndex == 1) return ("Avenger", 1);
        else if (classIndex == 2) return ("Ardent", 2);
        else if (classIndex == 3) return ("Barbarian", 3);
        else if (classIndex == 4) return ("Bard", 4);
        else if (classIndex == 5) return ("Cleric", 5);
        else if (classIndex == 6) return ("Druid", 6);
        else if (classIndex == 7) return ("Fighter", 7);
        else if (classIndex == 8) return ("Monk", 8);
        else if (classIndex == 9) return ("Paladin", 9);
        else if (classIndex == 10) return ("Player", 10);
        else if (classIndex == 11) return ("Psion", 11);
        else if (classIndex == 12) return ("Ranger", 12);
        else if (classIndex == 13) return ("Rogue", 13);
        else if (classIndex == 14) return ("Priest", 14);
        else if (classIndex == 15) return ("Shaman", 15);
        else if (classIndex == 16) return ("Sorcerer", 16);
        else if (classIndex == 17) return ("Warden", 17);
        else if (classIndex == 18) return ("Warlock", 18);
        else if (classIndex == 19) return ("Warlord", 19);
        else if (classIndex == 20) return ("Wizard", 20);
        else return ("Artificer", 0);
    }

    function getClassCount() public pure returns (uint8) {
        return 21;
    }

    function GetLand(address characterAddr, uint8 index)
        public
        view
        returns (string memory)
    {
        (string memory ret, ) = _land(characterAddr, index);
        return ret;
    }

    function _land(address characterAddr, uint8 index)
        public
        view
        returns (string memory, uint8)
    {
        uint8 land = IStakeWarsInternals(characterAddr).getLand(index);
        if (land == 1) return ("Arceus", 1);
        else if (land == 2) return ("Avilon", 2);
        else if (land == 3) return ("Convergence", 3);
        else if (land == 4) return ("The Deep", 4);
        else if (land == 5) return ("Genogia", 5);
        else if (land == 6) return ("Firebrink", 6);
        else if (land == 7) return ("Gilbatree", 7);
        else if (land == 8) return ("Glacia", 8);
        else if (land == 9) return ("Greater Portsmouth", 9);
        else if (land == 10) return ("Hell", 10);
        else if (land == 11) return ("Norvak", 11);
        else if (land == 12) return ("Orlal", 12);
        else if (land == 13) return ("Sartook", 13);
        else if (land == 14) return ("Second Landing", 14);
        else if (land == 15) return ("Tabishan", 15);
        else if (land == 16) return ("Tellbourogh", 16);
        else if (land == 17) return ("North Highlands", 17);
        else if (land == 18) return ("Forgotten", 18);
        else return ("Abyss", 0);
    }

    function getLandCount() public pure returns (uint8) {
        return 19;
    }

    function GetLevels(address characterAddr, address game)
        public
        view
        onlyAfterRelease(characterAddr)
        returns (bytes32)
    {
        IStakeWarsInternals character = IStakeWarsInternals(characterAddr);
        uint256 secret = _securityKey[character.edition()];
        return IStakeWarsInternals(characterAddr).getLevels(game, secret);
    }

    function GetExperience(address characterAddr, address game)
        public
        view
        onlyAfterRelease(characterAddr)
        returns (uint256)
    {
        IStakeWarsInternals character = IStakeWarsInternals(characterAddr);
        uint256 secret = _securityKey[character.edition()];
        return IStakeWarsInternals(characterAddr).GetExperience(game, secret);
    }

    function _setClass(
        address characterAddr,
        uint8 newClass,
        uint8 index
    ) public onlyAdminOrGC {
        IStakeWarsInternals character = IStakeWarsInternals(characterAddr);
        uint256 secret = _securityKey[character.edition()];
        IStakeWarsInternals(characterAddr).setClass(newClass, index, secret);
    }

    function _setLand(
        address characterAddr,
        uint8 newLand,
        uint8 index
    ) public onlyAdminOrGC {
        IStakeWarsInternals character = IStakeWarsInternals(characterAddr);
        uint256 secret = _securityKey[character.edition()];
        IStakeWarsInternals(characterAddr).setLand(newLand, index, secret);
    }

    function _updateExperience(
        address characterAddr,
        address changedExperience,
        uint256 amount,
        bool increase
    ) public onlyAdminOrGC {
        IStakeWarsInternals character = IStakeWarsInternals(characterAddr);
        uint256 secret = _securityKey[character.edition()];
        IStakeWarsInternals(characterAddr).updateExperience(
            changedExperience,
            amount,
            increase,
            secret
        );
    }

    function _setLevel(
        address characterAddr,
        address changedExperience,
        bytes32 value
    ) public onlyAdminOrGC {
        IStakeWarsInternals character = IStakeWarsInternals(characterAddr);
        uint256 secret = _securityKey[character.edition()];
        IStakeWarsInternals(characterAddr).setLevel(
            changedExperience,
            value,
            secret
        );
    }

    modifier onlyAdminOrGC() {
        require(
            hasRole(DEFAULT_ADMIN_ROLE, _msgSender()) ||
                hasRole(GAME_CONTROLLER_ROLE, _msgSender())
        );
        _;
    }

    modifier onlyAfterRelease(address characterAddr) {
        IStakeWarsInternals character = IStakeWarsInternals(characterAddr);
        require(
            character.edition() < Edition ||
                hasRole(DEFAULT_ADMIN_ROLE, _msgSender()) ||
                hasRole(GAME_CONTROLLER_ROLE, _msgSender())
        );
        _;
    }
}

// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

interface IStakeWarsInternals {
    function edition() external view returns (uint256);

    function tokenId() external view returns (uint256);

    function uriGroup() external view returns (uint256);

    function getRaritySeed(uint256 _securityKey)
        external
        view
        returns (uint256);

    function getRarity(uint256 _securityKey)
        external
        view
        returns (uint16, uint16);

    function getLand(uint8 index) external view returns (uint8);

    function getClass(uint8 index) external view returns (uint8);

    function getLevels(address game, uint256 _securityKey)
        external
        view
        returns (bytes32);

    function GetExperience(address game, uint256 securityKey)
        external
        view
        returns (uint256);

    function setClass(
        uint8 newClass,
        uint8 index,
        uint256 _securityKey
    ) external;

    function setLand(
        uint8 newLand,
        uint8 index,
        uint256 _securityKey
    ) external;

    function setLevel(
        address game,
        bytes32 value,
        uint256 _securityKey
    ) external;

    function updateExperience(
        address game,
        uint256 amount,
        bool increase,
        uint256 _securityKey
    ) external;

    function determineClass(uint48 value) external view returns (uint8, uint8);

    function determineLand(uint48 value) external view returns (uint8, uint8);
}

// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;
import "../StakeWarsFactoryUpgradable.sol";

contract StakeWarsFactoryUpgradableMock is StakeWarsFactoryUpgradable {
    uint256 internal counter = 0;

    function getBlockTimestamp() internal view override returns (uint256) {
        uint256 returnCount = counter;
        return returnCount;
    }

    function setBlockTimestamp(uint256 num) public {
        counter = num;
    }
}

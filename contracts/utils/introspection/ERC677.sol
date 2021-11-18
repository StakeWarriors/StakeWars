// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0;

import "./ERC20.sol";

abstract contract ERC677 is ERC20 {
    function transferAndCall(
        address to,
        uint256 value,
        bytes memory data
    ) public virtual returns (bool success);

    event Transfer(
        address indexed from,
        address indexed to,
        uint256 value,
        bytes data
    );
}

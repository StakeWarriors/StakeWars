pragma solidity 0.8.9;

import "./linkERC20.sol";

abstract contract ERC677Mock is linkERC20 {
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

pragma solidity 0.8.9;

abstract contract ERC677ReceiverMock {
    function onTokenTransfer(
        address _sender,
        uint256 _value,
        bytes memory _data
    ) public virtual;
}

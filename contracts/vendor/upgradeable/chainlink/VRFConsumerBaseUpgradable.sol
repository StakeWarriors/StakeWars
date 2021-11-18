// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

import "../openzeppelin/proxy/utils/Initializable.sol";
import "./interfaces/LinkTokenInterface.sol";
import "./VRFRequestIDBase.sol";

abstract contract VRFConsumerBaseUpgradable is VRFRequestIDBase, Initializable {
    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        virtual;

    function requestRandomness(
        bytes32 _keyHash,
        uint256 _fee,
        uint256 _seed
    ) internal returns (bytes32 requestId) {
        LINK.transferAndCall(vrfCoordinator, _fee, abi.encode(_keyHash, _seed));

        uint256 vRFSeed = makeVRFInputSeed(
            _keyHash,
            _seed,
            address(this),
            nonces[_keyHash]
        );

        nonces[_keyHash]++;
        return makeRequestId(_keyHash, vRFSeed);
    }

    // removed immutable keyword <--
    LinkTokenInterface internal LINK;
    // removed immutable keyword <--
    address private vrfCoordinator;

    mapping(bytes32 => uint256) /* keyHash */ /* nonce */
        private nonces;

    // replaced constructor with initializer <--
    function __VRFConsumerBase_init(address _vrfCoordinator, address _link)
        public
        initializer
    {
        __VRFConsumerBase_init_unchained(_vrfCoordinator, _link);
    }

    function __VRFConsumerBase_init_unchained(
        address _vrfCoordinator,
        address _link
    ) public initializer {
        vrfCoordinator = _vrfCoordinator;
        LINK = LinkTokenInterface(_link);
    }

    function rawFulfillRandomness(bytes32 requestId, uint256 randomness)
        external
    {
        require(
            msg.sender == vrfCoordinator,
            "Only VRFCoordinator can fulfill"
        );
        fulfillRandomness(requestId, randomness);
    }
}

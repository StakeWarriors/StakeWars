// SPDX-License-Identifier: MIT
pragma solidity >=0.6.12;

import "./vendor/openzeppelin/access/AccessControl.sol";

contract Administerable is AccessControl {
    bytes32 public constant _GAME_CONTROL_ROLE = hex"0001";
    bytes32 public constant _USER_ROLE = hex"0002";

    /// @dev Add `root` to the admin role as a member.
    constructor(address account) {
        _setupRole(_DEFAULT_ADMIN_ROLE, account);
        _setRoleAdmin(_GAME_CONTROL_ROLE, _DEFAULT_ADMIN_ROLE);
    }

    /// @dev Restricted to members of the admin role.
    modifier onlyAdmin() {
        require(isAdmin(msg.sender));
        _;
    }

    modifier onlyAdminOrGameControl() {
        require(isAdmin(msg.sender) || isGameControl(msg.sender));
        _;
    }

    /// @dev Return `true` if the account belongs to the admin role.
    function isAdmin(address account) public view virtual returns (bool) {
        return hasRole(_DEFAULT_ADMIN_ROLE, account);
    }

    /// @dev Return `true` if the account belongs to the game controller role.
    function isGameControl(address account) public view virtual returns (bool) {
        return hasRole(_GAME_CONTROL_ROLE, account);
    }

    /// @dev Add an account to the admin role. Restricted to admins.
    function addAdmin(address account) public virtual onlyAdmin {
        grantRole(_DEFAULT_ADMIN_ROLE, account);
    }

    /// @dev Add an account to the game controller role. Restricted to admins.
    function addGameControl(address account) public virtual onlyAdmin {
        grantRole(_GAME_CONTROL_ROLE, account);
    }

    /// @dev Remove an account from the game controller role. Restricted to admins.
    function removeGameControl(address account) public virtual onlyAdmin {
        revokeRole(_GAME_CONTROL_ROLE, account);
    }

    /// @dev Remove oneself from the admin role.
    function renounceGameControl() public virtual {
        renounceRole(_GAME_CONTROL_ROLE, msg.sender);
    }

    /// @dev Remove oneself from the admin role.
    function renounceAdmin() public virtual {
        renounceRole(_DEFAULT_ADMIN_ROLE, msg.sender);
    }
}

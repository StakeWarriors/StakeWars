// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;
import "./vendor/upgradeable/openzeppelin/token/ERC721/extensions/ERC721EnumerableUpgradeable.sol";
import "./vendor/upgradeable/openzeppelin/access/AccessControlUpgradeable.sol";
import "./vendor/upgradeable/chainlink/VRFConsumerBaseUpgradable.sol";
import "./vendor/upgradeable/crowdsafe/CrowdSafeV2.sol";
import "./StakeWarsInternals.sol";

contract StakeWarsFactoryUpgradable is
    ERC721EnumerableUpgradeable,
    VRFConsumerBaseUpgradable,
    AccessControlUpgradeable
{
    event Deposit(address indexed _from, uint256 _value);

    uint256 private _tokenIdsGen;
    uint256 private linkFee;
    bytes32 private keyhash;
    uint256 private _generativeSeed;

    uint256 public MaxSupply;
    uint256 public Price; //Matic
    uint256 public Edition;
    string public defaultURI;

    bool public SaleActive;
    bool public PresaleActive;
    uint256 internal _providedSeed;

    string[] private baseURI;
    uint256[] private _securityKey;

    address public crowdSafe;
    address[] public patronArray;
    StakeWarsInternals[] public warriorsToBeDetailed;

    mapping(uint48 => uint256) public rarityRatio;
    mapping(address => uint256) public patronsList;
    mapping(address => uint256) public presaleWhitelist;
    mapping(uint256 => StakeWarsInternals) public tokenIdToStakeWarrior;

    function __StakeWarsFactory_init(
        string memory name,
        string memory symbol,
        uint256 _edition,
        string memory _defaultURI,
        uint256 _MaxSupply,
        address _vrfCoordinator,
        address _linkToken,
        uint256 _linkFee,
        bytes32 _keyhash,
        uint256 securityKey
    ) public initializer {
        __AccessControl_init();
        __ERC721_init(name, symbol);
        __VRFConsumerBase_init(_vrfCoordinator, _linkToken);
        __StakeWarsFactory_init_unchained(
            _edition,
            _defaultURI,
            _MaxSupply,
            _linkFee,
            _keyhash,
            securityKey
        );
    }

    function __StakeWarsFactory_init_unchained(
        uint256 _edition,
        string memory _defaultURI,
        uint256 _MaxSupply,
        uint256 _linkFee,
        bytes32 _keyhash,
        uint256 securityKey
    ) public initializer {
        Edition = _edition;
        defaultURI = _defaultURI;
        linkFee = _linkFee;
        keyhash = _keyhash;
        MaxSupply = _MaxSupply;

        Price = 10 ether; // Matic
        SaleActive = false;
        PresaleActive = false;
        _securityKey.push(securityKey);
        requestRandomness(keyhash, linkFee, securityKey);
    }

    /** This is made virtual for testing capabilities */
    function fulfillRandomness(bytes32, uint256 randomness)
        internal
        virtual
        override
    {
        _providedSeed = randomness;
    }

    function _reserve() public onlyAdminOrGC {
        createMint();
    }

    function mintPresale() public payable {
        uint256 supply = totalSupply();
        uint256 reserved = presaleWhitelist[msg.sender];
        require(PresaleActive, "Presale must be active to mint");
        require(reserved > 0, "No tokens reserved for this address");
        require(
            supply + 1 <= MaxSupply,
            "Purchase would exceed max supply of tokens"
        );
        require(Price == msg.value, "Ether value sent is not correct");
        presaleWhitelist[msg.sender] = reserved - 1;
        if (crowdSafe != address(0)) {
            CrowdSafeV2(crowdSafe).ReportSafeAndShare(msg.sender, 50);
        }
        createMint();
    }

    function mint() public payable {
        require(SaleActive);
        require(totalSupply() + 1 <= MaxSupply);
        require(Price == msg.value);
        if (crowdSafe != address(0)) {
            CrowdSafeV2(crowdSafe).ReportSafeAndShare(msg.sender, 50);
        }
        createMint();
    }

    function createMint() internal {
        require(_providedSeed != 0);
        require(_securityKey.length > 0, "Secret Key Not Set");
        uint256 randomness;
        uint256 secret = _securityKey[_securityKey.length - 1];
        unchecked {
            randomness =
                block.timestamp *
                (_providedSeed + _generativeSeed + secret);

            _generativeSeed = randomness;
        }
        StakeWarsInternals warrior = new StakeWarsInternals(
            Edition,
            randomness,
            _tokenIdsGen,
            baseURI.length,
            secret
        );

        (, uint16 rarity) = warrior.getRarity(secret);

        rarityRatio[uint48(rarity)]++;

        tokenIdToStakeWarrior[_tokenIdsGen] = warrior;
        warriorsToBeDetailed.push(warrior);

        _safeMint(msg.sender, _tokenIdsGen);
        _tokenIdsGen++;
    }

    function warriorsToBeDetailedLength() public view returns (uint256) {
        return warriorsToBeDetailed.length;
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721EnumerableUpgradeable, AccessControlUpgradeable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    function _launchNFTs(uint256 securityKey)
        public
        onlyRole(DEFAULT_ADMIN_ROLE)
    {
        SaleActive = false;
        PresaleActive = false;
        Edition++;
        if (securityKey != _securityKey[_securityKey.length - 1]) {
            requestRandomness(keyhash, linkFee, securityKey);
        }
        _securityKey.push(securityKey);
    }

    function _setBaseURI(uint256 uriGroupIndex, string memory uri)
        public
        onlyAdminOrGC
    {
        require(uriGroupIndex <= baseURI.length);
        while (baseURI.length <= uriGroupIndex) {
            baseURI.push(defaultURI);
        }
        baseURI[uriGroupIndex] = uri;
    }

    function _setDefaultURI(string memory uri)
        public
        onlyRole(DEFAULT_ADMIN_ROLE)
    {
        defaultURI = uri;
    }

    function _setPrice(uint256 newPrice) public onlyRole(DEFAULT_ADMIN_ROLE) {
        Price = newPrice;
    }

    function _setCrowdSafeAddress(address _crowdSafe)
        public
        onlyRole(DEFAULT_ADMIN_ROLE)
    {
        crowdSafe = _crowdSafe;
    }

    function _addPresaleWhitelist(address reservee, uint256 amount)
        public
        onlyRole(DEFAULT_ADMIN_ROLE)
    {
        presaleWhitelist[reservee] = amount;
    }

    function _toggleSaleActive() public onlyRole(DEFAULT_ADMIN_ROLE) {
        SaleActive = !SaleActive;
    }

    function _togglePreSaleActive() public onlyRole(DEFAULT_ADMIN_ROLE) {
        PresaleActive = !PresaleActive;
    }

    function _expandMaxSupply(uint256 _MaxSupply)
        public
        onlyRole(DEFAULT_ADMIN_ROLE)
    {
        // Only to be used in conjunction with a new edition
        // and a subsequent pre-release sale
        MaxSupply = _MaxSupply;
    }

    function tokenURI(uint256 _tokenId)
        public
        view
        override
        returns (string memory)
    {
        StakeWarsInternals thisWarrior = tokenIdToStakeWarrior[_tokenId];
        uint256 myUriGroup = thisWarrior.uriGroup();
        uint256 myEdition = thisWarrior.edition();
        if (myUriGroup < baseURI.length && myEdition < Edition) {
            return
                string(
                    abi.encodePacked(
                        baseURI[myUriGroup],
                        "/",
                        uint2str(thisWarrior.tokenId()),
                        ".json"
                    )
                );
        } else {
            return defaultURI;
        }
    }

    function uint2str(uint256 _i)
        internal
        pure
        returns (string memory _uintAsString)
    {
        if (_i == 0) {
            return "0";
        }
        uint256 j = _i;
        uint256 len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint256 k = len;
        while (_i != 0) {
            k = k - 1;
            uint8 temp = (48 + uint8(_i - (_i / 10) * 10));
            bytes1 b1 = bytes1(temp);
            bstr[k] = b1;
            _i /= 10;
        }
        return string(bstr);
    }

    function getBaseURI() public view onlyAdminOrGC returns (string[] memory) {
        return baseURI;
    }

    function getBaseURILength() public view onlyAdminOrGC returns (uint256) {
        return baseURI.length;
    }

    function GetMyTokenWallet(address owner)
        public
        view
        returns (uint256[] memory)
    {
        if (owner == address(0)) {
            owner = msg.sender;
        }
        uint256 tokenCount = balanceOf(owner);

        uint256[] memory tokensId = new uint256[](tokenCount);
        for (uint256 i; i < tokenCount; i++) {
            tokensId[i] = tokenOfOwnerByIndex(owner, i);
        }
        return tokensId;
    }

    function GetMyStakeWarrior(address owner, uint256 index)
        external
        view
        returns (StakeWarsInternals)
    {
        return tokenIdToStakeWarrior[GetMyTokenWallet(owner)[index]];
    }

    function Donate() public payable {
        // Help Support The Developer(s) to Grow this Operation
        require(msg.value > Price / 20);
        patronsList[msg.sender] += msg.value;
        patronArray.push(msg.sender);
        emit Deposit(msg.sender, msg.value);
    }

    function _resetWarriorsToBeDetails() public {
        delete warriorsToBeDetailed;
    }

    function _withdraw() public onlyRole(DEFAULT_ADMIN_ROLE) {
        payable(msg.sender).transfer(address(this).balance);
        for (
            uint256 patronIndex = 0;
            patronIndex < patronArray.length;
            patronIndex++
        ) {
            address patron = patronArray[patronIndex];
            patronsList[patron] = 0;
        }
    }

    modifier onlyAdminOrGC() {
        require(
            hasRole(DEFAULT_ADMIN_ROLE, _msgSender()) ||
                hasRole(GAME_CONTROLLER_ROLE, _msgSender())
        );
        _;
    }
}

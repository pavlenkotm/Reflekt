// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title ReputationNFT
 * @dev ERC-721 NFT representing Web3 reputation badges
 * @notice Each NFT contains metadata stored on IPFS with reputation score and tier
 */
contract ReputationNFT is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;

    // Mapping from address to token ID (one badge per address)
    mapping(address => uint256) public addressToTokenId;

    // Mapping from token ID to reputation score
    mapping(uint256 => uint256) public tokenReputationScore;

    // Mapping from token ID to reputation tier
    mapping(uint256 => string) public tokenReputationTier;

    // Mapping to track if address has minted
    mapping(address => bool) public hasMinted;

    // Events
    event ReputationBadgeMinted(
        address indexed recipient,
        uint256 indexed tokenId,
        uint256 reputationScore,
        string tier,
        string tokenURI
    );

    event ReputationBadgeUpdated(
        address indexed owner,
        uint256 indexed tokenId,
        uint256 newReputationScore,
        string newTier,
        string newTokenURI
    );

    /**
     * @dev Constructor
     */
    constructor() ERC721("Web3 Reputation Badge", "W3REP") Ownable(msg.sender) {
        // Start token IDs at 1
        _tokenIdCounter.increment();
    }

    /**
     * @dev Mint a new reputation badge
     * @param recipient Address to receive the badge
     * @param tokenURI IPFS URI with metadata
     * @param reputationScore Reputation score (0-100)
     * @param tier Reputation tier (novice, common, uncommon, rare, epic, legendary)
     */
    function mintReputationBadge(
        address recipient,
        string memory tokenURI,
        uint256 reputationScore,
        string memory tier
    ) public onlyOwner returns (uint256) {
        require(recipient != address(0), "Cannot mint to zero address");
        require(reputationScore <= 100, "Score must be <= 100");
        require(!hasMinted[recipient], "Address already has a badge");

        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();

        _safeMint(recipient, tokenId);
        _setTokenURI(tokenId, tokenURI);

        addressToTokenId[recipient] = tokenId;
        tokenReputationScore[tokenId] = reputationScore;
        tokenReputationTier[tokenId] = tier;
        hasMinted[recipient] = true;

        emit ReputationBadgeMinted(recipient, tokenId, reputationScore, tier, tokenURI);

        return tokenId;
    }

    /**
     * @dev Update existing reputation badge
     * @param tokenId Token ID to update
     * @param newTokenURI New IPFS URI with updated metadata
     * @param newReputationScore New reputation score
     * @param newTier New reputation tier
     */
    function updateReputationBadge(
        uint256 tokenId,
        string memory newTokenURI,
        uint256 newReputationScore,
        string memory newTier
    ) public onlyOwner {
        require(_ownerOf(tokenId) != address(0), "Token does not exist");
        require(newReputationScore <= 100, "Score must be <= 100");

        _setTokenURI(tokenId, newTokenURI);
        tokenReputationScore[tokenId] = newReputationScore;
        tokenReputationTier[tokenId] = newTier;

        address owner = ownerOf(tokenId);
        emit ReputationBadgeUpdated(owner, tokenId, newReputationScore, newTier, newTokenURI);
    }

    /**
     * @dev Get reputation data for a token
     * @param tokenId Token ID to query
     * @return score Reputation score
     * @return tier Reputation tier
     * @return uri Token URI
     */
    function getReputationData(uint256 tokenId)
        public
        view
        returns (
            uint256 score,
            string memory tier,
            string memory uri
        )
    {
        require(_ownerOf(tokenId) != address(0), "Token does not exist");

        return (
            tokenReputationScore[tokenId],
            tokenReputationTier[tokenId],
            tokenURI(tokenId)
        );
    }

    /**
     * @dev Get token ID for an address
     * @param owner Address to query
     * @return tokenId Token ID owned by address (0 if none)
     */
    function getTokenIdByAddress(address owner) public view returns (uint256) {
        return addressToTokenId[owner];
    }

    /**
     * @dev Check if an address has a reputation badge
     * @param owner Address to check
     * @return bool True if address has minted a badge
     */
    function hasReputationBadge(address owner) public view returns (bool) {
        return hasMinted[owner];
    }

    /**
     * @dev Get total number of minted badges
     * @return uint256 Total supply
     */
    function totalSupply() public view returns (uint256) {
        return _tokenIdCounter.current() - 1;
    }

    /**
     * @dev Override to prevent token transfers (soulbound)
     * @notice Badges are non-transferable to maintain reputation integrity
     */
    function _update(address to, uint256 tokenId, address auth)
        internal
        override
        returns (address)
    {
        address from = _ownerOf(tokenId);

        // Allow minting (from == address(0))
        // Prevent transfers (from != address(0) && to != address(0))
        // Allow burning (to == address(0))
        require(
            from == address(0) || to == address(0),
            "Reputation badges are non-transferable (soulbound)"
        );

        return super._update(to, tokenId, auth);
    }

    /**
     * @dev Burn a reputation badge
     * @param tokenId Token ID to burn
     * @notice Only owner can burn their own badge
     */
    function burn(uint256 tokenId) public {
        require(ownerOf(tokenId) == msg.sender, "Only owner can burn their badge");

        address owner = ownerOf(tokenId);
        hasMinted[owner] = false;
        delete addressToTokenId[owner];
        delete tokenReputationScore[tokenId];
        delete tokenReputationTier[tokenId];

        _burn(tokenId);
    }

    // Required overrides
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}

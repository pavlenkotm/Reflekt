// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title SimpleToken
 * @dev Basic ERC-20 token with minting capabilities
 * @notice This is a demonstration token for the Web3 Multi-Language showcase
 */
contract SimpleToken is ERC20, Ownable {
    uint8 private _decimals;

    /**
     * @dev Constructor that gives msg.sender all of existing tokens
     * @param name Token name
     * @param symbol Token symbol
     * @param initialSupply Initial supply of tokens (in whole units)
     * @param decimals_ Number of decimals
     */
    constructor(
        string memory name,
        string memory symbol,
        uint256 initialSupply,
        uint8 decimals_
    ) ERC20(name, symbol) Ownable(msg.sender) {
        _decimals = decimals_;
        _mint(msg.sender, initialSupply * 10 ** decimals_);
    }

    /**
     * @dev Returns the number of decimals used for token amounts
     */
    function decimals() public view virtual override returns (uint8) {
        return _decimals;
    }

    /**
     * @dev Mints new tokens to a specified address
     * @param to Address to receive the tokens
     * @param amount Amount of tokens to mint (in smallest unit)
     */
    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    /**
     * @dev Burns tokens from the caller's balance
     * @param amount Amount of tokens to burn (in smallest unit)
     */
    function burn(uint256 amount) public {
        _burn(msg.sender, amount);
    }
}

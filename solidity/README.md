# 💎 Solidity - ERC-20 Token Implementation

A professional ERC-20 token implementation using OpenZeppelin contracts.

## 📋 Overview

`SimpleToken` is a feature-complete ERC-20 token with:
- ✅ Standard ERC-20 interface (transfer, approve, transferFrom)
- ✅ Minting capabilities (owner only)
- ✅ Burning functionality
- ✅ Configurable decimals
- ✅ Access control with Ownable pattern

## 🛠️ Built With

- **Solidity**: ^0.8.20
- **OpenZeppelin Contracts**: Industry-standard secure implementations
- **Hardhat**: Development environment (optional)
- **Foundry**: Testing framework (optional)

## 🚀 Quick Start

### Installation

```bash
# Using Hardhat
npm install --save-dev hardhat
npm install @openzeppelin/contracts

# Or using Foundry
forge install OpenZeppelin/openzeppelin-contracts
```

### Compilation

```bash
# Hardhat
npx hardhat compile

# Foundry
forge build
```

### Deployment

```bash
# Deploy to local network
npx hardhat run scripts/deploy.js --network localhost

# Deploy to testnet (Sepolia)
npx hardhat run scripts/deploy.js --network sepolia
```

## 📖 Contract Interface

### Constructor
```solidity
constructor(
    string memory name,        // Token name (e.g., "My Token")
    string memory symbol,      // Token symbol (e.g., "MTK")
    uint256 initialSupply,     // Initial supply in whole units
    uint8 decimals_            // Decimal places (usually 18)
)
```

### Key Functions

- `mint(address to, uint256 amount)` - Mint new tokens (owner only)
- `burn(uint256 amount)` - Burn tokens from caller's balance
- `transfer(address to, uint256 amount)` - Transfer tokens
- `approve(address spender, uint256 amount)` - Approve spending
- `transferFrom(address from, address to, uint256 amount)` - Transfer on behalf

## 🧪 Testing

```bash
# Run tests with Hardhat
npx hardhat test

# Run tests with Foundry
forge test -vvv
```

## 📊 Example Usage

```javascript
const SimpleToken = await ethers.getContractFactory("SimpleToken");
const token = await SimpleToken.deploy(
    "MyToken",
    "MTK",
    1000000,  // 1 million tokens
    18        // 18 decimals
);

console.log("Token deployed to:", token.address);
```

## 🔒 Security Features

- ✅ Uses audited OpenZeppelin contracts
- ✅ Owner-only minting prevents unauthorized supply inflation
- ✅ SafeMath built into Solidity ^0.8.0
- ✅ Reentrancy protection inherited from ERC-20

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details

## 🔗 Resources

- [OpenZeppelin ERC-20 Docs](https://docs.openzeppelin.com/contracts/4.x/erc20)
- [Ethereum EIP-20](https://eips.ethereum.org/EIPS/eip-20)
- [Solidity Documentation](https://docs.soliditylang.org/)

# JavaScript - Web3.js Examples

Modern JavaScript examples using Web3.js v4 for Ethereum blockchain interaction.

## Overview

This directory demonstrates professional Web3 development patterns using vanilla JavaScript and the Web3.js library - the original and most widely-used Ethereum JavaScript library.

## Features

- Wallet creation and management
- ETH and ERC-20 token operations
- Transaction sending and monitoring
- Message signing and verification
- Contract interaction
- Network utilities

## Installation

```bash
npm install
```

## Usage

### Basic Example

```javascript
const WalletManager = require('./wallet-manager');

const manager = new WalletManager('https://eth.llamarpc.com');

// Create wallet
const wallet = manager.createWallet();
console.log('Address:', wallet.address);

// Get balance
const balance = await manager.getBalance('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0');
console.log('Balance:', balance.balanceEth, 'ETH');

// Sign message
const signature = manager.signMessage(privateKey, 'Hello Web3!');
console.log('Signature:', signature.signature);

// Verify signature
const recovered = manager.recoverAddress('Hello Web3!', signature.signature);
console.log('Recovered address:', recovered);
```

### ERC-20 Tokens

```javascript
// Get token balance
const tokenBalance = await manager.getERC20Balance(
  '0xTokenAddress',
  '0xHolderAddress'
);
console.log('Balance:', tokenBalance.balanceFormatted);
```

### Network Information

```javascript
const networkInfo = await manager.getNetworkInfo();
console.log('Chain ID:', networkInfo.chainId);
console.log('Block:', networkInfo.blockNumber);
console.log('Gas Price:', networkInfo.gasPrice);
```

## Running Tests

```bash
npm test
```

## Key Differences from TypeScript/Ethers.js

| Feature | Web3.js | Ethers.js |
|---------|---------|-----------|
| Library Size | Larger | Smaller |
| API Style | Callback-first (v1), Promise (v4) | Promise-first |
| Provider Pattern | Web3Provider | BrowserProvider |
| Contract Calls | `.call()` | Direct function calls |
| Unit Conversion | `utils.fromWei()` | `formatEther()` |
| Signing | `accounts.sign()` | `signer.signMessage()` |

## API Reference

### WalletManager

#### Constructor
- `new WalletManager(rpcUrl)` - Create manager instance

#### Wallet Operations
- `createWallet()` - Generate new wallet
- `getBalance(address)` - Get ETH balance
- `sendTransaction(privateKey, to, value)` - Send ETH

#### Signing
- `signMessage(privateKey, message)` - Sign message
- `recoverAddress(message, signature)` - Recover signer

#### Network
- `getNetworkInfo()` - Get chain info
- `getBlock(number)` - Get block data
- `getTransaction(hash)` - Get transaction

#### Tokens
- `getERC20Balance(token, holder)` - Get token balance

#### Utilities
- `isValidAddress(address)` - Validate address
- `toChecksumAddress(address)` - Checksum address
- `keccak256(data)` - Hash data
- `toEther(wei)` / `toWei(ether)` - Convert units

## Best Practices

1. **Always validate addresses** before sending transactions
2. **Use checksummed addresses** for better security
3. **Handle errors** from network calls gracefully
4. **Never expose private keys** in production code
5. **Test on testnet** before mainnet deployment

## Web3.js v4 vs v1

This code uses Web3.js v4 (latest), which has breaking changes from v1:

```javascript
// v1 (Old)
const Web3 = require('web3');
const web3 = new Web3('http://localhost:8545');
web3.eth.getBalance('0x...').then(console.log);

// v4 (New)
const { Web3 } = require('web3');
const web3 = new Web3('http://localhost:8545');
const balance = await web3.eth.getBalance('0x...');
```

## Resources

- [Web3.js Documentation](https://docs.web3js.org/)
- [Ethereum JavaScript API](https://ethereum.org/en/developers/docs/apis/javascript/)
- [Web3.js GitHub](https://github.com/web3/web3.js)

## License

MIT

# 📘 TypeScript - Web3 Wallet & Contract Utilities

Modern TypeScript utilities for Web3 development with Ethers.js and Viem, demonstrating best practices for DApp frontend development.

## 📋 Overview

This module provides:
- ✅ Wallet connection (MetaMask, WalletConnect)
- ✅ Transaction signing and sending
- ✅ Smart contract interaction helpers
- ✅ Type-safe contract calls
- ✅ Event listening and filtering
- ✅ Modern Viem client integration
- ✅ Utility functions for common operations

## 🛠️ Built With

- **TypeScript**: 5.3+
- **Ethers.js**: 6.10+ (most popular Ethereum library)
- **Viem**: 2.7+ (modern alternative, better performance)
- **Node.js**: 18+

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
npm install

# Or with yarn
yarn install

# Or with pnpm
pnpm install
```

### Build

```bash
# Compile TypeScript
npm run build

# Development mode with watch
npm run dev

# Run linter
npm run lint

# Format code
npm run format
```

## 📖 API Reference

### WalletConnector

Main class for wallet interactions.

```typescript
import { WalletConnector } from './wallet-connect';

const wallet = new WalletConnector();

// Connect to MetaMask
const info = await wallet.connectMetaMask();
console.log(info.address, info.balance);

// Send transaction
const txHash = await wallet.sendTransaction({
  to: '0x...',
  value: '0.1', // ETH
});

// Sign message
const signature = await wallet.signMessage('Hello Web3!');

// Switch network
await wallet.switchNetwork(137); // Polygon

// Disconnect
wallet.disconnect();
```

### ContractInteractor

Type-safe smart contract interactions.

```typescript
import { ContractInteractor } from './wallet-connect';
import { ethers } from 'ethers';

const erc20Abi = [
  'function balanceOf(address) view returns (uint256)',
  'function transfer(address to, uint256 amount) returns (bool)',
  'event Transfer(address indexed from, address indexed to, uint256 value)',
];

const contract = new ContractInteractor(
  '0xTokenAddress',
  erc20Abi,
  signer
);

// Read from contract
const balance = await contract.call<bigint>('balanceOf', userAddress);

// Write to contract
const receipt = await contract.send('transfer', recipientAddress, ethers.parseEther('10'));

// Listen to events
contract.onEvent('Transfer', (from, to, value) => {
  console.log(`Transfer: ${from} -> ${to}, Amount: ${value}`);
});

// Query past events
const events = await contract.getPastEvents('Transfer', 0, 'latest');
```

### ViemClient

Modern alternative using Viem (better performance).

```typescript
import { ViemClient } from './wallet-connect';
import { mainnet } from 'viem/chains';

const client = new ViemClient(mainnet);

// Get balance
const balance = await client.getBalance('0x...');

// Get block number
const blockNumber = await client.getBlockNumber();

// Read from contract
const result = await client.readContract({
  address: '0x...',
  abi: erc20Abi,
  functionName: 'balanceOf',
  args: ['0xUserAddress'],
});

// Watch blocks
client.watchBlocks((blockNumber) => {
  console.log('New block:', blockNumber);
});
```

### Utility Functions

```typescript
import { utils } from './wallet-connect';

// Validate address
const isValid = utils.isValidAddress('0x...');

// Format values
const eth = utils.formatEther('1000000000000000000'); // "1.0"
const wei = utils.parseEther('1.5'); // 1500000000000000000n

// Estimate gas
const gasCost = await utils.estimateGas(provider, {
  to: '0x...',
  value: ethers.parseEther('1'),
});

// Generate wallet
const newWallet = utils.generateWallet();
console.log(newWallet.address, newWallet.mnemonic);
```

## 🧪 Testing

```bash
# Run tests
npm test

# With coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

Example test:
```typescript
import { WalletConnector, utils } from './wallet-connect';

describe('WalletConnector', () => {
  it('should validate Ethereum addresses', () => {
    expect(utils.isValidAddress('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb')).toBe(true);
    expect(utils.isValidAddress('invalid')).toBe(false);
  });

  it('should format ether correctly', () => {
    expect(utils.formatEther('1000000000000000000')).toBe('1.0');
  });
});
```

## 📊 Integration Examples

### React Integration

```typescript
import { useState, useEffect } from 'react';
import { WalletConnector } from './wallet-connect';

function WalletButton() {
  const [wallet, setWallet] = useState<WalletConnector | null>(null);
  const [address, setAddress] = useState<string>('');

  const connect = async () => {
    const w = new WalletConnector();
    const info = await w.connectMetaMask();
    setWallet(w);
    setAddress(info.address);
  };

  return (
    <div>
      {address ? (
        <p>Connected: {address.slice(0, 6)}...{address.slice(-4)}</p>
      ) : (
        <button onClick={connect}>Connect Wallet</button>
      )}
    </div>
  );
}
```

### Wagmi Hook Pattern

```typescript
import { useAccount, useConnect, useDisconnect } from 'wagmi';
import { InjectedConnector } from 'wagmi/connectors/injected';

function App() {
  const { address, isConnected } = useAccount();
  const { connect } = useConnect({
    connector: new InjectedConnector(),
  });
  const { disconnect } = useDisconnect();

  return (
    <div>
      {isConnected ? (
        <>
          <p>Connected: {address}</p>
          <button onClick={() => disconnect()}>Disconnect</button>
        </>
      ) : (
        <button onClick={() => connect()}>Connect Wallet</button>
      )}
    </div>
  );
}
```

## 🔒 Security Best Practices

- ✅ Never expose private keys in frontend code
- ✅ Always validate addresses before transactions
- ✅ Use hardware wallets for production
- ✅ Implement transaction simulation before sending
- ✅ Add slippage protection for trades
- ✅ Verify contract addresses and ABIs

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details

## 🔗 Resources

- [Ethers.js Documentation](https://docs.ethers.org/v6/)
- [Viem Documentation](https://viem.sh/)
- [Wagmi Documentation](https://wagmi.sh/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Web3Modal](https://web3modal.com/)

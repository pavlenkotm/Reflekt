# Cairo - StarkNet Smart Contracts

## Overview

Cairo is a Turing-complete programming language for writing provable programs on StarkNet, a validity rollup (ZK-Rollup) that scales Ethereum using STARK cryptographic proofs.

## Features

- **Zero-Knowledge Proofs**: Built-in support for STARK proofs
- **Cairo VM**: Custom virtual machine optimized for proving
- **Account Abstraction**: Native support for account abstraction
- **Gas Efficiency**: Exponentially cheaper than L1 Ethereum
- **Provable Computation**: All execution is cryptographically proven

## Project Structure

```
cairo/
├── src/
│   ├── erc20.cairo         # ERC-20 token implementation
│   ├── vault.cairo         # Token vault with staking
│   └── nft.cairo           # ERC-721 NFT contract
├── tests/
│   └── test_erc20.cairo    # Token tests
├── Scarb.toml              # Package configuration
└── README.md
```

## Installation

### Prerequisites

```bash
# Install Scarb (Cairo package manager)
curl --proto '=https' --tlsv1.2 -sSf https://docs.swmansion.com/scarb/install.sh | sh

# Verify installation
scarb --version
```

### Dependencies

```bash
# Install project dependencies
scarb build

# Run tests
scarb test
```

## Smart Contracts

### 1. ERC-20 Token (`src/erc20.cairo`)

A standard fungible token implementation following the StarkNet ERC-20 standard.

**Features:**
- Minting and burning
- Transfer and approve
- Balance queries
- Events emission

**Usage:**
```bash
# Build the contract
scarb build

# Deploy to StarkNet testnet
starkli deploy target/dev/reflekt_cairo_ERC20Token.sierra.json \
    --rpc https://starknet-goerli.g.alchemy.com/v2/YOUR_KEY
```

### 2. Token Vault (`src/vault.cairo`)

A secure vault for staking tokens with rewards.

**Features:**
- Deposit and withdraw tokens
- Reward calculation
- Emergency withdrawal
- Access control

### 3. NFT Contract (`src/nft.cairo`)

ERC-721 compliant NFT with metadata support.

**Features:**
- Minting with URI
- Transfer and approval
- Enumerable support
- Royalty info

## Development

### Build

```bash
# Compile contracts
scarb build

# Format code
scarb fmt
```

### Testing

```bash
# Run all tests
scarb test

# Run specific test
scarb test test_transfer

# Run with coverage
scarb test --coverage
```

### Deployment

```bash
# Deploy to testnet
starkli deploy \
    target/dev/reflekt_cairo_ERC20Token.sierra.json \
    --rpc $STARKNET_RPC_URL \
    --account ~/.starkli-wallets/deployer/account.json \
    --keystore ~/.starkli-wallets/deployer/keystore.json
```

## StarkNet Ecosystem

### Networks

- **Mainnet**: Production network
- **Goerli Testnet**: Public testing network
- **Sepolia Testnet**: Alternative testnet
- **Local Devnet**: Development environment

### RPC Providers

- [Alchemy StarkNet](https://www.alchemy.com/starknet)
- [Infura StarkNet](https://www.infura.io/networks/ethereum/starknet)
- [Blast API](https://blastapi.io/public-api/starknet)

### Tools

- **Scarb**: Package manager and build tool
- **Starkli**: CLI for StarkNet interactions
- **Cairo Profiler**: Performance analysis
- **Starknet Foundry**: Testing framework

## Cairo Language Features

### 1. Felt Type

```cairo
// Felt (Field Element) - fundamental type
let value: felt252 = 42;
```

### 2. Storage

```cairo
#[storage]
struct Storage {
    balances: LegacyMap<ContractAddress, u256>,
    total_supply: u256,
}
```

### 3. Events

```cairo
#[event]
#[derive(Drop, starknet::Event)]
enum Event {
    Transfer: Transfer,
}
```

### 4. External Functions

```cairo
#[external(v0)]
fn transfer(ref self: ContractState, recipient: ContractAddress, amount: u256) {
    // Implementation
}
```

## Security Best Practices

1. **Input Validation**: Always validate inputs
2. **Access Control**: Implement proper authorization
3. **Reentrancy Protection**: Use checks-effects-interactions pattern
4. **Integer Overflow**: Use safe math operations
5. **Event Logging**: Emit events for state changes

## Gas Optimization

- Use `LegacyMap` for storage efficiency
- Minimize storage operations
- Batch operations when possible
- Use appropriate data types

## Resources

- [Cairo Book](https://book.cairo-lang.org/)
- [StarkNet Documentation](https://docs.starknet.io/)
- [Cairo by Example](https://cairo-by-example.com/)
- [StarkNet Community](https://community.starknet.io/)
- [OpenZeppelin Cairo Contracts](https://github.com/OpenZeppelin/cairo-contracts)

## License

MIT License - See LICENSE file for details

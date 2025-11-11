# Sway - Fuel Network Smart Contracts

## Overview

Sway is a domain-specific language (DSL) for the Fuel Virtual Machine (FuelVM), designed for high-throughput blockchain execution with UTXO-based architecture and Rust-like syntax.

## Features

- **Rust-Inspired Syntax**: Familiar to Rust developers
- **UTXO Model**: Parallel transaction execution
- **Native Assets**: First-class asset support
- **Predicates**: Stateless validation logic
- **Scripts**: Flexible transaction execution
- **FuelVM**: High-performance virtual machine

## Project Structure

```
sway/
├── src/
│   ├── main.sw             # Token contract
│   ├── vault.sw            # Token vault
│   └── dex.sw              # Decentralized exchange
├── tests/
│   └── harness.rs          # Rust test harness
├── Forc.toml               # Package configuration
└── README.md
```

## Installation

### Prerequisites

```bash
# Install fuelup (Fuel toolchain manager)
curl https://install.fuel.network | sh

# Install Fuel toolchain
fuelup toolchain install latest
fuelup default latest

# Verify installation
forc --version
fuel-core --version
```

### Dependencies

```bash
# Build the project
forc build

# Run tests
forc test
```

## Smart Contracts

### 1. Token Contract (`src/main.sw`)

A native asset token implementation using Fuel's native asset system.

**Features:**
- Minting and burning
- Transfer operations
- Balance queries
- Multi-asset support

**Usage:**
```bash
# Build the contract
forc build

# Deploy to testnet
forc deploy --testnet

# Run local node
fuel-core run --db-type in-memory --debug
```

### 2. Token Vault (`src/vault.sw`)

A secure vault for staking native assets.

**Features:**
- Deposit and withdraw
- Reward distribution
- Time-locked withdrawals
- Multi-asset vaults

### 3. DEX Contract (`src/dex.sw`)

Automated market maker for token swaps.

**Features:**
- Liquidity pools
- Token swaps
- Price oracles
- Fee distribution

## Development

### Build

```bash
# Compile contracts
forc build

# Clean build artifacts
forc clean

# Format code
forc fmt
```

### Testing

```bash
# Run all tests
forc test

# Run with output
forc test -- --nocapture

# Run specific test
cargo test --package sway-contract test_mint
```

### Deployment

```bash
# Deploy to local node
forc deploy --node-url http://127.0.0.1:4000

# Deploy to testnet
forc deploy --testnet

# Deploy to mainnet (use with caution)
forc deploy --mainnet
```

## Fuel Ecosystem

### Networks

- **Mainnet Beta**: Production network
- **Testnet**: Public testing network
- **Local Node**: Development environment

### RPC Providers

- [Fuel Labs RPC](https://beta-5.fuel.network/)
- [Fuel Testnet](https://testnet.fuel.network/)

### Tools

- **Forc**: Fuel Orchestrator (build tool)
- **Fuel Core**: Full node implementation
- **Fuel Indexer**: Event indexing
- **Sway LSP**: Language server

## Sway Language Features

### 1. Storage

```sway
storage {
    balances: StorageMap<Identity, u64> = StorageMap {},
    total_supply: u64 = 0,
}
```

### 2. ABI Definition

```sway
abi Token {
    #[storage(read, write)]
    fn mint(amount: u64);

    #[storage(read)]
    fn balance_of(owner: Identity) -> u64;
}
```

### 3. Native Assets

```sway
let asset_id = msg_asset_id();
let amount = msg_amount();
transfer(to, asset_id, amount);
```

### 4. Predicates

```sway
predicate;

fn main(recipient: Address) -> bool {
    let sender: b256 = tx_witness_data(0);
    sender == recipient.into()
}
```

## Security Best Practices

1. **Asset Safety**: Always verify asset IDs
2. **Reentrancy**: Use checks-effects-interactions
3. **Access Control**: Implement proper authorization
4. **Input Validation**: Validate all inputs
5. **Gas Limits**: Set appropriate gas limits

## Gas Optimization

- Minimize storage operations
- Use efficient data structures
- Batch operations
- Optimize predicate logic

## Fuel VM Advantages

- **Parallel Execution**: UTXO-based parallelism
- **Native Assets**: No need for token standards
- **Predicates**: Stateless validation
- **Low Latency**: Fast block times
- **Developer Experience**: Rust-like syntax

## Resources

- [Sway Book](https://docs.fuel.network/docs/sway/)
- [Fuel Network Docs](https://docs.fuel.network/)
- [Sway by Example](https://swaybyexample.com/)
- [Fuel Forum](https://forum.fuel.network/)
- [Sway Standards](https://github.com/FuelLabs/sway-standards)

## License

MIT License - See LICENSE file for details

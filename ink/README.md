# 🦑 Ink! - Polkadot Smart Contracts

Rust-based eDSL for writing secure and efficient smart contracts on Polkadot and Substrate-based blockchains, compiling to WebAssembly (Wasm).

## 📋 Overview

Ink! is Parity's answer to smart contract development for the Polkadot ecosystem. Built on Rust, it offers:

- **Type Safety**: Rust's strong type system prevents common vulnerabilities
- **Performance**: Compiles to optimized WebAssembly bytecode
- **Developer Experience**: Familiar Rust syntax with smart contract primitives
- **Interoperability**: Works across all Substrate-based parachains
- **Small Footprint**: Minimal contract sizes due to Wasm efficiency

## ✨ Key Features

- ✅ **ERC-20 Compatible**: Standard token interface implementation
- ✅ **Event System**: Emit and index blockchain events
- ✅ **Storage Optimization**: Efficient key-value storage with `Mapping`
- ✅ **Built-in Testing**: Unit tests and E2E test framework
- ✅ **Error Handling**: Rust's `Result<T, E>` for safe error propagation
- ✅ **Access Control**: Easy implementation of ownership patterns
- ✅ **Upgradeable**: Support for proxy patterns and contract upgrades
- ✅ **Cross-Contract Calls**: Native support for calling other contracts

## 📁 Project Structure

```
ink/
├── src/
│   └── lib.rs              # Main ERC-20 token contract
├── Cargo.toml              # Project configuration
└── README.md               # This file
```

## 🚀 Installation

### Prerequisites

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Add WebAssembly target
rustup target add wasm32-unknown-unknown

# Install cargo-contract
cargo install cargo-contract --force
```

### Install Dependencies

```bash
cd ink
cargo contract build
```

## 🏗️ Build & Deploy

### Build Contract

```bash
# Build in debug mode
cargo contract build

# Build in release mode (optimized)
cargo contract build --release
```

This generates:
- `target/ink/erc20.wasm` - WebAssembly bytecode
- `target/ink/erc20.json` - Contract metadata
- `target/ink/erc20.contract` - Bundle for deployment

### Deploy to Local Node

```bash
# Start a local Substrate node with contracts pallet
substrate-contracts-node --dev

# Deploy contract
cargo contract instantiate \
  --constructor new \
  --args 1000000 \
  --suri //Alice \
  --skip-confirm
```

### Deploy to Testnet

```bash
# Deploy to Rococo Contracts (testnet)
cargo contract instantiate \
  --constructor new \
  --args 1000000 \
  --url wss://rococo-contracts-rpc.polkadot.io \
  --suri "your mnemonic phrase here" \
  --skip-confirm
```

## 🧪 Testing

### Unit Tests

```bash
# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test transfer_works
```

### E2E Tests

```bash
# Run end-to-end tests (requires running node)
cargo test --features e2e-tests
```

## 📖 Smart Contract: ERC-20 Token

### Overview

Full-featured ERC-20 token implementation with:
- Transfer tokens between accounts
- Approve spending allowances
- Mint new tokens
- Burn existing tokens

### Constructor

```rust
#[ink(constructor)]
pub fn new(total_supply: Balance) -> Self
```

**Example:**
```bash
# Create token with 1,000,000 supply
cargo contract instantiate --args 1000000 --constructor new
```

### Core Functions

#### 1. `total_supply() -> Balance`

Returns the total token supply.

```rust
let supply = contract.total_supply();
```

#### 2. `balance_of(owner: AccountId) -> Balance`

Returns the balance of an account.

```rust
let balance = contract.balance_of(alice);
```

#### 3. `transfer(to: AccountId, value: Balance) -> Result<()>`

Transfer tokens to another account.

```rust
contract.transfer(bob, 100)?;
```

#### 4. `approve(spender: AccountId, value: Balance) -> Result<()>`

Approve another account to spend tokens on your behalf.

```rust
contract.approve(charlie, 500)?;
```

#### 5. `transfer_from(from: AccountId, to: AccountId, value: Balance) -> Result<()>`

Transfer tokens on behalf of another account (requires approval).

```rust
contract.transfer_from(alice, bob, 100)?;
```

#### 6. `mint(to: AccountId, value: Balance) -> Result<()>`

Mint new tokens (⚠️ Add access control in production).

```rust
contract.mint(alice, 1000)?;
```

#### 7. `burn(value: Balance) -> Result<()>`

Burn tokens from caller's account.

```rust
contract.burn(500)?;
```

### Events

```rust
// Emitted on transfer
Transfer {
    from: Option<AccountId>,
    to: Option<AccountId>,
    value: Balance,
}

// Emitted on approval
Approval {
    owner: AccountId,
    spender: AccountId,
    value: Balance,
}
```

## 💡 Ink! Language Features

### 1. Storage

```rust
#[ink(storage)]
pub struct MyContract {
    value: i32,
    owner: AccountId,
    balances: Mapping<AccountId, Balance>,
}
```

### 2. Messages (Functions)

```rust
// Read-only message
#[ink(message)]
pub fn get_value(&self) -> i32 {
    self.value
}

// State-changing message
#[ink(message)]
pub fn set_value(&mut self, new_value: i32) {
    self.value = new_value;
}
```

### 3. Events

```rust
#[ink(event)]
pub struct ValueChanged {
    #[ink(topic)]
    old_value: i32,
    #[ink(topic)]
    new_value: i32,
}

// Emit event
self.env().emit_event(ValueChanged { old_value, new_value });
```

### 4. Error Handling

```rust
#[derive(Debug, PartialEq, Eq)]
#[ink::scale_derive(Encode, Decode, TypeInfo)]
pub enum Error {
    InsufficientBalance,
    Unauthorized,
}

pub type Result<T> = core::result::Result<T, Error>;
```

### 5. Cross-Contract Calls

```rust
use other_contract::OtherContractRef;

let other = OtherContractRef::from_account_id(contract_id);
other.some_function()?;
```

## 🔧 Development Tips

### Access Caller

```rust
let caller = self.env().caller();
```

### Access Contract Balance

```rust
let balance = self.env().balance();
```

### Transfer Native Token

```rust
self.env().transfer(recipient, amount)?;
```

### Get Block Number

```rust
let block = self.env().block_number();
```

## 🔒 Security Best Practices

1. **✅ Check-Effects-Interactions Pattern**
   - Always update state before external calls
   ```rust
   self.balances.insert(caller, new_balance);  // State change first
   self.external_call()?;                       // External call last
   ```

2. **✅ Use `Result<T, E>` for Error Handling**
   - Never use `.unwrap()` in production code
   - Always propagate errors with `?`

3. **✅ Implement Access Control**
   ```rust
   fn only_owner(&self) -> Result<()> {
       if self.env().caller() != self.owner {
           return Err(Error::Unauthorized);
       }
       Ok(())
   }
   ```

4. **✅ Validate Inputs**
   ```rust
   if amount == 0 {
       return Err(Error::InvalidAmount);
   }
   ```

5. **✅ Test Extensively**
   - Write unit tests for all functions
   - Use E2E tests for integration scenarios
   - Test edge cases and failure modes

6. **✅ Use Storage Efficiently**
   - `Mapping` is gas-efficient for key-value storage
   - Avoid storing large data structures
   - Consider lazy loading for large datasets

## ⚡ Gas Optimization

1. **Minimize Storage Operations**
   ```rust
   // Bad: Multiple reads
   let balance = self.balances.get(account);
   let new_balance = balance + amount;
   self.balances.insert(account, new_balance);

   // Good: Single read and write
   let balance = self.balances.get(account).unwrap_or(0);
   self.balances.insert(account, &(balance + amount));
   ```

2. **Use `Lazy<T>` for Rarely Used Data**
   ```rust
   use ink::storage::Lazy;

   #[ink(storage)]
   pub struct Contract {
       config: Lazy<Config>,
   }
   ```

3. **Batch Operations**
   - Process multiple operations in single transaction
   - Reduces overhead of multiple calls

4. **Avoid Loops Over Unbounded Data**
   - Use pagination for large datasets
   - Limit iteration counts

## 🆚 Ink! vs Other Smart Contract Languages

| Feature | Ink! (Polkadot) | Solidity (Ethereum) | Move (Aptos/Sui) |
|---------|-----------------|---------------------|------------------|
| Language | Rust eDSL | JavaScript-like | Move |
| Type Safety | ✅ Strong | ⚠️ Moderate | ✅ Strong |
| Memory Safety | ✅ Rust guarantees | ❌ Manual | ✅ Resource-based |
| Compilation | Wasm | EVM bytecode | MoveVM bytecode |
| Contract Size | Small (Wasm) | Moderate | Small |
| Gas Efficiency | ⚡ High | Moderate | ⚡ High |
| Learning Curve | Steep (Rust) | Moderate | Steep |
| Ecosystem | Growing | Mature | Emerging |
| Tooling | cargo-contract | Hardhat/Foundry | Move CLI |

## 🌐 Ecosystem Integration

### Supported Chains

- **Polkadot**: Main relay chain
- **Kusama**: Canary network
- **Astar**: DApp hub for Polkadot
- **Aleph Zero**: Privacy-focused chain
- **Phala Network**: Confidential smart contracts
- **Moonbeam**: Ethereum-compatible parachain
- **Any Substrate chain** with contracts pallet

### Frontend Integration

```javascript
// Using Polkadot.js API
import { ApiPromise, WsProvider } from '@polkadot/api';
import { ContractPromise } from '@polkadot/api-contract';

const wsProvider = new WsProvider('wss://rpc.polkadot.io');
const api = await ApiPromise.create({ provider: wsProvider });

// Load contract
const contract = new ContractPromise(api, metadata, contractAddress);

// Call read-only method
const { output } = await contract.query.balanceOf(
  callerAddress,
  { gasLimit: -1 },
  targetAddress
);

// Send transaction
await contract.tx.transfer(
  { gasLimit: -1 },
  recipientAddress,
  amount
).signAndSend(signer);
```

## 📚 Advanced Topics

### Contract Upgrades

```rust
// Use delegated execution pattern
#[ink(message)]
pub fn set_code(&mut self, code_hash: [u8; 32]) -> Result<()> {
    self.only_owner()?;
    ink::env::set_code_hash(&code_hash)?;
    Ok(())
}
```

### Proxy Patterns

```rust
// Minimal proxy contract
#[ink(storage)]
pub struct Proxy {
    admin: AccountId,
    implementation: AccountId,
}
```

### Custom Chain Extensions

```rust
#[ink::chain_extension]
pub trait RandomnessExtension {
    #[ink(extension = 1)]
    fn random() -> [u8; 32];
}
```

## 🛠️ Useful Commands

```bash
# Check contract
cargo contract check

# Build optimized contract
cargo contract build --release

# Generate contract metadata
cargo metadata --format-version 1

# Estimate gas
cargo contract instantiate --gas-limit 100000000000

# Call contract method
cargo contract call \
  --contract <ADDRESS> \
  --message transfer \
  --args <RECIPIENT> <AMOUNT>

# Upload code (without instantiating)
cargo contract upload --suri //Alice
```

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details

## 🔗 Resources

- **Official Docs**: https://use.ink/
- **GitHub**: https://github.com/paritytech/ink
- **Examples**: https://github.com/paritytech/ink-examples
- **cargo-contract**: https://github.com/paritytech/cargo-contract
- **Substrate Contracts**: https://docs.substrate.io/tutorials/smart-contracts/
- **Polkadot.js**: https://polkadot.js.org/docs/
- **Ink! Playground**: https://ink-playground.substrate.io/
- **Community**: https://substrate.stackexchange.com/

## 🎓 Learning Path

1. **Learn Rust**: https://doc.rust-lang.org/book/
2. **Ink! Basics**: https://use.ink/basics/contract-template
3. **Build Examples**: https://github.com/paritytech/ink-examples
4. **Deploy on Testnet**: Rococo Contracts Parachain
5. **Join Community**: Substrate Stack Exchange

---

**Built with ❤️ for the Polkadot Ecosystem**

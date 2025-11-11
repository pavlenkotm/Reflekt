# Fe - Python-Inspired EVM Smart Contracts

## Overview

Fe is a statically typed smart contract language for the Ethereum Virtual Machine (EVM), inspired by Python and Rust. It aims to provide a safer and more developer-friendly alternative to Solidity.

## Features

- **Python-like Syntax**: Familiar and readable
- **Static Typing**: Catch errors at compile time
- **Memory Safety**: No undefined behavior
- **EVM Compatible**: Runs on all EVM chains
- **Auditable**: Simple and explicit
- **Gas Efficient**: Optimized compilation

## Project Structure

```
fe/
├── src/
│   ├── token.fe            # ERC-20 token
│   ├── vault.fe            # Token vault
│   └── nft.fe              # ERC-721 NFT
├── tests/
│   └── test_token.py       # Python tests
├── fe.toml                 # Project configuration
└── README.md
```

## Installation

### Prerequisites

```bash
# Install Fe compiler
curl -L https://github.com/ethereum/fe/releases/latest/download/fe_amd64 -o fe
chmod +x fe
sudo mv fe /usr/local/bin/

# Verify installation
fe --version
```

### Dependencies

```bash
# Build the project
fe build

# Run tests
fe test
```

## Smart Contracts

### 1. Token Contract (`src/token.fe`)

A standard ERC-20 fungible token implementation.

**Features:**
- Minting and burning
- Transfer and approve
- Balance queries
- Event emissions

**Usage:**
```bash
# Compile contract
fe build src/token.fe

# Output will be in output/token/

# Deploy using foundry
forge create --contracts output/token/token.bin \
    --constructor-args "MyToken" "MTK" 1000000
```

### 2. Token Vault (`src/vault.fe`)

A secure vault for staking ERC-20 tokens.

**Features:**
- Deposit and withdraw
- Reward calculation
- Time locks
- Emergency functions

### 3. NFT Contract (`src/nft.fe`)

ERC-721 compliant NFT implementation.

**Features:**
- Minting with metadata
- Transfer and approval
- Ownership tracking
- URI storage

## Development

### Build

```bash
# Compile all contracts
fe build

# Compile specific contract
fe build src/token.fe

# Output ABI and bytecode
fe build --emit abi,bytecode
```

### Testing

```bash
# Run tests
fe test

# Run with output
fe test --verbose

# Run specific test
pytest tests/test_token.py::test_transfer
```

### Deployment

```bash
# Using Foundry
forge create \
    --contracts output/token/token.bin \
    --constructor-args "Token" "TKN" 1000000 \
    --rpc-url $RPC_URL \
    --private-key $PRIVATE_KEY

# Using Hardhat
npx hardhat run scripts/deploy-fe.js --network mainnet
```

## Fe Language Features

### 1. Contract Definition

```fe
contract Token:
    _balances: Map<address, u256>
    _total_supply: u256

    pub fn __init__(mut self, initial_supply: u256):
        self._total_supply = initial_supply
        self._balances[msg.sender] = initial_supply
```

### 2. Public Functions

```fe
pub fn transfer(mut self, to: address, amount: u256) -> bool:
    assert msg.sender != address(0), "zero address"
    assert self._balances[msg.sender] >= amount, "insufficient balance"

    self._balances[msg.sender] -= amount
    self._balances[to] += amount

    emit Transfer(sender: msg.sender, recipient: to, value: amount)
    return true
```

### 3. Events

```fe
event Transfer:
    idx sender: address
    idx recipient: address
    value: u256

event Approval:
    idx owner: address
    idx spender: address
    value: u256
```

### 4. Modifiers (via functions)

```fe
fn require_owner(self):
    assert msg.sender == self._owner, "not owner"

pub fn mint(mut self, to: address, amount: u256):
    self.require_owner()
    self._mint(to, amount)
```

## Security Best Practices

1. **Explicit Assertions**: Always use assert for conditions
2. **Integer Safety**: Fe prevents overflow by default
3. **Access Control**: Implement owner checks
4. **Input Validation**: Validate all external inputs
5. **Event Logging**: Emit events for state changes

## Gas Optimization

- Use appropriate integer types (u8, u16, u32, u64, u128, u256)
- Minimize storage operations
- Pack storage variables
- Use memory for temporary data

## Fe vs Solidity

### Advantages of Fe:

1. **Simpler Syntax**: Python-like, easier to read
2. **No Undefined Behavior**: Safer by design
3. **Better Error Messages**: More helpful compiler errors
4. **Explicit Memory Management**: Clear data locations
5. **Modern Language Design**: Incorporates lessons learned

### Example Comparison:

**Solidity:**
```solidity
function transfer(address to, uint256 amount) public returns (bool) {
    require(balances[msg.sender] >= amount, "Insufficient balance");
    balances[msg.sender] -= amount;
    balances[to] += amount;
    emit Transfer(msg.sender, to, amount);
    return true;
}
```

**Fe:**
```fe
pub fn transfer(mut self, to: address, amount: u256) -> bool:
    assert self._balances[msg.sender] >= amount, "insufficient balance"
    self._balances[msg.sender] -= amount
    self._balances[to] += amount
    emit Transfer(sender: msg.sender, recipient: to, value: amount)
    return true
```

## Type System

Fe uses a strong static type system:

- **Integers**: u8, u16, u32, u64, u128, u256, i8, i16, i32, i64, i128, i256
- **Address**: address (20 bytes)
- **Bool**: bool
- **String**: String<N> (fixed size)
- **Arrays**: Array<T, N> (fixed size)
- **Maps**: Map<K, V>
- **Structs**: Custom types

## Testing

Fe supports Python-based testing:

```python
# tests/test_token.py
def test_transfer(token, accounts):
    sender = accounts[0]
    recipient = accounts[1]

    initial_balance = token.balanceOf(sender)
    token.transfer(recipient, 100, sender=sender)

    assert token.balanceOf(sender) == initial_balance - 100
    assert token.balanceOf(recipient) == 100
```

## Interoperability

Fe contracts are fully compatible with:
- Solidity contracts
- Web3.js, Ethers.js, Viem
- Hardhat, Foundry, Truffle
- All EVM-compatible chains

## Resources

- [Fe Documentation](https://fe-lang.org/docs/)
- [Fe GitHub](https://github.com/ethereum/fe)
- [Fe Forum](https://github.com/ethereum/fe/discussions)
- [Fe Examples](https://github.com/ethereum/fe/tree/master/crates/test-files/fixtures)
- [Fe Book](https://fe-lang.org/book/)

## License

MIT License - See LICENSE file for details

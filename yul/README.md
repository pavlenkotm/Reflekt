# Yul - Low-Level EVM Language

## Overview

Yul is an intermediate language that can be compiled to bytecode for different backends, primarily the Ethereum Virtual Machine (EVM). It's designed to be a usable common denominator of EVM and Ewasm, enabling high-level optimizations.

## Features

- **Low-Level Control**: Direct access to EVM opcodes
- **Gas Optimization**: Maximum control over gas usage
- **Stack Safety**: Prevents stack issues with variable system
- **Inline Assembly**: Can be used within Solidity
- **Portable**: Works with EVM and Ewasm
- **Optimizable**: Easier for optimizers to work with

## Project Structure

```
yul/
├── src/
│   ├── Token.yul           # Minimal ERC-20 token
│   ├── Vault.yul           # Gas-optimized vault
│   └── Math.yul            # Math library
├── test/
│   └── test.sol            # Solidity test harness
├── foundry.toml            # Foundry configuration
└── README.md
```

## Installation

### Prerequisites

```bash
# Install Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Verify installation
forge --version
```

### Dependencies

```bash
# Compile Yul contracts
forge build

# Run tests
forge test
```

## Smart Contracts

### 1. Token Contract (`src/Token.yul`)

Ultra gas-optimized ERC-20 token implementation.

**Features:**
- Minimal bytecode size
- Optimized storage layout
- Efficient function dispatch
- Custom error handling

**Usage:**
```bash
# Compile Yul to bytecode
solc --strict-assembly --optimize src/Token.yul

# Deploy using cast
cast send --create $(cat Token.bin) --rpc-url $RPC_URL

# Interact with contract
cast call $CONTRACT "balanceOf(address)" $ADDRESS
```

### 2. Vault Contract (`src/Vault.yul`)

Highly optimized vault for token deposits.

**Features:**
- Minimal gas usage
- Packed storage
- Efficient math
- Custom ABI encoding

### 3. Math Library (`src/Math.yul`)

Gas-optimized mathematical operations.

**Features:**
- Safe arithmetic
- Fixed-point math
- Bitwise operations
- Common algorithms

## Development

### Build

```bash
# Compile Yul to EVM bytecode
solc --strict-assembly src/Token.yul

# With optimization
solc --strict-assembly --optimize --optimize-runs 200 src/Token.yul

# Output binary and opcodes
solc --strict-assembly --bin --opcodes src/Token.yul
```

### Testing

Yul contracts are typically tested with Solidity wrappers:

```solidity
// test/Token.t.sol
contract TokenTest is Test {
    TokenWrapper token;

    function setUp() public {
        bytes memory bytecode = hex"..."; // Yul bytecode
        address addr;
        assembly {
            addr := create(0, add(bytecode, 0x20), mload(bytecode))
        }
        token = TokenWrapper(addr);
    }

    function testTransfer() public {
        token.transfer(address(0x1), 100);
        assertEq(token.balanceOf(address(0x1)), 100);
    }
}
```

### Deployment

```bash
# Using Foundry
forge create \
    --constructor-args "MyToken" "MTK" \
    YulToken \
    --rpc-url $RPC_URL \
    --private-key $PRIVATE_KEY

# Using Hardhat
npx hardhat run scripts/deploy-yul.js
```

## Yul Language Features

### 1. Object Structure

```yul
object "Token" {
    code {
        // Constructor code
        datacopy(0, dataoffset("Runtime"), datasize("Runtime"))
        return(0, datasize("Runtime"))
    }
    object "Runtime" {
        code {
            // Runtime code (deployed bytecode)
            switch selector()
            case 0x70a08231 /* balanceOf(address) */ {
                returnUint(balanceOf(decodeAddress(0)))
            }
        }
    }
}
```

### 2. Function Definitions

```yul
function balanceOf(account) -> bal {
    let slot := getBalanceSlot(account)
    bal := sload(slot)
}

function transfer(to, amount) -> success {
    let from := caller()
    let fromBalance := balanceOf(from)

    if lt(fromBalance, amount) {
        revert(0, 0)
    }

    setBalance(from, sub(fromBalance, amount))
    setBalance(to, add(balanceOf(to), amount))

    success := 1
}
```

### 3. Storage Access

```yul
// Storage slots
function getBalanceSlot(account) -> slot {
    mstore(0, account)
    mstore(32, 0x00) // Slot 0 for balances mapping
    slot := keccak256(0, 64)
}

function setBalance(account, amount) {
    sstore(getBalanceSlot(account), amount)
}
```

### 4. Function Dispatch

```yul
function selector() -> s {
    s := shr(224, calldataload(0))
}

switch selector()
case 0xa9059cbb /* transfer(address,uint256) */ {
    let to := decodeAddress(0)
    let amount := decodeUint(1)
    returnUint(transfer(to, amount))
}
case 0x70a08231 /* balanceOf(address) */ {
    let account := decodeAddress(0)
    returnUint(balanceOf(account))
}
default {
    revert(0, 0)
}
```

### 5. Memory Management

```yul
// Allocate memory
function allocate(size) -> ptr {
    ptr := mload(0x40) // Free memory pointer
    mstore(0x40, add(ptr, size)) // Update pointer
}

// Copy calldata to memory
function copyCalldata(offset, length) -> ptr {
    ptr := allocate(length)
    calldatacopy(ptr, offset, length)
}
```

### 6. Events

```yul
function emitTransfer(from, to, amount) {
    // Event signature: Transfer(address,address,uint256)
    let signature := 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef

    mstore(0, amount)
    log3(
        0,      // data offset
        32,     // data size
        signature,
        from,   // indexed parameter 1
        to      // indexed parameter 2
    )
}
```

## Gas Optimization Techniques

### 1. Packed Storage

```yul
// Pack multiple values in one slot
// slot: | owner (20 bytes) | totalSupply (12 bytes) |
function packOwnerAndSupply(owner, supply) -> packed {
    packed := or(shl(96, owner), supply)
}

function unpackOwner(packed) -> owner {
    owner := shr(96, packed)
}
```

### 2. Efficient Loops

```yul
// Gas-efficient loop
function sumArray(arrPtr, length) -> sum {
    let end := add(arrPtr, mul(length, 32))
    for { let i := arrPtr } lt(i, end) { i := add(i, 32) } {
        sum := add(sum, mload(i))
    }
}
```

### 3. Bitwise Operations

```yul
// Use bitwise ops instead of arithmetic when possible
function isEven(x) -> result {
    result := iszero(and(x, 1))
}

function div2(x) -> result {
    result := shr(1, x)
}
```

### 4. Custom Errors

```yul
// Revert with custom error
function revertInsufficientBalance() {
    // Error signature: InsufficientBalance()
    mstore(0, 0xf4d678b8) // Error selector
    revert(0, 4)
}
```

## Security Considerations

1. **Integer Overflow**: Implement checks or use safe math
2. **Reentrancy**: Follow checks-effects-interactions
3. **Access Control**: Validate callers properly
4. **Input Validation**: Check all external inputs
5. **Storage Collisions**: Use proper slot calculation

## Yul vs Solidity

### When to Use Yul:

- Maximum gas optimization needed
- Building libraries and primitives
- Custom proxy implementations
- Educational purposes
- Performance-critical code

### When to Use Solidity:

- Rapid development
- Complex business logic
- Maintainability priority
- Team collaboration
- Most DApps

## EVM Opcodes Reference

Common opcodes used in Yul:

```yul
// Arithmetic
add(x, y)           // x + y
sub(x, y)           // x - y
mul(x, y)           // x * y
div(x, y)           // x / y
mod(x, y)           // x % y

// Comparison
lt(x, y)            // x < y
gt(x, y)            // x > y
eq(x, y)            // x == y
iszero(x)           // x == 0

// Bitwise
and(x, y)           // x & y
or(x, y)            // x | y
xor(x, y)           // x ^ y
not(x)              // ~x
shl(x, y)           // y << x
shr(x, y)           // y >> x

// Storage
sload(slot)         // Read storage
sstore(slot, val)   // Write storage

// Memory
mload(addr)         // Read memory
mstore(addr, val)   // Write memory

// Call context
caller()            // msg.sender
callvalue()         // msg.value
calldataload(i)     // msg.data[i:i+32]
calldatasize()      // msg.data.length

// Contract
address()           // address(this)
balance(addr)       // addr.balance
selfdestruct(addr)  // Destroy contract
```

## Debugging

```bash
# Generate opcodes
solc --strict-assembly --opcodes src/Token.yul

# Run in debug mode
forge test --debug testTransfer

# Trace execution
forge test --trace testTransfer
```

## Resources

- [Yul Documentation](https://docs.soliditylang.org/en/latest/yul.html)
- [EVM Opcodes](https://www.evm.codes/)
- [Yul Examples](https://github.com/ethereum/solidity/tree/develop/test/libyul)
- [Gas Optimization Guide](https://github.com/fvictorio/hardhat-gas-reporter)
- [Foundry Book](https://book.getfoundry.sh/)

## License

MIT License - See LICENSE file for details

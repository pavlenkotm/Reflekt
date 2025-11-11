# Motoko - Internet Computer Smart Contracts

## Overview

Motoko is a modern programming language designed specifically for the Internet Computer blockchain platform. It provides a high-level, actor-based programming model with automatic memory management and strong typing.

## Features

- **Actor Model**: Built-in concurrency and message passing
- **Automatic Memory Management**: No manual allocation/deallocation
- **Strong Static Typing**: Type safety with inference
- **Orthogonal Persistence**: State persists automatically
- **Asynchronous Programming**: Native async/await support
- **WebAssembly**: Compiles to efficient WASM

## Project Structure

```
motoko/
├── src/
│   ├── Token.mo            # DIP-20 token standard
│   ├── NFT.mo              # DIP-721 NFT standard
│   └── Vault.mo            # Token vault canister
├── test/
│   └── test.mo             # Test suite
├── dfx.json                # DFX configuration
└── README.md
```

## Installation

### Prerequisites

```bash
# Install DFX (DFINITY SDK)
sh -ci "$(curl -fsSL https://internetcomputer.org/install.sh)"

# Verify installation
dfx --version
```

### Dependencies

```bash
# Start local replica
dfx start --clean --background

# Deploy canisters
dfx deploy

# Stop replica
dfx stop
```

## Smart Contracts (Canisters)

### 1. Token Canister (`src/Token.mo`)

DIP-20 compliant fungible token implementation.

**Features:**
- Minting and burning
- Transfer and transferFrom
- Approve and allowance
- Balance queries
- Transaction history

**Usage:**
```bash
# Deploy token canister
dfx deploy Token --argument '(record {
    name = "MyToken";
    symbol = "MTK";
    decimals = 8;
    totalSupply = 1_000_000_00000000;
})'

# Transfer tokens
dfx canister call Token transfer '(principal "...", 1000)'

# Check balance
dfx canister call Token balanceOf '(principal "...")'
```

### 2. NFT Canister (`src/NFT.mo`)

DIP-721 compliant non-fungible token.

**Features:**
- Mint and burn NFTs
- Transfer and approve
- Metadata storage
- Enumeration support

### 3. Vault Canister (`src/Vault.mo`)

Secure token staking vault.

**Features:**
- Deposit and withdraw
- Reward calculation
- Time-locked staking
- Multi-token support

## Development

### Build

```bash
# Compile all canisters
dfx build

# Compile specific canister
dfx build Token

# Generate candid definitions
dfx generate
```

### Testing

```bash
# Run tests
dfx canister call Token runTests

# Interactive testing
dfx canister call Token balanceOf '(principal "aaaaa-aa")'

# Check canister status
dfx canister status Token
```

### Deployment

```bash
# Deploy to local replica
dfx deploy

# Deploy to IC mainnet
dfx deploy --network ic

# Upgrade canister
dfx canister install Token --mode upgrade
```

## Motoko Language Features

### 1. Actor Definition

```motoko
import Principal "mo:base/Principal";
import HashMap "mo:base/HashMap";

actor Token {
    private stable var totalSupply : Nat = 0;
    private var balances = HashMap.HashMap<Principal, Nat>(10, Principal.equal, Principal.hash);

    public shared(msg) func transfer(to: Principal, amount: Nat) : async Bool {
        // Implementation
        return true;
    };
};
```

### 2. Stable Variables

```motoko
// Persists across upgrades
private stable var owner : Principal = Principal.fromText("aaaaa-aa");
private stable var totalSupply : Nat = 1_000_000;

// Does not persist (must use pre/post upgrade hooks)
private var balances = HashMap.HashMap<Principal, Nat>(10, Principal.equal, Principal.hash);
```

### 3. Async/Await

```motoko
public shared(msg) func transferFrom(
    from: Principal,
    to: Principal,
    amount: Nat
) : async Result.Result<(), Text> {
    let fromBalance = await balanceOf(from);
    if (fromBalance < amount) {
        return #err("Insufficient balance");
    };
    // Transfer logic
    return #ok();
};
```

### 4. Type System

```motoko
type Account = {
    owner: Principal;
    balance: Nat;
};

type TransferArgs = {
    to: Principal;
    amount: Nat;
    memo: ?Blob;
};

type Result<T, E> = {
    #ok : T;
    #err : E;
};
```

### 5. Upgrade Hooks

```motoko
private stable var stableBalances : [(Principal, Nat)] = [];

system func preupgrade() {
    stableBalances := Iter.toArray(balances.entries());
};

system func postupgrade() {
    balances := HashMap.fromIter<Principal, Nat>(
        stableBalances.vals(),
        10,
        Principal.equal,
        Principal.hash
    );
};
```

## Security Best Practices

1. **Caller Authentication**: Always verify msg.caller
2. **Stable Variables**: Use for critical state
3. **Upgrade Safety**: Implement pre/post upgrade hooks
4. **Input Validation**: Validate all inputs
5. **Cycle Management**: Monitor canister cycles
6. **Access Control**: Implement proper permissions

## Internet Computer Concepts

### Canisters

Smart contracts on the Internet Computer are called "canisters". They:
- Run WebAssembly code
- Store state persistently
- Can be upgraded
- Respond to queries and updates
- Require cycles (gas) to run

### Queries vs Updates

**Query Calls** (fast, free):
```motoko
public query func balanceOf(account: Principal) : async Nat {
    // Read-only, no state changes
    return balances.get(account) ?? 0;
};
```

**Update Calls** (consensus, costs cycles):
```motoko
public shared(msg) func transfer(to: Principal, amount: Nat) : async Bool {
    // Modifies state, goes through consensus
    // Implementation
    return true;
};
```

### Cycles

Canisters require cycles (IC's gas) to operate:

```bash
# Check cycles balance
dfx canister status Token

# Add cycles to canister
dfx canister deposit-cycles 1000000000000 Token
```

## Standards

### DIP-20 (Fungible Token)

Standard interface for fungible tokens on IC:
- `transfer(to, amount)`
- `transferFrom(from, to, amount)`
- `approve(spender, amount)`
- `balanceOf(account)`
- `totalSupply()`

### DIP-721 (Non-Fungible Token)

Standard interface for NFTs on IC:
- `mint(to, tokenId, metadata)`
- `transferFrom(from, to, tokenId)`
- `approve(to, tokenId)`
- `ownerOf(tokenId)`
- `tokenMetadata(tokenId)`

## Testing

Motoko supports unit testing:

```motoko
import Debug "mo:base/Debug";
import Token "Token";

actor Test {
    public func runTests() : async () {
        Debug.print("Running token tests...");

        // Test transfer
        let result = await Token.transfer(Principal.fromText("..."), 100);
        assert(result == true);

        Debug.print("All tests passed!");
    };
};
```

## Gas Optimization

- Use query calls when possible (free)
- Minimize stable variable writes
- Use efficient data structures (HashMap, TrieMap)
- Batch operations to reduce calls
- Monitor cycle consumption

## Tools

- **DFX**: Command-line tool for IC development
- **Motoko Playground**: Browser-based IDE
- **Vessel**: Package manager for Motoko
- **IC Inspector**: Blockchain explorer
- **NNS Dapp**: Governance and staking

## Resources

- [Motoko Documentation](https://internetcomputer.org/docs/current/motoko/main/motoko)
- [Internet Computer Docs](https://internetcomputer.org/docs)
- [Motoko Base Library](https://internetcomputer.org/docs/current/motoko/main/base/)
- [IC Developer Forum](https://forum.dfinity.org/)
- [Examples Repository](https://github.com/dfinity/examples)

## License

MIT License - See LICENSE file for details

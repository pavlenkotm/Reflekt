# 🔷 Move - Token Swap DEX

A decentralized exchange (DEX) smart contract written in Move for the Aptos blockchain, implementing an automated market maker (AMM) with constant product formula.

## 📋 Overview

`token_swap` module demonstrates:
- ✅ Liquidity pool management
- ✅ Constant product AMM (x * y = k)
- ✅ Token swapping with 0.3% fee
- ✅ LP token minting for liquidity providers
- ✅ Safe resource management in Move
- ✅ Generic type parameters for any coin pair

## 🛠️ Built With

- **Move**: Aptos framework
- **Aptos CLI**: 2.0.0+
- **Node.js**: 18+ (for TypeScript SDK)

## 🔍 Why Move?

Move is designed for:
- **Resource Safety**: Digital assets can't be copied or lost
- **Formal Verification**: Mathematically provable correctness
- **Gas Efficiency**: Optimized bytecode execution
- **Type Safety**: Strong static typing prevents bugs

## 🚀 Quick Start

### Prerequisites

```bash
# Install Aptos CLI
curl -fsSL "https://aptos.dev/scripts/install_cli.py" | python3

# Verify installation
aptos --version

# Initialize Aptos account
aptos init
```

### Compilation

```bash
# Navigate to move directory
cd move

# Compile the module
aptos move compile

# Run tests
aptos move test

# Run with coverage
aptos move test --coverage
```

### Deployment

```bash
# Deploy to devnet
aptos move publish --named-addresses reflekt=default

# Deploy to testnet
aptos move publish --named-addresses reflekt=default --network testnet

# Deploy to mainnet (⚠️ be careful!)
aptos move publish --named-addresses reflekt=default --network mainnet
```

## 📖 Module Interface

### Structs

#### LiquidityPool<CoinX, CoinY>
Stores reserves of two coins and tracks LP token supply.

#### LPToken
Marker type for liquidity provider tokens.

### Public Functions

#### initialize_pool
```move
public entry fun initialize_pool<CoinX, CoinY>(admin: &signer)
```
Initialize a new liquidity pool for a token pair.

#### add_liquidity
```move
public entry fun add_liquidity<CoinX, CoinY>(
    provider: &signer,
    amount_x: u64,
    amount_y: u64,
    pool_addr: address,
)
```
Add liquidity to pool and receive LP tokens.

#### swap_x_to_y
```move
public entry fun swap_x_to_y<CoinX, CoinY>(
    trader: &signer,
    amount_in: u64,
    min_amount_out: u64,
    pool_addr: address,
)
```
Swap CoinX for CoinY with slippage protection.

#### swap_y_to_x
```move
public entry fun swap_y_to_x<CoinX, CoinY>(
    trader: &signer,
    amount_in: u64,
    min_amount_out: u64,
    pool_addr: address,
)
```
Swap CoinY for CoinX with slippage protection.

#### get_reserves (view)
```move
#[view]
public fun get_reserves<CoinX, CoinY>(pool_addr: address): (u64, u64)
```
Query current pool reserves.

## 🧪 Testing

```bash
# Run all tests
aptos move test

# Run specific test
aptos move test --filter test_initialize_pool

# Run with gas profiling
aptos move test --gas

# Generate coverage report
aptos move test --coverage
aptos move coverage summary
```

Example test:
```move
#[test(admin = @reflekt)]
fun test_swap(admin: &signer) acquires LiquidityPool {
    initialize_pool<USDC, APT>(admin);
    add_liquidity<USDC, APT>(admin, 1000000, 500000, @reflekt);

    swap_x_to_y<USDC, APT>(admin, 10000, 4900, @reflekt);

    let (reserve_x, reserve_y) = get_reserves<USDC, APT>(@reflekt);
    assert!(reserve_x > 1000000, 0);
}
```

## 📊 Example Client Usage (TypeScript)

```typescript
import { AptosClient, AptosAccount, TxnBuilderTypes } from "aptos";

const client = new AptosClient("https://fullnode.devnet.aptoslabs.com");
const account = new AptosAccount();

// Initialize pool
await client.generateTransaction(account.address(), {
  function: "0xREFLEKT::token_swap::initialize_pool",
  type_arguments: ["0x1::aptos_coin::AptosCoin", "0xUSDC::USDC"],
  arguments: [],
});

// Add liquidity
await client.generateTransaction(account.address(), {
  function: "0xREFLEKT::token_swap::add_liquidity",
  type_arguments: ["0x1::aptos_coin::AptosCoin", "0xUSDC::USDC"],
  arguments: [1000000, 500000, account.address()],
});

// Swap tokens
await client.generateTransaction(account.address(), {
  function: "0xREFLEKT::token_swap::swap_x_to_y",
  type_arguments: ["0x1::aptos_coin::AptosCoin", "0xUSDC::USDC"],
  arguments: [10000, 4900, account.address()],
});
```

## 🔒 Security Features

- ✅ Resource safety prevents asset loss
- ✅ No reentrancy vulnerabilities (Move design)
- ✅ Slippage protection on all swaps
- ✅ Overflow protection with checked arithmetic
- ✅ Access control on pool initialization
- ✅ Formal verification capabilities

## 📐 AMM Formula

Constant Product Market Maker:
```
x * y = k (constant)

Output = (Input * 997 * ReserveOut) / (ReserveIn * 1000 + Input * 997)
         ^^^^^^^^^ 0.3% fee
```

## 🆚 Move vs Solidity

| Feature | Move | Solidity |
|---------|------|----------|
| Resource Safety | ✅ Built-in | ❌ Manual |
| Formal Verification | ✅ Native | ⚠️ External tools |
| Reentrancy | ✅ Impossible | ⚠️ Must guard |
| Global Storage | ✅ Resource-oriented | ⚠️ Mapping-based |
| Generics | ✅ First-class | ❌ No generics |

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details

## 🔗 Resources

- [Move Book](https://move-language.github.io/move/)
- [Aptos Documentation](https://aptos.dev/)
- [Move Prover](https://github.com/move-language/move/tree/main/language/move-prover)
- [Aptos TypeScript SDK](https://aptos.dev/sdks/ts-sdk/)
- [Move Tutorial](https://github.com/aptos-labs/aptos-core/tree/main/aptos-move/move-examples)

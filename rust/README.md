# 🦀 Rust - Solana Counter Program

A secure and efficient counter program built with Anchor framework for Solana blockchain.

## 📋 Overview

This `counter_program` demonstrates:
- ✅ Anchor framework usage for Solana development
- ✅ Program Derived Addresses (PDAs)
- ✅ State management and account validation
- ✅ Safe arithmetic with overflow/underflow protection
- ✅ Access control with authority checks
- ✅ Custom error handling

## 🛠️ Built With

- **Rust**: 1.75.0+
- **Anchor**: 0.29.0
- **Solana**: 1.17.0+
- **Node.js**: 18+ (for tests)

## 🚀 Quick Start

### Prerequisites

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Solana CLI
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"

# Install Anchor
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force
avm install latest
avm use latest

# Verify installations
rustc --version
solana --version
anchor --version
```

### Build and Test

```bash
# Build the program
anchor build

# Run tests
anchor test

# Run tests with logs
anchor test -- --nocapture
```

### Deploy

```bash
# Deploy to localnet (start test validator first)
solana-test-validator  # In separate terminal
anchor deploy

# Deploy to devnet
anchor deploy --provider.cluster devnet

# Deploy to mainnet-beta (⚠️ be careful!)
anchor deploy --provider.cluster mainnet
```

## 📖 Program Interface

### Instructions

#### Initialize
Creates a new counter account with initial value of 0.
```rust
pub fn initialize(ctx: Context<Initialize>) -> Result<()>
```

#### Increment
Increases the counter by a specified amount.
```rust
pub fn increment(ctx: Context<Update>, amount: u64) -> Result<()>
```

#### Decrement
Decreases the counter by a specified amount.
```rust
pub fn decrement(ctx: Context<Update>, amount: u64) -> Result<()>
```

#### Reset
Resets the counter to 0.
```rust
pub fn reset(ctx: Context<Update>) -> Result<()>
```

## 🧪 Testing

Create a test file `tests/counter.ts`:

```typescript
import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { CounterProgram } from "../target/types/counter_program";
import { assert } from "chai";

describe("counter-program", () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const program = anchor.workspace.CounterProgram as Program<CounterProgram>;
  const counter = anchor.web3.Keypair.generate();

  it("Initializes counter", async () => {
    await program.methods
      .initialize()
      .accounts({
        counter: counter.publicKey,
        authority: provider.wallet.publicKey,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .signers([counter])
      .rpc();

    const account = await program.account.counter.fetch(counter.publicKey);
    assert.equal(account.count.toNumber(), 0);
  });

  it("Increments counter", async () => {
    await program.methods
      .increment(new anchor.BN(5))
      .accounts({
        counter: counter.publicKey,
        authority: provider.wallet.publicKey,
      })
      .rpc();

    const account = await program.account.counter.fetch(counter.publicKey);
    assert.equal(account.count.toNumber(), 5);
  });
});
```

Run tests:
```bash
anchor test
```

## 📊 Example Client Usage

```javascript
const anchor = require("@coral-xyz/anchor");

async function main() {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const program = anchor.workspace.CounterProgram;
  const counter = anchor.web3.Keypair.generate();

  // Initialize
  await program.methods
    .initialize()
    .accounts({
      counter: counter.publicKey,
      authority: provider.wallet.publicKey,
      systemProgram: anchor.web3.SystemProgram.programId,
    })
    .signers([counter])
    .rpc();

  console.log("Counter initialized!");

  // Increment
  await program.methods
    .increment(new anchor.BN(10))
    .accounts({
      counter: counter.publicKey,
      authority: provider.wallet.publicKey,
    })
    .rpc();

  // Fetch and display
  const account = await program.account.counter.fetch(counter.publicKey);
  console.log("Counter value:", account.count.toString());
}
```

## 🔒 Security Features

- ✅ Overflow/underflow protection with `checked_add`/`checked_sub`
- ✅ Authority validation with `has_one` constraint
- ✅ Custom error codes for better debugging
- ✅ Zero-copy deserialization for efficiency
- ✅ Rent-exempt account initialization

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Client Application             │
│     (JavaScript/TypeScript/Rust)         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Solana RPC Endpoint              │
│    (Mainnet/Devnet/Localnet)             │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│       Counter Program (On-chain)         │
│  • initialize()                          │
│  • increment(amount)                     │
│  • decrement(amount)                     │
│  • reset()                               │
└─────────────────────────────────────────┘
```

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details

## 🔗 Resources

- [Anchor Documentation](https://www.anchor-lang.com/)
- [Solana Cookbook](https://solanacookbook.com/)
- [Solana Documentation](https://docs.solana.com/)
- [Anchor Book](https://book.anchor-lang.com/)
- [Rust Programming Language](https://doc.rust-lang.org/book/)

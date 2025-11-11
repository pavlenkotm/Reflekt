# Clarity - Stacks Blockchain Smart Contracts

## Overview

Clarity is a decidable smart contract language for the Stacks blockchain. It is designed to be more secure and predictable than other smart contract languages by being non-Turing complete and having no compiler, preventing entire classes of bugs.

## Features

- **Decidability**: Code execution is predictable and analyzable
- **No Compiler**: Interpreted directly, eliminating compiler bugs
- **Post-Conditions**: Built-in runtime assertions
- **Non-Turing Complete**: Prevents infinite loops
- **Bitcoin Integration**: Settles on Bitcoin blockchain
- **Lisp-like Syntax**: Functional programming paradigm

## Project Structure

```
clarity/
├── contracts/
│   ├── sip-010-token.clar      # Fungible token standard
│   ├── sip-009-nft.clar        # NFT standard
│   └── vault.clar              # Token vault
├── tests/
│   └── token_test.ts           # TypeScript tests
├── Clarinet.toml               # Project configuration
└── README.md
```

## Installation

### Prerequisites

```bash
# Install Clarinet (Clarity development tool)
curl -L https://github.com/hirosystems/clarinet/releases/latest/download/clarinet-linux-x64.tar.gz | tar xz
sudo mv clarinet /usr/local/bin/

# Verify installation
clarinet --version
```

### Dependencies

```bash
# Initialize project
clarinet new my-project

# Check contracts
clarinet check

# Run tests
clarinet test
```

## Smart Contracts

### 1. SIP-010 Token (`contracts/sip-010-token.clar`)

Standard fungible token implementation for Stacks.

**Features:**
- Transfer and transfer-memo
- Balance queries
- Token metadata
- Minting (owner only)

**Usage:**
```bash
# Check contract
clarinet check

# Run tests
clarinet test

# Deploy to testnet
clarinet deploy --testnet

# Call contract function
stx call-contract-func token transfer \
    --recipient ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM \
    --amount u1000 \
    --network testnet
```

### 2. SIP-009 NFT (`contracts/sip-009-nft.clar`)

Non-fungible token standard for Stacks.

**Features:**
- Mint and transfer NFTs
- Owner tracking
- URI management
- Enumeration support

### 3. Vault Contract (`contracts/vault.clar`)

Secure vault for staking SIP-010 tokens.

**Features:**
- Deposit and withdraw
- Reward calculation
- Time-locked staking
- Multi-token support

## Development

### Build

```bash
# Check all contracts
clarinet check

# Check specific contract
clarinet check contracts/sip-010-token.clar

# Generate documentation
clarinet docs
```

### Testing

```bash
# Run all tests
clarinet test

# Run with coverage
clarinet test --coverage

# Run specific test
clarinet test --filter token
```

### Deployment

```bash
# Deploy to devnet
clarinet integrate

# Deploy to testnet
clarinet deploy --testnet

# Deploy to mainnet
clarinet deploy --mainnet
```

## Clarity Language Features

### 1. Contract Definition

```clarity
;; Define a fungible token
(define-fungible-token reflekt-token)

;; Define constants
(define-constant contract-owner tx-sender)
(define-constant err-owner-only (err u100))
(define-constant err-not-authorized (err u101))

;; Define data variables
(define-data-var token-name (string-ascii 32) "Reflekt Token")
(define-data-var token-symbol (string-ascii 10) "RFLKT")
(define-data-var token-decimals uint u8)
```

### 2. Public Functions

```clarity
(define-public (transfer (amount uint) (sender principal) (recipient principal) (memo (optional (buff 34))))
    (begin
        ;; Check authorization
        (asserts! (is-eq tx-sender sender) err-not-authorized)

        ;; Perform transfer
        (try! (ft-transfer? reflekt-token amount sender recipient))

        ;; Print memo if provided
        (match memo to-print (print to-print) 0x)

        ;; Return success
        (ok true)
    )
)
```

### 3. Read-Only Functions

```clarity
(define-read-only (get-balance (account principal))
    (ok (ft-get-balance reflekt-token account))
)

(define-read-only (get-total-supply)
    (ok (ft-get-supply reflekt-token))
)

(define-read-only (get-name)
    (ok (var-get token-name))
)
```

### 4. Data Maps

```clarity
;; Define data map
(define-map allowances
    {owner: principal, spender: principal}
    {amount: uint}
)

;; Get from map
(define-read-only (get-allowance (owner principal) (spender principal))
    (default-to u0
        (get amount (map-get? allowances {owner: owner, spender: spender}))
    )
)

;; Set in map
(define-public (set-allowance (spender principal) (amount uint))
    (ok (map-set allowances {owner: tx-sender, spender: spender} {amount: amount}))
)
```

### 5. Private Functions

```clarity
(define-private (internal-transfer (amount uint) (sender principal) (recipient principal))
    (begin
        (asserts! (>= (ft-get-balance reflekt-token sender) amount) err-insufficient-balance)
        (ft-transfer? reflekt-token amount sender recipient)
    )
)
```

### 6. Post-Conditions

Clarity supports runtime assertions that must be true after execution:

```clarity
(define-public (transfer-with-check (amount uint) (recipient principal))
    (let (
        (sender-balance-before (ft-get-balance reflekt-token tx-sender))
        (recipient-balance-before (ft-get-balance reflekt-token recipient))
    )
        (try! (ft-transfer? reflekt-token amount tx-sender recipient))

        ;; Post-condition: verify balances changed correctly
        (asserts!
            (is-eq
                (ft-get-balance reflekt-token tx-sender)
                (- sender-balance-before amount)
            )
            err-post-condition-failed
        )

        (ok true)
    )
)
```

## Security Best Practices

1. **Access Control**: Always check tx-sender
2. **Input Validation**: Validate all inputs with asserts!
3. **Arithmetic Safety**: Use safe-add, safe-subtract
4. **Post-Conditions**: Verify critical state changes
5. **Immutability**: Use constants when possible
6. **Error Handling**: Use try! and proper error codes

## Token Standards

### SIP-010 (Fungible Token)

Required trait:

```clarity
(define-trait sip-010-trait
    (
        (transfer (uint principal principal (optional (buff 34))) (response bool uint))
        (get-name () (response (string-ascii 32) uint))
        (get-symbol () (response (string-ascii 32) uint))
        (get-decimals () (response uint uint))
        (get-balance (principal) (response uint uint))
        (get-total-supply () (response uint uint))
        (get-token-uri () (response (optional (string-utf8 256)) uint))
    )
)
```

### SIP-009 (Non-Fungible Token)

Required trait:

```clarity
(define-trait sip-009-trait
    (
        (get-last-token-id () (response uint uint))
        (get-token-uri (uint) (response (optional (string-ascii 256)) uint))
        (get-owner (uint) (response (optional principal) uint))
        (transfer (uint principal principal) (response bool uint))
    )
)
```

## Testing with Clarinet

TypeScript test example:

```typescript
import { Clarinet, Tx, Chain, Account, types } from 'https://deno.land/x/clarinet/index.ts';

Clarinet.test({
    name: "Can transfer tokens",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        let deployer = accounts.get('deployer')!;
        let wallet1 = accounts.get('wallet_1')!;

        let block = chain.mineBlock([
            Tx.contractCall('token', 'transfer', [
                types.uint(1000),
                types.principal(deployer.address),
                types.principal(wallet1.address),
                types.none()
            ], deployer.address)
        ]);

        block.receipts[0].result.expectOk().expectBool(true);
    },
});
```

## Bitcoin Integration

Clarity contracts can read Bitcoin state:

```clarity
(define-read-only (get-bitcoin-block-hash (height uint))
    (get-block-info? header-hash height)
)

(define-read-only (get-bitcoin-block-time (height uint))
    (get-block-info? time height)
)
```

## Clarity vs Other Languages

### Advantages:

1. **Decidability**: Can prove properties about code
2. **No Compiler Bugs**: Interpreted directly
3. **Bitcoin Settlement**: Inherits Bitcoin security
4. **Predictable Costs**: No gas estimation needed
5. **Safer Upgrades**: No storage layout issues

### Trade-offs:

1. **Limited Expressiveness**: Non-Turing complete
2. **Different Paradigm**: Lisp-like syntax
3. **Smaller Ecosystem**: Newer platform
4. **Learning Curve**: Functional programming

## Tools

- **Clarinet**: Development and testing tool
- **Stacks Explorer**: Blockchain explorer
- **Hiro Wallet**: Browser wallet
- **Stacks.js**: JavaScript SDK
- **Clarity REPL**: Interactive development

## Resources

- [Clarity Book](https://book.clarity-lang.org/)
- [Stacks Documentation](https://docs.stacks.co/)
- [Clarity Reference](https://docs.stacks.co/clarity/overview)
- [Stacks Forum](https://forum.stacks.org/)
- [SIP Repository](https://github.com/stacksgov/sips)

## License

MIT License - See LICENSE file for details

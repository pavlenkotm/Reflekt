# Code Examples and Use Cases

This document showcases practical examples and use cases for each language in the repository.

## Smart Contracts

### Solidity - ERC-20 Token

**Use Case**: Launch your own cryptocurrency or governance token

```solidity
// Deploy a token with 1 million supply
const token = await SimpleToken.deploy(
  "MyToken",
  "MTK",
  1000000,
  18
);

// Mint additional tokens (owner only)
await token.mint(userAddress, ethers.parseEther("1000"));

// Transfer tokens
await token.transfer(recipientAddress, ethers.parseEther("100"));
```

[Full Example →](./solidity/)

---

### Vyper - ETH Vault

**Use Case**: Time-locked savings or escrow

```python
# Deploy vault
vault = Vault.deploy(sender=deployer)

# Deposit ETH
vault.deposit(value=Web3.toWei(10, 'ether'))

# Withdraw after conditions met
vault.withdraw(Web3.toWei(5, 'ether'))
```

[Full Example →](./vyper/)

---

### Rust - Solana Counter

**Use Case**: On-chain state management for games or voting

```rust
// Initialize counter
let tx = program
    .request()
    .accounts(Initialize {
        counter: counter_pubkey,
        user: user.pubkey(),
        system_program: system_program::ID,
    })
    .args(instruction::Initialize {})
    .send()?;

// Increment by 5
program.increment(5).await?;
```

[Full Example →](./rust/)

---

## DApp Frontends

### TypeScript - Wallet Connection

**Use Case**: Connect MetaMask to your DApp

```typescript
import { WalletConnector } from './wallet-connect';

const wallet = new WalletConnector();

// Connect
const info = await wallet.connectMetaMask();
console.log(`Connected: ${info.address}`);

// Send transaction
const txHash = await wallet.sendTransaction({
  to: '0x...',
  value: '0.1', // ETH
});

// Sign message
const signature = await wallet.signMessage('Hello Web3!');
```

[Full Example →](./typescript/)

---

### HTML/CSS - Landing Page

**Use Case**: Professional landing page for your DApp

Features:
- Responsive design
- Language showcase grid
- Feature highlights
- Mobile-friendly

[Full Example →](./html-css/)

---

## Backend Services

### Python - CLI Tools

**Use Case**: Automate blockchain operations

```bash
# Check multiple balances
python web3_cli.py balance 0xVitalik...
python web3_cli.py balance 0xUser1...
python web3_cli.py balance 0xUser2...

# Check token balances
python web3_cli.py token 0xUSDC... 0xHolder...

# Generate wallets
python web3_cli.py generate
```

[Full Example →](./python/)

---

### Go - Signature Verification

**Use Case**: Verify user ownership for authentication

```go
sv := NewSignatureVerifier()

// User signs message with MetaMask
message := "Authenticate for myapp.com"
signature := "0x..." // From MetaMask

// Verify on backend
valid, err := sv.VerifySignature(userAddress, message, signature)
if valid {
    // Grant access
}
```

[Full Example →](./go/)

---

### Ruby - Blockchain Indexer

**Use Case**: Index blockchain data for analytics

```ruby
indexer = BlockchainIndexer.new

# Index last 100 blocks
blocks = indexer.index_blocks(100)

# Analyze
stats = indexer.analyze_blocks(blocks)

puts "Total transactions: #{stats[:total_transactions]}"
puts "Average gas: #{stats[:average_gas_used]}"
```

[Full Example →](./ruby/)

---

## Mobile Development

### Swift - iOS Wallet

**Use Case**: Native iOS cryptocurrency wallet

```swift
let wallet = WalletKit()

// Generate wallet
let (address, privateKey) = try wallet.generateWallet()

// Save to Keychain (secure)
try KeychainManager.save(privateKey, for: address)

// Format values
let eth = wallet.formatToEther("1000000000000000000")
// "1.0"
```

[Full Example →](./swift/)

---

### Java - Android Wallet

**Use Case**: Enterprise Android wallet app

```java
WalletManager manager = new WalletManager("https://eth.llamarpc.com");

// Generate wallet
ECKeyPair keyPair = manager.generateWallet();

// Get balance
BigDecimal balance = manager.getBalance(address);

// Send transaction
String txHash = manager.sendTransaction(
    privateKey,
    toAddress,
    new BigDecimal("0.1")
);
```

[Full Example →](./java/)

---

## DevOps & Automation

### Bash - Deployment

**Use Case**: Automated contract deployment

```bash
# Set environment
export NETWORK="sepolia"
export PRIVATE_KEY="0x..."

# Run deployment pipeline
./bash/deploy.sh

# Output:
# ✅ Contract deployed at: 0x...
# ✅ Verified on Etherscan
# ✅ Deployment saved to deployments/sepolia.json
```

[Full Example →](./bash/)

---

## Advanced Use Cases

### Multi-Chain Portfolio Tracker

Combine multiple languages:

1. **Python**: Fetch balances from multiple chains
2. **Ruby**: Index historical data
3. **TypeScript**: Frontend dashboard
4. **Go**: High-performance API

### DAO Governance System

1. **Solidity**: Governance contract
2. **TypeScript**: Voting UI
3. **Python**: Proposal analysis
4. **Bash**: Automated execution

### NFT Marketplace

1. **Solidity**: ERC-721 + Marketplace contracts
2. **TypeScript**: Frontend (listing, buying, selling)
3. **Python**: Metadata generation and IPFS upload
4. **Go**: High-performance backend API

### DeFi Yield Aggregator

1. **Solidity**: Vault and strategy contracts
2. **TypeScript**: User interface
3. **Python**: Yield calculation and rebalancing
4. **Ruby**: Historical APY tracking

---

## Integration Examples

### With Popular Frameworks

#### Next.js + TypeScript
```typescript
// pages/index.tsx
import { WalletConnector } from '../lib/wallet-connect';

export default function Home() {
  const [address, setAddress] = useState('');

  const connect = async () => {
    const wallet = new WalletConnector();
    const info = await wallet.connectMetaMask();
    setAddress(info.address);
  };

  return <button onClick={connect}>Connect Wallet</button>;
}
```

#### Flask + Python
```python
from flask import Flask, jsonify
from web3_cli import Web3CLI

app = Flask(__name__)
cli = Web3CLI('https://eth.llamarpc.com')

@app.route('/balance/<address>')
def get_balance(address):
    balance = cli.get_balance(address)
    return jsonify(balance)
```

#### Express + TypeScript
```typescript
import express from 'express';
import { WalletConnector } from './wallet-connect';

const app = express();

app.get('/api/gas-price', async (req, res) => {
  const wallet = new WalletConnector();
  // Implementation
});
```

---

## Best Practices

### Smart Contracts
✅ Use OpenZeppelin for standard contracts
✅ Always test on testnets first
✅ Get professional audits for mainnet
✅ Implement access control
✅ Emit events for important actions

### Frontend
✅ Handle wallet disconnection
✅ Show transaction status
✅ Implement error handling
✅ Add loading states
✅ Make mobile-responsive

### Backend
✅ Validate all inputs
✅ Implement rate limiting
✅ Use environment variables
✅ Log important operations
✅ Handle RPC failures gracefully

---

## More Examples

Want to see more examples? Check:
- Individual README files in each folder
- [GitHub Discussions](https://github.com/pavlenkotm/Reflekt/discussions)
- [Issue tracker](https://github.com/pavlenkotm/Reflekt/issues) for feature requests

## Contributing Examples

Have a cool example? Submit a PR! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

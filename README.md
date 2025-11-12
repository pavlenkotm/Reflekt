# 🌐 Web3 Multi-Language Repository

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Languages](https://img.shields.io/badge/languages-25+-blue.svg)
![Commits](https://img.shields.io/badge/commits-40+-orange.svg)
![CI](https://github.com/pavlenkotm/Reflekt/workflows/CI%2FCD%20Pipeline/badge.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**A comprehensive Web3 development playground showcasing professional smart contracts, blockchain tools, and DApps across 25+ programming languages and exotic blockchain ecosystems.**

Perfect for learning, reference, or jumpstarting your next Web3 project!

---

## ✨ What's Inside?

This repository demonstrates **production-ready** Web3 code in multiple ecosystems:

- **Smart Contract Languages**: Solidity, Vyper, Move, Plutus (Haskell), Cairo (StarkNet), Ink! (Polkadot), Sway (Fuel), Fe (EVM), Motoko (ICP), Yul (Low-level EVM), Clarity (Stacks)
- **Systems Programming**: Rust, Go, C++, Zig
- **Web & Mobile**: TypeScript, JavaScript, Swift, Java
- **Scripting & Automation**: Python, Ruby, Bash
- **Frontend**: HTML/CSS responsive landing page

Each example includes:
- ✅ Complete, runnable code
- ✅ Comprehensive README with setup instructions
- ✅ Real-world use cases
- ✅ Security best practices
- ✅ Tests (where applicable)

---

## 📂 Repository Structure

```
Reflekt/
├── solidity/          # ERC-20 token with OpenZeppelin + tests
├── vyper/             # ETH vault contract
├── rust/              # Solana Anchor program + tests
├── move/              # Aptos token swap DEX
├── cairo/             # StarkNet ERC-20 (ZK-rollups)
├── ink/               # Polkadot/Substrate Wasm contracts
├── sway/              # Fuel Network token (UTXO model)
├── fe/                # Python-inspired EVM token
├── motoko/            # Internet Computer canister
├── yul/               # Low-level EVM assembly
├── clarity/           # Stacks SIP-010 token (Bitcoin L2)
├── typescript/        # Ethers.js & Viem utilities + tests
├── javascript/        # Web3.js wallet manager + tests
├── python/            # Web3.py CLI tools + tests
├── go/                # Ethereum utilities + Cosmos SDK module
├── cpp/               # Keccak256 cryptographic utilities
├── java/              # Web3j wallet manager
├── swift/             # iOS/macOS WalletKit
├── bash/              # Deployment automation scripts
├── haskell/           # Plutus smart contracts (Cardano)
├── zig/               # High-performance crypto for WASM
├── ruby/              # Blockchain data indexer
├── html-css/          # DApp landing page
├── contracts/         # Original Reputation NFT project + tests
├── src/               # Original Python backend + tests
├── frontend/          # Original Streamlit frontend
├── .github/           # CI/CD workflows (improved)
├── Dockerfile         # Multi-stage Docker build
├── docker-compose.yml # Development & testing services
└── DOCKER.md          # Docker documentation
```

---

## 🚀 Quick Start

### Prerequisites

Different languages have different requirements. See individual README files for specifics.

### Explore a Specific Language

```bash
# Clone the repository
git clone https://github.com/pavlenkotm/Reflekt.git
cd Reflekt

# Navigate to any language folder
cd typescript

# Follow the README instructions
cat README.md
```

### Run Examples

Each language folder contains:
- `README.md` - Setup and usage instructions
- Working code examples
- Build/run commands
- Test suites (where applicable)

---

## 💎 Featured Projects

### 1. Solidity - ERC-20 Token
Professional token implementation with OpenZeppelin contracts.

```solidity
contract SimpleToken is ERC20, Ownable {
    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
}
```

**Tech**: Solidity ^0.8.20, OpenZeppelin, Hardhat/Foundry

[View Code →](./solidity/)

---

### 2. Rust - Solana Counter Program
High-performance Solana program using Anchor framework.

```rust
#[program]
pub mod counter_program {
    pub fn increment(ctx: Context<Update>, amount: u64) -> Result<()> {
        ctx.accounts.counter.count = ctx.accounts.counter.count
            .checked_add(amount)
            .ok_or(CounterError::Overflow)?;
        Ok(())
    }
}
```

**Tech**: Rust, Anchor 0.29, Solana

[View Code →](./rust/)

---

### 3. TypeScript - Web3 Wallet Utilities
Modern DApp development with Ethers.js and Viem.

```typescript
const wallet = new WalletConnector();
await wallet.connectMetaMask();
const signature = await wallet.signMessage("Hello Web3!");
```

**Tech**: TypeScript 5.3+, Ethers.js 6.10, Viem 2.7

[View Code →](./typescript/)

---

### 4. Python - Web3.py CLI Tools
Command-line blockchain automation.

```bash
python web3_cli.py balance 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
python web3_cli.py token 0xUSDC... 0xHolder...
```

**Tech**: Python 3.8+, Web3.py 6.15+

[View Code →](./python/)

---

### 5. Move - Token Swap DEX
Automated market maker for Aptos blockchain.

```move
public entry fun swap_x_to_y<CoinX, CoinY>(
    trader: &signer,
    amount_in: u64,
    min_amount_out: u64,
    pool_addr: address,
) acquires LiquidityPool { ... }
```

**Tech**: Move, Aptos Framework

[View Code →](./move/)

---

## 📊 Language Comparison

| Language   | Use Case             | Performance | Difficulty | Ecosystem |
|------------|----------------------|-------------|------------|-----------|
| Solidity   | Ethereum contracts   | Medium      | Medium     | ⭐⭐⭐⭐⭐ |
| Vyper      | Secure EVM contracts | Medium      | Easy       | ⭐⭐⭐    |
| Rust       | Solana programs      | Very High   | Hard       | ⭐⭐⭐⭐  |
| Move       | Aptos/Sui contracts  | High        | Medium     | ⭐⭐⭐    |
| Cairo      | StarkNet ZK-rollups  | High        | Hard       | ⭐⭐⭐    |
| Ink!       | Polkadot Wasm        | High        | Hard       | ⭐⭐⭐    |
| Sway       | Fuel UTXO contracts  | Very High   | Medium     | ⭐⭐      |
| Fe         | Python-like EVM      | Medium      | Easy       | ⭐⭐      |
| Motoko     | Internet Computer    | Medium      | Medium     | ⭐⭐⭐    |
| Yul        | Low-level EVM        | Very High   | Hard       | ⭐⭐⭐⭐  |
| Clarity    | Stacks Bitcoin L2    | Medium      | Medium     | ⭐⭐⭐    |
| TypeScript | DApp frontends       | Medium      | Easy       | ⭐⭐⭐⭐⭐ |
| Python     | Automation scripts   | Medium      | Easy       | ⭐⭐⭐⭐⭐ |
| Go         | Cosmos SDK/Backend   | Very High   | Medium     | ⭐⭐⭐⭐  |
| C++        | Crypto primitives    | Extreme     | Hard       | ⭐⭐⭐    |
| Java       | Enterprise/Android   | High        | Medium     | ⭐⭐⭐⭐  |
| Swift      | iOS wallets          | High        | Medium     | ⭐⭐⭐    |

---

## 🧪 Testing & CI/CD

This repository includes:
- ✅ GitHub Actions CI/CD pipeline
- ✅ Multi-language test automation
- ✅ Linting and formatting checks
- ✅ Build verification

```yaml
# Automatically tests Python, TypeScript, Solidity, Go, Rust, and C++
- Python: pytest, flake8
- TypeScript: tsc, eslint
- Solidity: hardhat compile
- Go: go build
- Rust: cargo build
- C++: g++ compile
```

---

## 🎯 Use Cases

### 1. **Learning Web3 Development**
- Compare implementations across languages
- See best practices in action
- Understand different blockchain ecosystems

### 2. **Project Starters**
- Copy and adapt code for your project
- Use as boilerplate
- Reference implementations

### 3. **Portfolio Showcase**
- Demonstrate multi-language proficiency
- Show blockchain expertise
- Highlight open-source contributions

### 4. **Team Education**
- Onboard developers to Web3
- Compare language trade-offs
- Explore different architectures

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/Reflekt.git

# Create feature branch
git checkout -b feature/amazing-addition

# Make changes and commit
git commit -m "feat(lang): add amazing feature"

# Push and create PR
git push origin feature/amazing-addition
```

**Commit Convention**: We follow [Conventional Commits](https://www.conventionalcommits.org/)

---

## 🧪 Testing

All language implementations now include comprehensive test suites!

### Run All Tests

```bash
# Using Docker
docker-compose up test

# Or run individually
cd python && pytest tests/ --verbose
cd typescript && npm test
cd javascript && npm test
cd go && go test -v ./...
cd solidity && npx hardhat test
cd contracts && npx hardhat test
```

### Test Coverage

- **Python**: pytest with coverage reporting
- **TypeScript**: Jest with mock providers
- **JavaScript**: Mocha + Chai for Web3.js
- **Go**: Native testing with race detection
- **Solidity**: Hardhat test framework

See [`TESTING.md`](./TESTING.md) for detailed testing guide.

---

## 🐳 Docker Support

Complete Docker setup for development and testing.

### Quick Start with Docker

```bash
# Start development environment
docker-compose up -d dev
docker-compose exec dev bash

# Run all tests
docker-compose up test

# Start API and frontend
docker-compose up -d api frontend

# Local blockchain
docker-compose up -d hardhat
```

### Available Services

- `dev` - Full development environment (Python, Node, Go, Rust, C++)
- `test` - Run complete test suite
- `api` - Python FastAPI backend (port 8000)
- `frontend` - Streamlit app (port 8501)
- `hardhat` - Local Ethereum network (port 8545)

See [`DOCKER.md`](./DOCKER.md) for complete Docker documentation.

---

## 📦 Deployments

Reference contract deployments on testnets and mainnet.

See [`DEPLOYMENTS.md`](./DEPLOYMENTS.md) for:
- Deployed contract addresses
- Network configurations
- Interaction examples
- Verification commands

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## 🔗 Resources

### Blockchains & Protocols
- [Ethereum](https://ethereum.org/) - Smart contract platform
- [Solana](https://solana.com/) - High-performance blockchain
- [Aptos](https://aptoslabs.com/) - Move-based blockchain
- [Cardano](https://cardano.org/) - Proof-of-stake blockchain

### Development Tools
- [Hardhat](https://hardhat.org/) - Ethereum development environment
- [Foundry](https://getfoundry.sh/) - Blazing fast Ethereum toolkit
- [Anchor](https://www.anchor-lang.com/) - Solana framework
- [OpenZeppelin](https://openzeppelin.com/) - Secure smart contract library

### Learning
- [Solidity by Example](https://solidity-by-example.org/)
- [Rust Book](https://doc.rust-lang.org/book/)
- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Ethers.js Docs](https://docs.ethers.org/)

---

## 📬 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/pavlenkotm/Reflekt/issues)
- **Discussions**: [Ask questions or share ideas](https://github.com/pavlenkotm/Reflekt/discussions)
- **Twitter**: [@ReflektApp](https://twitter.com/ReflektApp)

---

## 🌟 Star History

If you find this repository helpful, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=pavlenkotm/Reflekt&type=Date)](https://star-history.com/#pavlenkotm/Reflekt&Date)

---

## 📈 GitHub Stats

![GitHub stats](https://github-readme-stats.vercel.app/api/pin/?username=pavlenkotm&repo=Reflekt&theme=radical)

---

<p align="center">
  <strong>Made with ❤️ for the Web3 community</strong>
  <br>
  <a href="https://github.com/pavlenkotm/Reflekt">View on GitHub</a> •
  <a href="https://github.com/pavlenkotm/Reflekt/issues">Report Issue</a> •
  <a href="./CONTRIBUTING.md">Contribute</a>
</p>

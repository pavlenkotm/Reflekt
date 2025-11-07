# Quick Start Guide

Get started with the Web3 Multi-Language Repository in 5 minutes!

## Choose Your Path

### 🎯 I want to learn Web3
→ Start with [TypeScript](./typescript/) or [Python](./python/)

### 💎 I want to write smart contracts
→ Start with [Solidity](./solidity/) on Ethereum

### 🚀 I want high performance
→ Start with [Rust](./rust/) on Solana or [Go](./go/)

### 📱 I want to build mobile apps
→ Start with [Swift](./swift/) (iOS) or [Java](./java/) (Android)

## 5-Minute Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/pavlenkotm/Reflekt.git
cd Reflekt
```

### 2. Pick a Language

```bash
# TypeScript example
cd typescript
npm install
npm run build

# Python example
cd python
pip install -r requirements.txt
python web3_cli.py --help

# Solidity example
cd solidity
npm install
npx hardhat compile
```

### 3. Run Your First Example

```bash
# TypeScript: Connect to wallet
node dist/wallet-connect.js

# Python: Check Vitalik's balance
python web3_cli.py balance 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045

# Solidity: Run tests
npx hardhat test
```

## Environment Setup

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your RPC URL:

```bash
ETHEREUM_RPC_URL=https://eth.llamarpc.com
```

## What to Explore

### For Beginners
1. [README.md](./README.md) - Project overview
2. [FAQ.md](./FAQ.md) - Common questions
3. [GLOSSARY.md](./GLOSSARY.md) - Web3 terms
4. [TypeScript Example](./typescript/README.md)

### For Developers
1. [ARCHITECTURE.md](./ARCHITECTURE.md) - System design
2. [TESTING.md](./TESTING.md) - How to test
3. [EXAMPLES.md](./EXAMPLES.md) - Code examples
4. Individual language folders

### For Contributors
1. [CONTRIBUTING.md](./CONTRIBUTING.md) - How to contribute
2. [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) - Community guidelines
3. [SECURITY.md](./SECURITY.md) - Security policy
4. [ROADMAP.md](./ROADMAP.md) - Future plans

## Common Commands

```bash
# Install all dependencies
make install

# Run all tests
make test

# Clean build artifacts
make clean

# See all commands
make help
```

## Get Help

- 📚 Read the [FAQ](./FAQ.md)
- 💬 Open a [Discussion](https://github.com/pavlenkotm/Reflekt/discussions)
- 🐛 Report [Issues](https://github.com/pavlenkotm/Reflekt/issues)
- 📖 Check individual README files in each folder

## Next Steps

1. **Explore** - Browse different language folders
2. **Experiment** - Modify code and see what happens
3. **Build** - Use examples in your own projects
4. **Contribute** - Submit PRs to improve the repo

## Resources

- [Ethereum.org](https://ethereum.org/en/developers/)
- [Solana Cookbook](https://solanacookbook.com/)
- [Web3 University](https://www.web3.university/)
- [OpenZeppelin Docs](https://docs.openzeppelin.com/)

---

**Ready to dive deeper?** Check out [README.md](./README.md) for the full documentation!

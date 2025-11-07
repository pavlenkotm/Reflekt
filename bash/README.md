# 🐚 Bash - Web3 Deployment Automation

Production-ready Bash scripts for smart contract deployment, verification, and monitoring across EVM chains.

## 📋 Overview

`deploy.sh` provides:
- ✅ Automated contract compilation
- ✅ Multi-network deployment (Hardhat/Foundry)
- ✅ Etherscan verification
- ✅ Gas price monitoring
- ✅ Post-deployment validation
- ✅ Deployment logging

## 🚀 Quick Start

```bash
# Make executable
chmod +x bash/deploy.sh

# Set environment variables
export NETWORK="sepolia"
export PRIVATE_KEY="0x..."
export RPC_URL="https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY"

# Run deployment
./bash/deploy.sh
```

## 📖 Features

### Supported Networks
- Ethereum (mainnet, sepolia, goerli)
- Polygon (mainnet, mumbai)
- Arbitrum, Optimism, Base
- Any EVM-compatible chain

### Automated Steps
1. Environment validation
2. Gas price check
3. Contract compilation
4. Deployment
5. Etherscan verification
6. On-chain validation

## 📄 License

MIT License

# Contract Deployments

Reference deployments of Reflekt smart contracts across various networks.

## Testnet Deployments

### Sepolia (Ethereum Testnet)

#### ReputationNFT
- **Address**: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0` (example)
- **Explorer**: https://sepolia.etherscan.io/address/0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0
- **Network**: Sepolia (Chain ID: 11155111)
- **Block**: 4567890
- **Deployer**: `0x...`

#### SimpleToken (ERC-20)
- **Address**: `0x1234567890123456789012345678901234567890` (example)
- **Explorer**: https://sepolia.etherscan.io/address/0x1234567890123456789012345678901234567890
- **Network**: Sepolia (Chain ID: 11155111)
- **Token Name**: Reflekt Test Token
- **Symbol**: RTT
- **Decimals**: 18
- **Initial Supply**: 1,000,000 RTT

### Base Sepolia (L2 Testnet)

#### SimpleToken
- **Address**: `0xabcdefabcdefabcdefabcdefabcdefabcdefabcd` (example)
- **Explorer**: https://sepolia.basescan.org/address/0xabcdefabcdefabcdefabcdefabcdefabcdefabcd
- **Network**: Base Sepolia (Chain ID: 84532)

### Optimism Sepolia (L2 Testnet)

#### ReputationNFT
- **Address**: `0xfedcbafedcbafedcbafedcbafedcbafedcbafed` (example)
- **Explorer**: https://sepolia-optimistic.etherscan.io/address/0xfedcbafedcbafedcbafedcbafedcbafedcbafed
- **Network**: Optimism Sepolia (Chain ID: 11155420)

## Deployment Scripts

### Deploy ReputationNFT

```bash
cd contracts
npx hardhat run scripts/deploy.js --network sepolia
```

### Deploy SimpleToken

```bash
cd solidity
npx hardhat run scripts/deploy.js --network sepolia
```

### Verify Contract

```bash
npx hardhat verify --network sepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

## Interacting with Deployed Contracts

### Using Python (Web3.py)

```python
from web3 import Web3

# Connect to Sepolia
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/YOUR_KEY'))

# ReputationNFT contract
nft_address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0'
nft_abi = [...] # Load from artifacts

contract = w3.eth.contract(address=nft_address, abi=nft_abi)

# Get total supply
total = contract.functions.totalSupply().call()
print(f"Total NFTs minted: {total}")

# Check if address has badge
has_badge = contract.functions.hasReputationBadge('0xYourAddress').call()
print(f"Has badge: {has_badge}")
```

### Using TypeScript (Ethers.js)

```typescript
import { ethers } from 'ethers';

// Connect to Sepolia
const provider = new ethers.JsonRpcProvider('https://sepolia.infura.io/v3/YOUR_KEY');

// ReputationNFT contract
const nftAddress = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0';
const nftAbi = [...]; // Load from artifacts

const contract = new ethers.Contract(nftAddress, nftAbi, provider);

// Get reputation data
const [score, tier, uri] = await contract.getReputationData(1);
console.log(`Score: ${score}, Tier: ${tier}`);
```

### Using JavaScript (Web3.js)

```javascript
const { Web3 } = require('web3');

// Connect to Sepolia
const web3 = new Web3('https://sepolia.infura.io/v3/YOUR_KEY');

// SimpleToken contract
const tokenAddress = '0x1234567890123456789012345678901234567890';
const tokenAbi = [...]; // Load from artifacts

const contract = new web3.eth.Contract(tokenAbi, tokenAddress);

// Get balance
const balance = await contract.methods.balanceOf('0xYourAddress').call();
console.log(`Balance: ${balance}`);
```

### Using Go (go-ethereum)

```go
package main

import (
    "github.com/ethereum/go-ethereum/ethclient"
    "github.com/ethereum/go-ethereum/common"
)

func main() {
    client, _ := ethclient.Dial("https://sepolia.infura.io/v3/YOUR_KEY")

    address := common.HexToAddress("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0")

    // Load contract ABI and interact...
}
```

## Contract ABIs

Contract ABIs are available in the following locations:

- **ReputationNFT**: `contracts/artifacts/contracts/ReputationNFT.sol/ReputationNFT.json`
- **SimpleToken**: `solidity/artifacts/contracts/SimpleToken.sol/SimpleToken.json`

## Faucets for Testing

### Sepolia ETH Faucets
- https://sepoliafaucet.com/
- https://www.alchemy.com/faucets/ethereum-sepolia
- https://faucet.quicknode.com/ethereum/sepolia

### Base Sepolia ETH
- https://www.coinbase.com/faucets/base-ethereum-goerli-faucet

### Optimism Sepolia ETH
- https://app.optimism.io/faucet

## Mainnet Deployments

> **⚠️ WARNING**: These are example addresses. No actual mainnet deployments exist yet.

### Production Checklist

Before deploying to mainnet:

- [ ] Complete security audit
- [ ] Test on all target testnets
- [ ] Verify gas optimization
- [ ] Review access controls
- [ ] Document emergency procedures
- [ ] Set up monitoring and alerts
- [ ] Prepare verification on Etherscan
- [ ] Configure multi-sig for ownership
- [ ] Test upgrade mechanisms (if applicable)
- [ ] Prepare incident response plan

## Deployment History

### v1.0.0 (Example)
- **Date**: 2024-01-15
- **Network**: Sepolia
- **Contracts**: ReputationNFT, SimpleToken
- **Changes**: Initial deployment
- **Gas Used**: ~2,500,000
- **Tx Hash**: `0x...`

## Contract Verification

All contracts are verified on Etherscan-compatible explorers:

```bash
# Verify on Sepolia
npx hardhat verify --network sepolia \
  0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0

# Verify with constructor args
npx hardhat verify --network sepolia \
  0x1234567890123456789012345678901234567890 \
  "Reflekt Test Token" "RTT" 1000000 18
```

## Integration Examples

### Get NFT Metadata

```bash
# Using curl
curl https://sepolia.infura.io/v3/YOUR_KEY \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"eth_call",
    "params":[{
      "to": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
      "data": "0xc87b56dd0000000000000000000000000000000000000000000000000000000000000001"
    }, "latest"],
    "id":1
  }'
```

### Transfer Tokens

```bash
# Using cast (Foundry)
cast send 0x1234567890123456789012345678901234567890 \
  "transfer(address,uint256)" \
  0xRecipient 1000000000000000000 \
  --rpc-url https://sepolia.infura.io/v3/YOUR_KEY \
  --private-key $PRIVATE_KEY
```

## Monitoring

### Events to Monitor

#### ReputationNFT
- `ReputationBadgeMinted(address,uint256,uint256,string,string)`
- `ReputationBadgeUpdated(address,uint256,uint256,string,string)`
- `Transfer(address,address,uint256)`

#### SimpleToken
- `Transfer(address,address,uint256)`
- `Approval(address,address,uint256)`

### Monitoring Tools
- [Tenderly](https://tenderly.co/)
- [Blocknative](https://www.blocknative.com/)
- [Etherscan Alerts](https://etherscan.io/myaddress)

## Support

For questions or issues with deployments:
- Open an issue on GitHub
- Check the documentation in `/docs`
- Review test files for usage examples

# 🐍 Python - Web3.py CLI Tools

Command-line utilities for blockchain operations built with Web3.py, demonstrating automation and scripting for Ethereum and EVM chains.

## 📋 Overview

`web3_cli.py` provides:
- ✅ Balance checking (ETH and ERC-20 tokens)
- ✅ Transaction lookup and details
- ✅ Smart contract interaction
- ✅ Wallet generation
- ✅ Block information retrieval
- ✅ Multi-chain support (Ethereum, Polygon, BSC, etc.)
- ✅ Automated transaction signing

## 🛠️ Built With

- **Python**: 3.8+
- **Web3.py**: 6.15+ (official Ethereum Python library)
- **eth-account**: Account management
- **eth-typing**: Type hints for Ethereum

## 🚀 Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or install globally
pip install web3 eth-account eth-typing
```

### Environment Setup

```bash
# Optional: Set default RPC URL
export WEB3_RPC_URL="https://eth.llamarpc.com"

# For private operations (NEVER commit this!)
export PRIVATE_KEY="0x..."
```

## 📖 Usage

### Get ETH Balance

```bash
# Check balance
python web3_cli.py balance 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb

# Output:
{
  "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "balance_wei": "1500000000000000000",
  "balance_eth": "1.5",
  "balance_formatted": "1.500000 ETH"
}
```

### Get Transaction Details

```bash
python web3_cli.py tx 0xabc123...

# Output includes: from, to, value, gas, status, etc.
```

### Check ERC-20 Token Balance

```bash
# Check USDC balance
python web3_cli.py token \
  0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb

# Output:
{
  "token_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  "holder_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "balance_formatted": "1000.000000 USDC",
  "decimals": 6,
  "symbol": "USDC"
}
```

### Generate New Wallet

```bash
python web3_cli.py generate

# Output:
{
  "address": "0x...",
  "private_key": "0x...",
  "warning": "⚠️  NEVER share your private key!"
}
```

### Get Block Information

```bash
# Latest block
python web3_cli.py block

# Specific block
python web3_cli.py block 18000000
```

### Using Custom RPC

```bash
# Polygon
python web3_cli.py --rpc https://polygon-rpc.com balance 0x...

# BSC
python web3_cli.py --rpc https://bsc-dataseed.binance.org balance 0x...

# Arbitrum
python web3_cli.py --rpc https://arb1.arbitrum.io/rpc balance 0x...
```

## 🔧 Programmatic Usage

```python
from web3_cli import Web3CLI

# Initialize
cli = Web3CLI('https://eth.llamarpc.com')

# Get balance
balance = cli.get_balance('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb')
print(f"Balance: {balance['balance_formatted']}")

# Check token balance
token_balance = cli.get_erc20_balance(
    '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',  # USDC
    '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb'
)
print(f"USDC Balance: {token_balance['balance_formatted']}")

# Call any contract function
result = cli.call_contract(
    contract_address='0x...',
    abi=[...],
    function_name='totalSupply'
)

# Generate wallet
new_wallet = cli.generate_wallet()
print(f"New address: {new_wallet['address']}")
```

## 🧪 Advanced Examples

### Batch Balance Checker

```python
#!/usr/bin/env python3
from web3_cli import Web3CLI

addresses = [
    '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
    '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
    # ... more addresses
]

cli = Web3CLI('https://eth.llamarpc.com')

for addr in addresses:
    balance = cli.get_balance(addr)
    print(f"{addr}: {balance['balance_formatted']}")
```

### Monitor New Blocks

```python
from web3_cli import Web3CLI
import time

cli = Web3CLI('https://eth.llamarpc.com')
last_block = 0

while True:
    block = cli.get_block_info()
    if block['number'] > last_block:
        print(f"New block: {block['number']} - {block['transactions_count']} txs")
        last_block = block['number']
    time.sleep(12)  # Ethereum block time
```

### Portfolio Tracker

```python
from web3_cli import Web3CLI

cli = Web3CLI('https://eth.llamarpc.com')

# Define your portfolio
PORTFOLIO = {
    'USDC': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    'USDT': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
    'DAI': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
}

YOUR_ADDRESS = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb'

print("📊 Portfolio Snapshot\n")

# Check ETH
eth_balance = cli.get_balance(YOUR_ADDRESS)
print(f"ETH: {eth_balance['balance_formatted']}")

# Check tokens
for name, address in PORTFOLIO.items():
    try:
        balance = cli.get_erc20_balance(address, YOUR_ADDRESS)
        print(f"{name}: {balance['balance_formatted']}")
    except Exception as e:
        print(f"{name}: Error - {e}")
```

## 🔒 Security Best Practices

- ✅ Never hardcode private keys
- ✅ Use environment variables for sensitive data
- ✅ Validate addresses before transactions
- ✅ Test on testnets first
- ✅ Use hardware wallets for production
- ✅ Keep dependencies updated

## 📊 Supported Networks

| Network | RPC URL |
|---------|---------|
| Ethereum | `https://eth.llamarpc.com` |
| Polygon | `https://polygon-rpc.com` |
| BSC | `https://bsc-dataseed.binance.org` |
| Arbitrum | `https://arb1.arbitrum.io/rpc` |
| Optimism | `https://mainnet.optimism.io` |
| Avalanche | `https://api.avax.network/ext/bc/C/rpc` |

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest test_web3_cli.py

# With coverage
pytest --cov=web3_cli test_web3_cli.py
```

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details

## 🔗 Resources

- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Ethereum Python Documentation](https://ethereum.org/en/developers/docs/programming-languages/python/)
- [eth-account API](https://eth-account.readthedocs.io/)
- [Infura API](https://infura.io/)
- [Alchemy API](https://www.alchemy.com/)

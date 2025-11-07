# 💎 Ruby - Blockchain Indexer

Elegant blockchain data indexing and analysis tool built with Ruby, demonstrating scripting for Web3 data pipelines.

## 📋 Overview

- ✅ JSON-RPC client for EVM chains
- ✅ Block indexing and analysis
- ✅ Transaction tracking
- ✅ Balance checking
- ✅ Statistical analysis
- ✅ Clean, idiomatic Ruby

## 🚀 Quick Start

```bash
# Run directly
ruby blockchain_indexer.rb

# Or make executable
chmod +x blockchain_indexer.rb
./blockchain_indexer.rb
```

## 📖 Usage

```ruby
require_relative 'blockchain_indexer'

indexer = BlockchainIndexer.new

# Get current block
block_num = indexer.current_block

# Check balance
balance = indexer.get_balance('0x...')

# Index blocks
blocks = indexer.index_blocks(100)

# Analyze
stats = indexer.analyze_blocks(blocks)
```

## 📄 License

MIT License

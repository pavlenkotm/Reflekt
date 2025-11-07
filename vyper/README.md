# 🐍 Vyper - Simple ETH Vault

A secure Ethereum vault contract written in Vyper, demonstrating an alternative to Solidity with Python-like syntax.

## 📋 Overview

`SimpleVault` is a basic ETH vault with:
- ✅ Deposit and withdraw functionality
- ✅ Individual user balance tracking
- ✅ Owner-controlled pause mechanism
- ✅ Ownership transfer capability
- ✅ Event logging for all operations

## 🔍 Why Vyper?

Vyper is designed for:
- **Security**: Eliminates many Solidity footguns
- **Simplicity**: Python-like syntax, easier to audit
- **Transparency**: No hidden behaviors or complex inheritance

## 🛠️ Built With

- **Vyper**: ^0.3.9
- **Python**: 3.8+ (for vyper compiler)
- **Ape**: Development framework (recommended)
- **Titanoboa**: Testing framework

## 🚀 Quick Start

### Installation

```bash
# Install Vyper compiler
pip install vyper

# Or using pipx
pipx install vyper

# Verify installation
vyper --version
```

### Compilation

```bash
# Compile contract
vyper vyper/SimpleVault.vy

# Generate ABI
vyper -f abi vyper/SimpleVault.vy > SimpleVault.abi

# Generate bytecode
vyper -f bytecode vyper/SimpleVault.vy > SimpleVault.bin
```

### Deployment with Ape

```bash
# Install Ape framework
pip install eth-ape

# Compile with Ape
ape compile

# Deploy to local network
ape run deploy --network ethereum:local:foundry

# Deploy to testnet
ape run deploy --network ethereum:sepolia:alchemy
```

## 📖 Contract Interface

### Functions

#### User Functions
- `deposit()` - Deposit ETH into vault (payable)
- `withdraw(amount: uint256)` - Withdraw specific amount
- `withdraw_all()` - Withdraw entire balance
- `get_balance(user: address)` - Check user's vault balance

#### Owner Functions
- `pause()` - Pause all deposits/withdrawals
- `unpause()` - Resume operations
- `transfer_ownership(new_owner: address)` - Transfer ownership

#### View Functions
- `owner()` - Get current owner address
- `total_deposited()` - Get total ETH deposited
- `is_paused()` - Check if contract is paused
- `get_contract_balance()` - Get contract's ETH balance

## 🧪 Testing with Titanoboa

```python
import ape
from ape import accounts

def test_deposit_withdraw():
    # Deploy contract
    owner = accounts[0]
    user = accounts[1]
    vault = owner.deploy(project.SimpleVault)

    # Deposit 1 ETH
    vault.deposit(sender=user, value="1 ether")
    assert vault.get_balance(user) == 10**18

    # Withdraw 0.5 ETH
    vault.withdraw(5 * 10**17, sender=user)
    assert vault.get_balance(user) == 5 * 10**17

    print("✅ Tests passed!")
```

## 📊 Example Usage

```python
from ape import accounts, project

# Deploy
owner = accounts[0]
vault = owner.deploy(project.SimpleVault)

# User deposits
user = accounts[1]
vault.deposit(sender=user, value="1 ether")

# Check balance
balance = vault.get_balance(user)
print(f"User balance: {balance / 10**18} ETH")

# Withdraw
vault.withdraw_all(sender=user)
```

## 🔒 Security Features

- ✅ No complex inheritance (reduces attack surface)
- ✅ Bounds and overflow checking by default
- ✅ Clear state mutability
- ✅ Simple, auditable code
- ✅ Reentrancy protection with built-in patterns

## 🆚 Vyper vs Solidity

| Feature | Vyper | Solidity |
|---------|-------|----------|
| Syntax | Python-like | JavaScript-like |
| Inheritance | ❌ No | ✅ Yes |
| Modifiers | ❌ No | ✅ Yes |
| Inline Assembly | ❌ No | ✅ Yes |
| Integer Overflow | ✅ Safe by default | ⚠️ Need SafeMath (<0.8) |
| Learning Curve | Easier | Steeper |

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details

## 🔗 Resources

- [Vyper Documentation](https://docs.vyperlang.org/)
- [Vyper by Example](https://vyper-by-example.org/)
- [Ape Framework](https://docs.apeworx.io/)
- [Titanoboa Testing](https://github.com/vyperlang/titanoboa)

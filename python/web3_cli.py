#!/usr/bin/env python3
"""
Web3 CLI Tools - Command-line utilities for blockchain operations
Demonstrates Python Web3.py usage for automation and scripting
"""

import sys
import argparse
import json
from typing import Optional, Dict, Any
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from eth_typing import Address
import os
from pathlib import Path


class Web3CLI:
    """Command-line interface for Web3 operations"""

    def __init__(self, rpc_url: str):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

        # Add PoA middleware for networks like Polygon, BSC
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to {rpc_url}")

        print(f"✅ Connected to {rpc_url}")
        print(f"📊 Chain ID: {self.w3.eth.chain_id}")

    def get_balance(self, address: str) -> Dict[str, Any]:
        """Get ETH balance of an address"""
        checksum_address = self.w3.to_checksum_address(address)
        balance_wei = self.w3.eth.get_balance(checksum_address)
        balance_eth = self.w3.from_wei(balance_wei, 'ether')

        return {
            'address': checksum_address,
            'balance_wei': str(balance_wei),
            'balance_eth': str(balance_eth),
            'balance_formatted': f"{balance_eth:.6f} ETH"
        }

    def get_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction details"""
        tx = self.w3.eth.get_transaction(tx_hash)
        receipt = self.w3.eth.get_transaction_receipt(tx_hash)

        return {
            'hash': tx['hash'].hex(),
            'from': tx['from'],
            'to': tx['to'],
            'value': str(self.w3.from_wei(tx['value'], 'ether')),
            'gas': tx['gas'],
            'gas_price': str(self.w3.from_wei(tx['gasPrice'], 'gwei')),
            'nonce': tx['nonce'],
            'block_number': tx['blockNumber'],
            'status': 'success' if receipt['status'] == 1 else 'failed',
            'gas_used': receipt['gasUsed'],
        }

    def send_transaction(
        self,
        private_key: str,
        to_address: str,
        value_eth: float,
        gas_price_gwei: Optional[float] = None
    ) -> str:
        """Send ETH transaction"""
        account = Account.from_key(private_key)
        to_checksum = self.w3.to_checksum_address(to_address)

        # Get nonce
        nonce = self.w3.eth.get_transaction_count(account.address)

        # Gas price
        if gas_price_gwei is None:
            gas_price = self.w3.eth.gas_price
        else:
            gas_price = self.w3.to_wei(gas_price_gwei, 'gwei')

        # Build transaction
        transaction = {
            'nonce': nonce,
            'to': to_checksum,
            'value': self.w3.to_wei(value_eth, 'ether'),
            'gas': 21000,
            'gasPrice': gas_price,
            'chainId': self.w3.eth.chain_id,
        }

        # Sign transaction
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)

        # Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        print(f"📤 Transaction sent: {tx_hash.hex()}")
        print("⏳ Waiting for confirmation...")

        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt['status'] == 1:
            print(f"✅ Transaction confirmed in block {receipt['blockNumber']}")
        else:
            print("❌ Transaction failed")

        return tx_hash.hex()

    def call_contract(
        self,
        contract_address: str,
        abi: list,
        function_name: str,
        *args
    ) -> Any:
        """Call a read-only contract function"""
        checksum_address = self.w3.to_checksum_address(contract_address)
        contract = self.w3.eth.contract(address=checksum_address, abi=abi)

        result = getattr(contract.functions, function_name)(*args).call()
        return result

    def get_erc20_balance(
        self,
        token_address: str,
        holder_address: str
    ) -> Dict[str, Any]:
        """Get ERC-20 token balance"""
        # Minimal ERC-20 ABI
        erc20_abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "symbol",
                "outputs": [{"name": "", "type": "string"}],
                "type": "function"
            },
        ]

        token = self.w3.eth.contract(
            address=self.w3.to_checksum_address(token_address),
            abi=erc20_abi
        )

        holder_checksum = self.w3.to_checksum_address(holder_address)

        balance = token.functions.balanceOf(holder_checksum).call()
        decimals = token.functions.decimals().call()
        symbol = token.functions.symbol().call()

        balance_formatted = balance / (10 ** decimals)

        return {
            'token_address': token_address,
            'holder_address': holder_address,
            'balance_raw': str(balance),
            'balance_formatted': f"{balance_formatted:.6f} {symbol}",
            'decimals': decimals,
            'symbol': symbol,
        }

    def generate_wallet(self) -> Dict[str, str]:
        """Generate a new Ethereum wallet"""
        account = Account.create()

        return {
            'address': account.address,
            'private_key': account.key.hex(),
            'warning': '⚠️  NEVER share your private key!'
        }

    def get_block_info(self, block_number: int = None) -> Dict[str, Any]:
        """Get block information"""
        block = self.w3.eth.get_block(block_number or 'latest')

        return {
            'number': block['number'],
            'hash': block['hash'].hex(),
            'parent_hash': block['parentHash'].hex(),
            'timestamp': block['timestamp'],
            'transactions_count': len(block['transactions']),
            'gas_used': block['gasUsed'],
            'gas_limit': block['gasLimit'],
            'miner': block.get('miner', 'N/A'),
        }


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Web3 CLI - Blockchain operations from command line'
    )

    parser.add_argument(
        '--rpc',
        default=os.getenv('WEB3_RPC_URL', 'https://eth.llamarpc.com'),
        help='RPC endpoint URL'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Balance command
    balance_parser = subparsers.add_parser('balance', help='Get ETH balance')
    balance_parser.add_argument('address', help='Ethereum address')

    # Transaction command
    tx_parser = subparsers.add_parser('tx', help='Get transaction details')
    tx_parser.add_argument('hash', help='Transaction hash')

    # Token balance command
    token_parser = subparsers.add_parser('token', help='Get ERC-20 token balance')
    token_parser.add_argument('token_address', help='Token contract address')
    token_parser.add_argument('holder_address', help='Holder address')

    # Generate wallet
    subparsers.add_parser('generate', help='Generate new wallet')

    # Block info
    block_parser = subparsers.add_parser('block', help='Get block info')
    block_parser.add_argument(
        'number',
        nargs='?',
        type=int,
        help='Block number (default: latest)'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        cli = Web3CLI(args.rpc)

        if args.command == 'balance':
            result = cli.get_balance(args.address)
            print(json.dumps(result, indent=2))

        elif args.command == 'tx':
            result = cli.get_transaction(args.hash)
            print(json.dumps(result, indent=2))

        elif args.command == 'token':
            result = cli.get_erc20_balance(args.token_address, args.holder_address)
            print(json.dumps(result, indent=2))

        elif args.command == 'generate':
            result = cli.generate_wallet()
            print(json.dumps(result, indent=2))

        elif args.command == 'block':
            result = cli.get_block_info(args.number)
            print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

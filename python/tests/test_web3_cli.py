"""
Unit tests for Web3 CLI tools
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from web3 import Web3
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from web3_cli import Web3CLI


class TestWeb3CLI:
    """Test cases for Web3CLI class"""

    @pytest.fixture
    def mock_w3(self):
        """Create mock Web3 instance"""
        with patch('web3_cli.Web3') as mock:
            w3_instance = Mock()
            w3_instance.is_connected.return_value = True
            w3_instance.eth.chain_id = 1
            mock.return_value = w3_instance
            yield w3_instance

    @pytest.fixture
    def cli(self, mock_w3):
        """Create Web3CLI instance with mocked connection"""
        with patch('builtins.print'):  # Suppress connection messages
            cli = Web3CLI('http://localhost:8545')
        return cli

    def test_initialization_success(self, mock_w3):
        """Test successful Web3 connection"""
        with patch('builtins.print'):
            cli = Web3CLI('http://localhost:8545')
        assert cli.w3.is_connected()

    def test_initialization_failure(self):
        """Test failed Web3 connection"""
        with patch('web3_cli.Web3') as mock:
            w3_instance = Mock()
            w3_instance.is_connected.return_value = False
            mock.return_value = w3_instance

            with pytest.raises(ConnectionError):
                Web3CLI('http://invalid')

    def test_get_balance(self, cli, mock_w3):
        """Test getting ETH balance"""
        mock_w3.to_checksum_address.return_value = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0'
        mock_w3.eth.get_balance.return_value = 1000000000000000000  # 1 ETH in wei
        mock_w3.from_wei.return_value = 1.0

        result = cli.get_balance('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0')

        assert result['address'] == '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0'
        assert result['balance_wei'] == '1000000000000000000'
        assert 'balance_eth' in result

    def test_generate_wallet(self, cli):
        """Test wallet generation"""
        with patch('web3_cli.Account') as mock_account:
            mock_wallet = Mock()
            mock_wallet.address = '0x1234567890123456789012345678901234567890'
            mock_wallet.key.hex.return_value = '0xabcdef'
            mock_account.create.return_value = mock_wallet

            result = cli.generate_wallet()

            assert 'address' in result
            assert 'private_key' in result
            assert 'warning' in result

    def test_get_block_info(self, cli, mock_w3):
        """Test getting block information"""
        mock_block = {
            'number': 12345,
            'hash': b'\x12\x34',
            'parentHash': b'\x56\x78',
            'timestamp': 1234567890,
            'transactions': ['0xtx1', '0xtx2'],
            'gasUsed': 21000,
            'gasLimit': 30000000,
            'miner': '0xminer'
        }
        mock_w3.eth.get_block.return_value = mock_block

        result = cli.get_block_info(12345)

        assert result['number'] == 12345
        assert result['transactions_count'] == 2
        assert result['gas_used'] == 21000

    def test_call_contract(self, cli, mock_w3):
        """Test calling contract function"""
        mock_contract = Mock()
        mock_function = Mock()
        mock_function.call.return_value = 1000
        mock_contract.functions.balanceOf = Mock(return_value=mock_function)

        mock_w3.eth.contract.return_value = mock_contract
        mock_w3.to_checksum_address.return_value = '0xContract'

        result = cli.call_contract(
            '0xContract',
            [],
            'balanceOf',
            '0xAddress'
        )

        assert result == 1000

    def test_get_erc20_balance(self, cli, mock_w3):
        """Test getting ERC-20 token balance"""
        mock_contract = Mock()

        # Mock contract functions
        balance_func = Mock()
        balance_func.call.return_value = 1000000000000000000  # 1 token

        decimals_func = Mock()
        decimals_func.call.return_value = 18

        symbol_func = Mock()
        symbol_func.call.return_value = 'TEST'

        mock_contract.functions.balanceOf.return_value = balance_func
        mock_contract.functions.decimals.return_value = decimals_func
        mock_contract.functions.symbol.return_value = symbol_func

        mock_w3.eth.contract.return_value = mock_contract
        mock_w3.to_checksum_address.side_effect = lambda x: x

        result = cli.get_erc20_balance(
            '0xToken',
            '0xHolder'
        )

        assert result['balance_raw'] == '1000000000000000000'
        assert result['decimals'] == 18
        assert result['symbol'] == 'TEST'


class TestUtils:
    """Test utility functions"""

    def test_address_validation(self):
        """Test Ethereum address validation"""
        # Valid addresses
        assert Web3.is_address('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0')
        assert Web3.is_address('0x0000000000000000000000000000000000000000')

        # Invalid addresses
        assert not Web3.is_address('0x123')
        assert not Web3.is_address('invalid')

    def test_wei_conversion(self):
        """Test wei/ether conversion"""
        assert Web3.from_wei(1000000000000000000, 'ether') == 1
        assert Web3.to_wei(1, 'ether') == 1000000000000000000


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

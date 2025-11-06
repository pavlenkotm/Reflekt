"""
Wallet Scanner Module
Analyzes wallet activity: transactions, NFTs, DAO participation, ENS, token diversity
"""

from typing import Dict, List, Optional
from web3 import Web3
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


class WalletScanner:
    """Scans and analyzes Web3 wallet activity"""

    def __init__(self, rpc_url: Optional[str] = None):
        """Initialize scanner with RPC URL"""
        self.rpc_url = rpc_url or os.getenv("ETHEREUM_RPC_URL")
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

    def is_valid_address(self, address: str) -> bool:
        """Check if address is valid Ethereum address"""
        return Web3.is_address(address)

    def get_transaction_count(self, address: str) -> int:
        """Get total number of transactions for address"""
        try:
            checksum_address = Web3.to_checksum_address(address)
            return self.w3.eth.get_transaction_count(checksum_address)
        except Exception as e:
            print(f"Error getting transaction count: {e}")
            return 0

    def get_balance(self, address: str) -> float:
        """Get ETH balance for address"""
        try:
            checksum_address = Web3.to_checksum_address(address)
            balance_wei = self.w3.eth.get_balance(checksum_address)
            return float(self.w3.from_wei(balance_wei, 'ether'))
        except Exception as e:
            print(f"Error getting balance: {e}")
            return 0.0

    def analyze_wallet(self, address: str) -> Dict:
        """
        Comprehensive wallet analysis
        Returns dict with all metrics needed for reputation score
        """
        if not self.is_valid_address(address):
            raise ValueError(f"Invalid Ethereum address: {address}")

        checksum_address = Web3.to_checksum_address(address)

        # Basic metrics
        tx_count = self.get_transaction_count(checksum_address)
        balance = self.get_balance(checksum_address)

        # Wallet age estimation (based on first block - simplified)
        # In production, use Etherscan/Alchemy API for accurate first transaction
        current_block = self.w3.eth.block_number
        wallet_age_days = self._estimate_wallet_age(checksum_address)

        analysis = {
            "address": checksum_address,
            "transaction_count": tx_count,
            "balance": balance,
            "wallet_age_days": wallet_age_days,
            "is_active": tx_count > 0,
            "activity_level": self._categorize_activity(tx_count),

            # Extended metrics (would require external APIs in production)
            "nft_count": self._get_nft_count(checksum_address),
            "dao_participations": self._get_dao_participation(checksum_address),
            "token_diversity": self._get_token_diversity(checksum_address),
            "ens_name": self._get_ens_name(checksum_address),
            "defi_interactions": self._get_defi_interactions(checksum_address),

            "timestamp": datetime.now().isoformat()
        }

        return analysis

    def _estimate_wallet_age(self, address: str) -> int:
        """
        Estimate wallet age in days
        Simplified version - in production use historical data from indexer
        """
        # This is a placeholder - real implementation would query blockchain history
        # Using transaction count as a proxy for age
        tx_count = self.get_transaction_count(address)

        # Rough estimation: assume ~1 tx per week for average user
        estimated_days = min(tx_count * 7, 1825)  # cap at 5 years
        return estimated_days

    def _categorize_activity(self, tx_count: int) -> str:
        """Categorize wallet activity level"""
        if tx_count == 0:
            return "inactive"
        elif tx_count < 10:
            return "beginner"
        elif tx_count < 100:
            return "active"
        elif tx_count < 500:
            return "power_user"
        else:
            return "whale"

    def _get_nft_count(self, address: str) -> int:
        """
        Get NFT count for address
        Placeholder - requires Alchemy NFT API or similar
        """
        # In production: Use Alchemy NFT API or Moralis
        # For now, return mock data based on tx count
        tx_count = self.get_transaction_count(address)
        return min(tx_count // 10, 50)  # Estimate

    def _get_dao_participation(self, address: str) -> List[Dict]:
        """
        Get DAO participation data
        Placeholder - requires Snapshot API or on-chain governance tracking
        """
        # In production: Query Snapshot API, Tally, or governance contracts
        # Mock data for demonstration
        tx_count = self.get_transaction_count(address)

        if tx_count > 100:
            return [
                {"name": "Example DAO", "proposals_voted": 5},
                {"name": "Community DAO", "proposals_voted": 3}
            ]
        elif tx_count > 50:
            return [{"name": "Example DAO", "proposals_voted": 2}]
        else:
            return []

    def _get_token_diversity(self, address: str) -> int:
        """
        Calculate token diversity (number of different tokens held)
        Placeholder - requires token balance API
        """
        # In production: Use Alchemy Token API or Moralis
        tx_count = self.get_transaction_count(address)
        return min(tx_count // 20, 20)  # Estimate

    def _get_ens_name(self, address: str) -> Optional[str]:
        """
        Get ENS name for address
        Requires ENS registry lookup
        """
        try:
            # Simplified ENS lookup
            # In production: Use web3.py ENS module or ENS subgraph
            ens_name = self.w3.ens.name(address)
            return ens_name
        except Exception as e:
            return None

    def _get_defi_interactions(self, address: str) -> Dict:
        """
        Get DeFi protocol interaction stats
        Placeholder - requires protocol-specific queries
        """
        # In production: Query Uniswap, Aave, Compound, etc. subgraphs
        tx_count = self.get_transaction_count(address)

        return {
            "uniswap_swaps": max(0, tx_count // 5),
            "aave_interactions": max(0, tx_count // 10),
            "total_defi_protocols": min(tx_count // 30, 10)
        }


class TheGraphScanner:
    """
    Scanner using TheGraph for more detailed analysis
    Placeholder for production implementation
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("THEGRAPH_API_KEY")

    async def query_subgraph(self, subgraph_url: str, query: str):
        """Query TheGraph subgraph"""
        # Implementation would use gql library to query subgraphs
        pass

    async def get_uniswap_activity(self, address: str):
        """Query Uniswap subgraph for trading activity"""
        pass

    async def get_ens_domains(self, address: str):
        """Query ENS subgraph for owned domains"""
        pass


if __name__ == "__main__":
    # Example usage
    scanner = WalletScanner()

    # Example address (Vitalik's address for demo)
    test_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

    try:
        print(f"Analyzing wallet: {test_address}")
        analysis = scanner.analyze_wallet(test_address)

        print("\n=== Wallet Analysis ===")
        for key, value in analysis.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {e}")

"""
Reputation Score Calculator
Calculates Web3 reputation score (0-100) based on wallet activity
"""

from typing import Dict, List
from datetime import datetime


class ReputationCalculator:
    """
    Calculates reputation score based on wallet metrics
    Score range: 0-100
    """

    # Score weights configuration
    WEIGHTS = {
        "long_term_holder": 10,      # Hold ETH/tokens for extended period
        "dao_participation": 20,      # Active in governance
        "nft_mints": 5,              # Early NFT minter
        "frequent_swaps": -5,         # Day trader penalty
        "transaction_volume": 15,     # Overall activity
        "token_diversity": 10,        # Portfolio diversity
        "defi_usage": 15,            # DeFi protocol usage
        "wallet_age": 10,            # Account age
        "ens_ownership": 5,          # ENS domain ownership
        "balance": 5,                # Current ETH balance
    }

    # Tier thresholds
    TIERS = {
        "legendary": 90,
        "epic": 75,
        "rare": 60,
        "uncommon": 40,
        "common": 20,
        "novice": 0
    }

    def __init__(self):
        """Initialize reputation calculator"""
        self.max_score = 100
        self.min_score = 0

    def calculate_score(self, wallet_analysis: Dict) -> Dict:
        """
        Calculate comprehensive reputation score

        Args:
            wallet_analysis: Dict from WalletScanner.analyze_wallet()

        Returns:
            Dict with score, breakdown, tier, and badges
        """
        scores = {}

        # 1. Long-term holder score (0-10 points)
        scores["long_term_holder"] = self._calculate_holder_score(wallet_analysis)

        # 2. DAO participation (0-20 points)
        scores["dao_participation"] = self._calculate_dao_score(wallet_analysis)

        # 3. NFT mints (0-5 points, can be more with bonuses)
        scores["nft_mints"] = self._calculate_nft_score(wallet_analysis)

        # 4. Frequent swaps penalty (0 to -5 points)
        scores["frequent_swaps"] = self._calculate_swap_penalty(wallet_analysis)

        # 5. Transaction volume (0-15 points)
        scores["transaction_volume"] = self._calculate_transaction_score(wallet_analysis)

        # 6. Token diversity (0-10 points)
        scores["token_diversity"] = self._calculate_diversity_score(wallet_analysis)

        # 7. DeFi usage (0-15 points)
        scores["defi_usage"] = self._calculate_defi_score(wallet_analysis)

        # 8. Wallet age (0-10 points)
        scores["wallet_age"] = self._calculate_age_score(wallet_analysis)

        # 9. ENS ownership (0-5 points)
        scores["ens_ownership"] = self._calculate_ens_score(wallet_analysis)

        # 10. Balance score (0-5 points)
        scores["balance"] = self._calculate_balance_score(wallet_analysis)

        # Calculate total score
        total_score = sum(scores.values())
        total_score = max(self.min_score, min(self.max_score, total_score))

        # Determine tier
        tier = self._get_tier(total_score)

        # Determine special badges
        badges = self._calculate_badges(wallet_analysis, scores)

        return {
            "total_score": round(total_score, 2),
            "score_breakdown": scores,
            "tier": tier,
            "badges": badges,
            "calculated_at": datetime.now().isoformat(),
            "address": wallet_analysis.get("address")
        }

    def _calculate_holder_score(self, analysis: Dict) -> float:
        """
        Long-term holder score
        Based on wallet age and balance stability
        """
        age_days = analysis.get("wallet_age_days", 0)
        balance = analysis.get("balance", 0)

        # Score increases with age
        if age_days >= 1825:  # 5+ years
            age_score = 10
        elif age_days >= 1095:  # 3+ years
            age_score = 8
        elif age_days >= 365:  # 1+ year
            age_score = 6
        elif age_days >= 180:  # 6+ months
            age_score = 4
        else:
            age_score = 2

        # Bonus for holding balance
        if balance > 1:
            age_score = min(age_score + 2, 10)

        return age_score

    def _calculate_dao_score(self, analysis: Dict) -> float:
        """DAO participation score"""
        dao_list = analysis.get("dao_participations", [])

        if not dao_list:
            return 0

        # Points per DAO
        score = len(dao_list) * 5

        # Bonus for voting activity
        total_votes = sum(dao.get("proposals_voted", 0) for dao in dao_list)
        score += min(total_votes * 2, 10)

        return min(score, 20)

    def _calculate_nft_score(self, analysis: Dict) -> float:
        """NFT minting and ownership score"""
        nft_count = analysis.get("nft_count", 0)

        if nft_count == 0:
            return 0
        elif nft_count < 5:
            return 2
        elif nft_count < 20:
            return 4
        else:
            return 5

    def _calculate_swap_penalty(self, analysis: Dict) -> float:
        """
        Penalty for excessive day trading
        Rewards long-term holding over speculation
        """
        defi = analysis.get("defi_interactions", {})
        swaps = defi.get("uniswap_swaps", 0)
        tx_count = analysis.get("transaction_count", 0)

        # If swaps are more than 50% of transactions, apply penalty
        if tx_count > 0:
            swap_ratio = swaps / tx_count
            if swap_ratio > 0.5:
                return -5
            elif swap_ratio > 0.3:
                return -3
            elif swap_ratio > 0.2:
                return -1

        return 0

    def _calculate_transaction_score(self, analysis: Dict) -> float:
        """Transaction volume score"""
        tx_count = analysis.get("transaction_count", 0)

        if tx_count >= 1000:
            return 15
        elif tx_count >= 500:
            return 12
        elif tx_count >= 200:
            return 10
        elif tx_count >= 100:
            return 8
        elif tx_count >= 50:
            return 6
        elif tx_count >= 20:
            return 4
        elif tx_count >= 5:
            return 2
        else:
            return 0

    def _calculate_diversity_score(self, analysis: Dict) -> float:
        """Token diversity score"""
        diversity = analysis.get("token_diversity", 0)

        if diversity >= 15:
            return 10
        elif diversity >= 10:
            return 8
        elif diversity >= 5:
            return 5
        elif diversity >= 2:
            return 3
        else:
            return 0

    def _calculate_defi_score(self, analysis: Dict) -> float:
        """DeFi protocol usage score"""
        defi = analysis.get("defi_interactions", {})
        protocols = defi.get("total_defi_protocols", 0)

        if protocols >= 8:
            return 15
        elif protocols >= 5:
            return 12
        elif protocols >= 3:
            return 9
        elif protocols >= 1:
            return 5
        else:
            return 0

    def _calculate_age_score(self, analysis: Dict) -> float:
        """Wallet age score"""
        age_days = analysis.get("wallet_age_days", 0)

        if age_days >= 1825:  # 5+ years
            return 10
        elif age_days >= 1095:  # 3+ years
            return 8
        elif age_days >= 730:  # 2+ years
            return 6
        elif age_days >= 365:  # 1+ year
            return 4
        elif age_days >= 180:  # 6+ months
            return 2
        else:
            return 0

    def _calculate_ens_score(self, analysis: Dict) -> float:
        """ENS ownership score"""
        ens_name = analysis.get("ens_name")
        return 5 if ens_name else 0

    def _calculate_balance_score(self, analysis: Dict) -> float:
        """Current balance score"""
        balance = analysis.get("balance", 0)

        if balance >= 10:
            return 5
        elif balance >= 5:
            return 4
        elif balance >= 1:
            return 3
        elif balance >= 0.1:
            return 2
        elif balance > 0:
            return 1
        else:
            return 0

    def _get_tier(self, score: float) -> str:
        """Determine reputation tier based on score"""
        for tier_name, threshold in self.TIERS.items():
            if score >= threshold:
                return tier_name
        return "novice"

    def _calculate_badges(self, analysis: Dict, scores: Dict) -> List[str]:
        """
        Calculate special achievement badges
        """
        badges = []

        # Early Adopter
        if analysis.get("wallet_age_days", 0) >= 1825:
            badges.append("Early Adopter")

        # DAO Voter
        if len(analysis.get("dao_participations", [])) >= 2:
            badges.append("DAO Voter")

        # NFT Collector
        if analysis.get("nft_count", 0) >= 20:
            badges.append("NFT Collector")

        # DeFi Native
        defi = analysis.get("defi_interactions", {})
        if defi.get("total_defi_protocols", 0) >= 5:
            badges.append("DeFi Native")

        # Power User
        if analysis.get("transaction_count", 0) >= 500:
            badges.append("Power User")

        # Whale
        if analysis.get("balance", 0) >= 10:
            badges.append("Whale")

        # Diamond Hands (long-term holder with good score)
        if scores.get("long_term_holder", 0) >= 8 and scores.get("frequent_swaps", 0) >= -1:
            badges.append("Diamond Hands")

        # ENS Owner
        if analysis.get("ens_name"):
            badges.append("ENS Owner")

        # Diversified
        if analysis.get("token_diversity", 0) >= 10:
            badges.append("Diversified Portfolio")

        return badges

    def get_tier_description(self, tier: str) -> str:
        """Get description for reputation tier"""
        descriptions = {
            "legendary": "Elite Web3 contributor with exceptional on-chain reputation",
            "epic": "Highly respected community member with strong track record",
            "rare": "Active participant with solid Web3 presence",
            "uncommon": "Regular user showing consistent engagement",
            "common": "Growing presence in Web3 ecosystem",
            "novice": "Beginning the Web3 journey"
        }
        return descriptions.get(tier, "Unknown tier")


if __name__ == "__main__":
    # Example usage
    from wallet_scanner import WalletScanner

    scanner = WalletScanner()
    calculator = ReputationCalculator()

    # Example address
    test_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

    try:
        # Analyze wallet
        print(f"Analyzing wallet: {test_address}\n")
        analysis = scanner.analyze_wallet(test_address)

        # Calculate reputation
        reputation = calculator.calculate_score(analysis)

        print("=== REPUTATION REPORT ===")
        print(f"Total Score: {reputation['total_score']}/100")
        print(f"Tier: {reputation['tier'].upper()}")
        print(f"\nScore Breakdown:")
        for category, score in reputation['score_breakdown'].items():
            print(f"  {category}: {score}")

        print(f"\nBadges Earned: {', '.join(reputation['badges']) if reputation['badges'] else 'None'}")
        print(f"\nTier Description: {calculator.get_tier_description(reputation['tier'])}")

    except Exception as e:
        print(f"Error: {e}")

"""
Bonus Feature Integrations
- Lens Protocol integration
- Advanced leaderboard features
- DAO recruitment API
"""

from typing import Dict, List, Optional
import requests
import json
from datetime import datetime


class LensProtocolIntegration:
    """
    Integration with Lens Protocol for Web3 social features
    """

    def __init__(self):
        """Initialize Lens Protocol integration"""
        self.lens_api_url = "https://api.lens.dev"

    def get_lens_profile(self, address: str) -> Optional[Dict]:
        """
        Get Lens Protocol profile for an address

        Args:
            address: Ethereum address

        Returns:
            Lens profile data or None
        """
        # Query Lens Protocol API
        query = """
        query Profile($address: EthereumAddress!) {
            defaultProfile(request: { ethereumAddress: $address }) {
                id
                name
                handle
                bio
                picture {
                    ... on MediaSet {
                        original {
                            url
                        }
                    }
                }
                stats {
                    totalFollowers
                    totalFollowing
                    totalPosts
                    totalComments
                    totalMirrors
                }
            }
        }
        """

        try:
            response = requests.post(
                self.lens_api_url,
                json={
                    "query": query,
                    "variables": {"address": address}
                },
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("data", {}).get("defaultProfile")

        except Exception as e:
            print(f"Error fetching Lens profile: {e}")

        return None

    def calculate_lens_score(self, lens_profile: Dict) -> float:
        """
        Calculate additional reputation points from Lens activity

        Args:
            lens_profile: Lens profile data

        Returns:
            Bonus score (0-10 points)
        """
        if not lens_profile:
            return 0

        stats = lens_profile.get("stats", {})

        followers = stats.get("totalFollowers", 0)
        posts = stats.get("totalPosts", 0)
        comments = stats.get("totalComments", 0)
        mirrors = stats.get("totalMirrors", 0)

        # Calculate score
        score = 0

        # Followers contribution (0-4 points)
        if followers >= 1000:
            score += 4
        elif followers >= 500:
            score += 3
        elif followers >= 100:
            score += 2
        elif followers >= 10:
            score += 1

        # Content creation (0-3 points)
        total_content = posts + comments
        if total_content >= 100:
            score += 3
        elif total_content >= 50:
            score += 2
        elif total_content >= 10:
            score += 1

        # Engagement (0-3 points)
        if mirrors >= 50:
            score += 3
        elif mirrors >= 20:
            score += 2
        elif mirrors >= 5:
            score += 1

        return min(score, 10)


class DAORecruitmentAPI:
    """
    API for DAOs to search and recruit based on reputation scores
    """

    def __init__(self):
        """Initialize DAO recruitment API"""
        self.profiles_db = []  # In production, use real database

    def add_profile(self, address: str, reputation: Dict, analysis: Dict):
        """
        Add a profile to the recruitment database

        Args:
            address: Wallet address
            reputation: Reputation data
            analysis: Wallet analysis data
        """
        profile = {
            "address": address,
            "score": reputation.get("total_score"),
            "tier": reputation.get("tier"),
            "badges": reputation.get("badges", []),
            "transaction_count": analysis.get("transaction_count"),
            "dao_participations": len(analysis.get("dao_participations", [])),
            "nft_count": analysis.get("nft_count"),
            "token_diversity": analysis.get("token_diversity"),
            "wallet_age_days": analysis.get("wallet_age_days"),
            "activity_level": analysis.get("activity_level"),
            "added_at": datetime.now().isoformat()
        }

        # Remove existing profile for this address
        self.profiles_db = [p for p in self.profiles_db if p["address"] != address]

        # Add new profile
        self.profiles_db.append(profile)

    def search_candidates(
        self,
        min_score: Optional[int] = None,
        min_dao_participation: Optional[int] = None,
        required_badges: Optional[List[str]] = None,
        min_transaction_count: Optional[int] = None,
        tier: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for candidates based on criteria

        Args:
            min_score: Minimum reputation score
            min_dao_participation: Minimum number of DAO participations
            required_badges: List of required badges
            min_transaction_count: Minimum transaction count
            tier: Required tier

        Returns:
            List of matching profiles
        """
        results = self.profiles_db.copy()

        # Apply filters
        if min_score is not None:
            results = [p for p in results if p["score"] >= min_score]

        if min_dao_participation is not None:
            results = [p for p in results if p["dao_participations"] >= min_dao_participation]

        if required_badges:
            results = [
                p for p in results
                if all(badge in p["badges"] for badge in required_badges)
            ]

        if min_transaction_count is not None:
            results = [p for p in results if p["transaction_count"] >= min_transaction_count]

        if tier:
            results = [p for p in results if p["tier"] == tier]

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)

        return results

    def get_dao_recommendations(self, dao_requirements: Dict) -> List[Dict]:
        """
        Get recommended candidates for a DAO based on their requirements

        Args:
            dao_requirements: Dict with DAO requirements

        Returns:
            List of recommended profiles
        """
        return self.search_candidates(
            min_score=dao_requirements.get("min_score"),
            min_dao_participation=dao_requirements.get("min_dao_participation"),
            required_badges=dao_requirements.get("required_badges"),
            min_transaction_count=dao_requirements.get("min_transaction_count"),
            tier=dao_requirements.get("tier")
        )


class AdvancedLeaderboard:
    """
    Advanced leaderboard with filtering and categories
    """

    def __init__(self, data_file: str = "./data/leaderboard.json"):
        """Initialize advanced leaderboard"""
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        """Load leaderboard data from file"""
        try:
            with open(self.data_file, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def save_data(self):
        """Save leaderboard data to file"""
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def get_by_tier(self, tier: str) -> List[Dict]:
        """Get leaderboard filtered by tier"""
        return [entry for entry in self.data if entry["tier"] == tier]

    def get_by_badge(self, badge: str) -> List[Dict]:
        """Get users who have a specific badge"""
        return [entry for entry in self.data if badge in entry.get("badges", [])]

    def get_top_by_category(self, category: str, limit: int = 10) -> List[Dict]:
        """
        Get top users by specific category

        Categories:
        - dao_participation
        - nft_collector
        - defi_user
        - early_adopter
        """
        category_badges = {
            "dao_participation": "DAO Voter",
            "nft_collector": "NFT Collector",
            "defi_user": "DeFi Native",
            "early_adopter": "Early Adopter"
        }

        badge = category_badges.get(category)
        if not badge:
            return []

        filtered = self.get_by_badge(badge)
        return sorted(filtered, key=lambda x: x["score"], reverse=True)[:limit]

    def get_rising_stars(self, days: int = 7) -> List[Dict]:
        """
        Get recently added high-performing users

        Args:
            days: Number of days to look back

        Returns:
            List of rising star profiles
        """
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=days)

        recent = [
            entry for entry in self.data
            if datetime.fromisoformat(entry.get("updated_at", "2020-01-01")) > cutoff_date
        ]

        # Filter for high scores only
        rising = [entry for entry in recent if entry["score"] >= 60]

        return sorted(rising, key=lambda x: x["score"], reverse=True)

    def get_statistics(self) -> Dict:
        """Get overall leaderboard statistics"""
        if not self.data:
            return {}

        scores = [entry["score"] for entry in self.data]
        tiers = [entry["tier"] for entry in self.data]

        # Tier distribution
        tier_counts = {}
        for tier in ["legendary", "epic", "rare", "uncommon", "common", "novice"]:
            tier_counts[tier] = len([t for t in tiers if t == tier])

        return {
            "total_users": len(self.data),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "highest_score": max(scores) if scores else 0,
            "lowest_score": min(scores) if scores else 0,
            "tier_distribution": tier_counts,
            "total_badges_awarded": sum(len(entry.get("badges", [])) for entry in self.data)
        }


# Export utilities
class ProfileExporter:
    """
    Export profiles in various formats for different use cases
    """

    @staticmethod
    def export_for_dao(reputation: Dict, analysis: Dict) -> Dict:
        """
        Export profile in DAO-friendly format

        Returns:
            Dict optimized for DAO recruitment
        """
        return {
            "wallet_address": reputation.get("address"),
            "reputation_score": reputation.get("total_score"),
            "tier": reputation.get("tier"),
            "governance_experience": {
                "dao_participations": len(analysis.get("dao_participations", [])),
                "dao_list": analysis.get("dao_participations", [])
            },
            "on_chain_activity": {
                "transaction_count": analysis.get("transaction_count"),
                "wallet_age_days": analysis.get("wallet_age_days"),
                "activity_level": analysis.get("activity_level")
            },
            "achievements": reputation.get("badges", []),
            "web3_experience": {
                "nft_count": analysis.get("nft_count"),
                "token_diversity": analysis.get("token_diversity"),
                "defi_protocols": analysis.get("defi_interactions", {}).get("total_defi_protocols")
            },
            "profile_timestamp": datetime.now().isoformat()
        }

    @staticmethod
    def export_for_recruitment(reputation: Dict, analysis: Dict) -> Dict:
        """
        Export profile for Web3 job recruitment

        Returns:
            Dict formatted for recruitment platforms
        """
        return {
            "candidate_address": reputation.get("address"),
            "overall_score": reputation.get("total_score"),
            "skill_level": reputation.get("tier"),
            "experience_summary": {
                "years_in_web3": analysis.get("wallet_age_days", 0) / 365,
                "transaction_count": analysis.get("transaction_count"),
                "activity_rating": analysis.get("activity_level")
            },
            "specializations": [],  # Derived from badges
            "achievements": reputation.get("badges", []),
            "governance_involvement": len(analysis.get("dao_participations", [])) > 0,
            "defi_experience": analysis.get("defi_interactions", {}).get("total_defi_protocols", 0) > 0,
            "nft_familiarity": analysis.get("nft_count", 0) > 0,
            "generated_at": datetime.now().isoformat()
        }


if __name__ == "__main__":
    # Example usage

    # Lens Protocol
    lens = LensProtocolIntegration()
    print("=== Lens Protocol Integration ===")
    # profile = lens.get_lens_profile("0x...")
    # score = lens.calculate_lens_score(profile)
    # print(f"Lens Score: {score}")

    # DAO Recruitment
    print("\n=== DAO Recruitment API ===")
    dao_api = DAORecruitmentAPI()

    # Search example
    candidates = dao_api.search_candidates(min_score=70, min_dao_participation=2)
    print(f"Found {len(candidates)} candidates")

    # Advanced Leaderboard
    print("\n=== Advanced Leaderboard ===")
    leaderboard = AdvancedLeaderboard()
    stats = leaderboard.get_statistics()
    print(f"Leaderboard stats: {json.dumps(stats, indent=2)}")

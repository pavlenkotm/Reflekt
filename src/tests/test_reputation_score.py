"""
Unit tests for Reputation Score Calculator
"""

import pytest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from reputation_score import ReputationCalculator


class TestReputationCalculator:
    """Test cases for ReputationCalculator"""

    @pytest.fixture
    def calculator(self):
        """Create calculator instance"""
        return ReputationCalculator()

    @pytest.fixture
    def sample_wallet_novice(self):
        """Sample wallet data for novice user"""
        return {
            "address": "0x1234567890123456789012345678901234567890",
            "balance": 0.1,
            "wallet_age_days": 30,
            "transaction_count": 10,
            "token_diversity": 2,
            "nft_count": 0,
            "dao_participations": [],
            "defi_interactions": {
                "uniswap_swaps": 2,
                "total_defi_protocols": 1
            },
            "ens_name": None
        }

    @pytest.fixture
    def sample_wallet_legendary(self):
        """Sample wallet data for legendary user"""
        return {
            "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
            "balance": 15.5,
            "wallet_age_days": 2000,
            "transaction_count": 1500,
            "token_diversity": 25,
            "nft_count": 50,
            "dao_participations": [
                {"name": "Uniswap", "proposals_voted": 10},
                {"name": "Compound", "proposals_voted": 15},
                {"name": "Aave", "proposals_voted": 8}
            ],
            "defi_interactions": {
                "uniswap_swaps": 50,
                "total_defi_protocols": 10
            },
            "ens_name": "vitalik.eth"
        }

    def test_calculator_initialization(self, calculator):
        """Test calculator initialization"""
        assert calculator.max_score == 100
        assert calculator.min_score == 0
        assert len(calculator.WEIGHTS) == 10
        assert len(calculator.TIERS) == 6

    def test_calculate_score_novice(self, calculator, sample_wallet_novice):
        """Test score calculation for novice wallet"""
        result = calculator.calculate_score(sample_wallet_novice)

        assert result['total_score'] >= 0
        assert result['total_score'] <= 100
        assert result['tier'] in ['novice', 'common']
        assert 'score_breakdown' in result
        assert 'badges' in result
        assert result['address'] == sample_wallet_novice['address']

    def test_calculate_score_legendary(self, calculator, sample_wallet_legendary):
        """Test score calculation for legendary wallet"""
        result = calculator.calculate_score(sample_wallet_legendary)

        assert result['total_score'] >= 80  # Should be high score
        assert result['tier'] in ['epic', 'legendary']
        assert len(result['badges']) >= 3  # Should have multiple badges

    def test_holder_score_calculation(self, calculator):
        """Test long-term holder score calculation"""
        # New wallet
        analysis_new = {"wallet_age_days": 30, "balance": 0.1}
        score_new = calculator._calculate_holder_score(analysis_new)
        assert score_new >= 2
        assert score_new <= 4

        # 5-year old wallet with balance
        analysis_old = {"wallet_age_days": 2000, "balance": 5}
        score_old = calculator._calculate_holder_score(analysis_old)
        assert score_old == 10

    def test_dao_score_calculation(self, calculator):
        """Test DAO participation score"""
        # No DAO participation
        analysis_none = {"dao_participations": []}
        assert calculator._calculate_dao_score(analysis_none) == 0

        # Multiple DAOs with votes
        analysis_active = {
            "dao_participations": [
                {"proposals_voted": 5},
                {"proposals_voted": 10}
            ]
        }
        score = calculator._calculate_dao_score(analysis_active)
        assert score > 0
        assert score <= 20

    def test_nft_score_calculation(self, calculator):
        """Test NFT score calculation"""
        assert calculator._calculate_nft_score({"nft_count": 0}) == 0
        assert calculator._calculate_nft_score({"nft_count": 3}) == 2
        assert calculator._calculate_nft_score({"nft_count": 10}) == 4
        assert calculator._calculate_nft_score({"nft_count": 25}) == 5

    def test_swap_penalty(self, calculator):
        """Test frequent trading penalty"""
        # Low swap ratio - no penalty
        analysis_low = {
            "transaction_count": 100,
            "defi_interactions": {"uniswap_swaps": 10}
        }
        assert calculator._calculate_swap_penalty(analysis_low) == 0

        # High swap ratio - penalty
        analysis_high = {
            "transaction_count": 100,
            "defi_interactions": {"uniswap_swaps": 60}
        }
        assert calculator._calculate_swap_penalty(analysis_high) == -5

    def test_transaction_score(self, calculator):
        """Test transaction volume score"""
        assert calculator._calculate_transaction_score({"transaction_count": 5}) == 2
        assert calculator._calculate_transaction_score({"transaction_count": 100}) == 8
        assert calculator._calculate_transaction_score({"transaction_count": 500}) == 12
        assert calculator._calculate_transaction_score({"transaction_count": 1500}) == 15

    def test_diversity_score(self, calculator):
        """Test token diversity score"""
        assert calculator._calculate_diversity_score({"token_diversity": 1}) == 0
        assert calculator._calculate_diversity_score({"token_diversity": 5}) == 5
        assert calculator._calculate_diversity_score({"token_diversity": 10}) == 8
        assert calculator._calculate_diversity_score({"token_diversity": 20}) == 10

    def test_defi_score(self, calculator):
        """Test DeFi usage score"""
        analysis_none = {"defi_interactions": {"total_defi_protocols": 0}}
        assert calculator._calculate_defi_score(analysis_none) == 0

        analysis_active = {"defi_interactions": {"total_defi_protocols": 5}}
        assert calculator._calculate_defi_score(analysis_active) == 12

    def test_age_score(self, calculator):
        """Test wallet age score"""
        assert calculator._calculate_age_score({"wallet_age_days": 30}) == 0
        assert calculator._calculate_age_score({"wallet_age_days": 200}) == 2
        assert calculator._calculate_age_score({"wallet_age_days": 400}) == 4
        assert calculator._calculate_age_score({"wallet_age_days": 800}) == 6
        assert calculator._calculate_age_score({"wallet_age_days": 1200}) == 8
        assert calculator._calculate_age_score({"wallet_age_days": 2000}) == 10

    def test_ens_score(self, calculator):
        """Test ENS ownership score"""
        assert calculator._calculate_ens_score({"ens_name": None}) == 0
        assert calculator._calculate_ens_score({"ens_name": "vitalik.eth"}) == 5

    def test_balance_score(self, calculator):
        """Test balance score"""
        assert calculator._calculate_balance_score({"balance": 0}) == 0
        assert calculator._calculate_balance_score({"balance": 0.05}) == 1
        assert calculator._calculate_balance_score({"balance": 0.5}) == 2
        assert calculator._calculate_balance_score({"balance": 2}) == 3
        assert calculator._calculate_balance_score({"balance": 7}) == 4
        assert calculator._calculate_balance_score({"balance": 15}) == 5

    def test_tier_determination(self, calculator):
        """Test tier assignment based on score"""
        assert calculator._get_tier(95) == 'legendary'
        assert calculator._get_tier(80) == 'epic'
        assert calculator._get_tier(65) == 'rare'
        assert calculator._get_tier(50) == 'uncommon'
        assert calculator._get_tier(30) == 'common'
        assert calculator._get_tier(10) == 'novice'

    def test_badges_early_adopter(self, calculator):
        """Test Early Adopter badge"""
        analysis = {
            "wallet_age_days": 2000,
            "dao_participations": [],
            "nft_count": 0,
            "defi_interactions": {"total_defi_protocols": 0},
            "transaction_count": 10,
            "balance": 0.1,
            "ens_name": None,
            "token_diversity": 1
        }
        scores = {
            "long_term_holder": 10,
            "frequent_swaps": 0
        }
        badges = calculator._calculate_badges(analysis, scores)
        assert 'Early Adopter' in badges

    def test_badges_dao_voter(self, calculator):
        """Test DAO Voter badge"""
        analysis = {
            "wallet_age_days": 100,
            "dao_participations": [{"name": "DAO1"}, {"name": "DAO2"}],
            "nft_count": 0,
            "defi_interactions": {"total_defi_protocols": 0},
            "transaction_count": 10,
            "balance": 0.1,
            "ens_name": None,
            "token_diversity": 1
        }
        scores = {"long_term_holder": 5, "frequent_swaps": 0}
        badges = calculator._calculate_badges(analysis, scores)
        assert 'DAO Voter' in badges

    def test_badges_whale(self, calculator):
        """Test Whale badge"""
        analysis = {
            "wallet_age_days": 100,
            "dao_participations": [],
            "nft_count": 0,
            "defi_interactions": {"total_defi_protocols": 0},
            "transaction_count": 10,
            "balance": 15,
            "ens_name": None,
            "token_diversity": 1
        }
        scores = {"long_term_holder": 5, "frequent_swaps": 0}
        badges = calculator._calculate_badges(analysis, scores)
        assert 'Whale' in badges

    def test_score_bounds(self, calculator):
        """Test that scores are always within bounds"""
        # Extreme low case
        analysis_low = {
            "address": "0x123",
            "balance": 0,
            "wallet_age_days": 0,
            "transaction_count": 0,
            "token_diversity": 0,
            "nft_count": 0,
            "dao_participations": [],
            "defi_interactions": {
                "uniswap_swaps": 0,
                "total_defi_protocols": 0
            },
            "ens_name": None
        }
        result_low = calculator.calculate_score(analysis_low)
        assert result_low['total_score'] >= 0
        assert result_low['total_score'] <= 100

    def test_tier_descriptions(self, calculator):
        """Test tier descriptions"""
        assert 'Elite' in calculator.get_tier_description('legendary')
        assert 'respected' in calculator.get_tier_description('epic')
        assert 'Active' in calculator.get_tier_description('rare')
        assert 'Regular' in calculator.get_tier_description('uncommon')
        assert 'Growing' in calculator.get_tier_description('common')
        assert 'Beginning' in calculator.get_tier_description('novice')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

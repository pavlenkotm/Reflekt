"""
Streamlit Frontend for Web3 Reputation NFT
User-friendly dashboard for analyzing wallets and minting reputation badges
"""

import streamlit as st
import sys
import os
from pathlib import Path
import json
from datetime import datetime
import pandas as pd

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from wallet_scanner import WalletScanner
from reputation_score import ReputationCalculator
from badge_generator import BadgeGenerator, IPFSUploader

# Page config
st.set_page_config(
    page_title="Web3 Reputation NFT",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .badge-item {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        display: inline-block;
    }
    .tier-legendary { background: linear-gradient(135deg, #FFD700 0%, #FF6B35 100%); }
    .tier-epic { background: linear-gradient(135deg, #A020F0 0%, #00D9FF 100%); }
    .tier-rare { background: linear-gradient(135deg, #00B4D8 0%, #90E0EF 100%); }
    .tier-uncommon { background: linear-gradient(135deg, #06FFA5 0%, #2EC4B6 100%); }
    .tier-common { background: linear-gradient(135deg, #4ECDC4 0%, #44A1A0 100%); }
    .tier-novice { background: linear-gradient(135deg, #58A6FF 0%, #79C0FF 100%); }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis' not in st.session_state:
    st.session_state.analysis = None
if 'reputation' not in st.session_state:
    st.session_state.reputation = None
if 'badge_path' not in st.session_state:
    st.session_state.badge_path = None

# Initialize components
@st.cache_resource
def init_components():
    """Initialize scanner, calculator, and generator"""
    scanner = WalletScanner()
    calculator = ReputationCalculator()
    generator = BadgeGenerator()
    uploader = IPFSUploader()
    return scanner, calculator, generator, uploader

scanner, calculator, generator, uploader = init_components()

# Header
st.markdown("""
<div class="main-header">
    <h1>🌐 Web3 Reputation NFT</h1>
    <p>Analyze your on-chain reputation and mint your personalized badge</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=Reflekt", use_column_width=True)
    st.markdown("---")

    st.markdown("### 🔍 Navigation")
    page = st.radio(
        "Select Page:",
        ["🏠 Home", "📊 Analysis", "🏆 Leaderboard", "ℹ️ About"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 📚 Quick Stats")

    # Load leaderboard if exists
    try:
        with open("../data/leaderboard.json", "r") as f:
            leaderboard = json.load(f)
            st.metric("Total Badges", len(leaderboard))
            if leaderboard:
                avg_score = sum(e["score"] for e in leaderboard) / len(leaderboard)
                st.metric("Average Score", f"{avg_score:.1f}")
    except:
        st.metric("Total Badges", "0")

    st.markdown("---")
    st.markdown("### 🔗 Links")
    st.markdown("[📖 Documentation](https://github.com)")
    st.markdown("[🐛 Report Bug](https://github.com)")
    st.markdown("[💡 Request Feature](https://github.com)")

# Main content based on page selection
if "Home" in page:
    # Home Page
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🎯 Get Your Web3 Reputation Badge")

        st.markdown("""
        Analyze your on-chain activity and receive a personalized NFT badge representing your Web3 reputation.
        Our system evaluates:
        - 📈 Transaction history
        - 🗳️ DAO participation
        - 🎨 NFT collection
        - 💎 Token diversity
        - 🏦 DeFi protocol usage
        """)

        # Wallet input
        wallet_address = st.text_input(
            "Enter Ethereum Address",
            placeholder="0x...",
            help="Enter your Ethereum wallet address to analyze"
        )

        col_btn1, col_btn2, col_btn3 = st.columns(3)

        with col_btn1:
            if st.button("🔍 Analyze Wallet", type="primary", use_container_width=True):
                if wallet_address:
                    with st.spinner("Analyzing wallet..."):
                        try:
                            # Analyze wallet
                            analysis = scanner.analyze_wallet(wallet_address)
                            st.session_state.analysis = analysis

                            # Calculate reputation
                            reputation = calculator.calculate_score(analysis)
                            st.session_state.reputation = reputation

                            st.success("✓ Analysis complete!")

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please enter a wallet address")

        with col_btn2:
            if st.button("🎨 Generate Badge", use_container_width=True):
                if st.session_state.reputation:
                    with st.spinner("Generating badge..."):
                        try:
                            badge_path = generator.generate_badge(
                                st.session_state.reputation,
                                st.session_state.analysis
                            )
                            st.session_state.badge_path = badge_path
                            st.success("✓ Badge generated!")

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Analyze wallet first")

        with col_btn3:
            if st.button("🚀 Mint NFT", use_container_width=True):
                if st.session_state.badge_path:
                    with st.spinner("Uploading to IPFS..."):
                        try:
                            # Upload image
                            image_hash = uploader.upload_image(
                                st.session_state.badge_path,
                                f"badge_{wallet_address}"
                            )

                            if image_hash:
                                # Upload metadata
                                metadata = uploader.create_nft_metadata(
                                    st.session_state.reputation,
                                    image_hash,
                                    st.session_state.analysis
                                )
                                metadata_hash = uploader.upload_metadata(
                                    metadata,
                                    f"metadata_{wallet_address}"
                                )

                                if metadata_hash:
                                    st.success(f"✓ NFT Ready!")
                                    st.code(f"ipfs://{metadata_hash}", language="text")
                                    st.info("Use this URI to mint your NFT on-chain")
                            else:
                                st.error("Please configure PINATA credentials in .env")

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Generate badge first")

    with col2:
        st.markdown("### 📊 Tier System")

        tiers = [
            ("🏆 Legendary", "90-100", "#FFD700"),
            ("⭐ Epic", "75-89", "#A020F0"),
            ("💎 Rare", "60-74", "#00B4D8"),
            ("🔷 Uncommon", "40-59", "#06FFA5"),
            ("🔹 Common", "20-39", "#4ECDC4"),
            ("🌱 Novice", "0-19", "#58A6FF")
        ]

        for tier, score_range, color in tiers:
            st.markdown(f"""
            <div style="background: {color}; color: white; padding: 0.5rem;
                        border-radius: 5px; margin: 0.3rem 0;">
                <strong>{tier}</strong><br/>
                <small>{score_range} points</small>
            </div>
            """, unsafe_allow_html=True)

    # Display results
    if st.session_state.reputation:
        st.markdown("---")
        st.markdown("### 📊 Your Reputation Report")

        tier = st.session_state.reputation["tier"]
        score = st.session_state.reputation["total_score"]

        # Score display
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Reputation Score", f"{score:.1f}/100")

        with col2:
            st.metric("Tier", tier.upper())

        with col3:
            st.metric("Badges Earned", len(st.session_state.reputation["badges"]))

        with col4:
            st.metric("Transactions", st.session_state.analysis["transaction_count"])

        # Progress bar
        st.progress(score / 100)

        # Breakdown
        st.markdown("### 📈 Score Breakdown")

        breakdown = st.session_state.reputation["score_breakdown"]
        breakdown_df = pd.DataFrame([
            {"Category": k.replace("_", " ").title(), "Score": v}
            for k, v in breakdown.items()
        ]).sort_values("Score", ascending=False)

        st.bar_chart(breakdown_df.set_index("Category"))

        # Badges
        if st.session_state.reputation["badges"]:
            st.markdown("### 🏆 Achievement Badges")

            badge_html = " ".join([
                f'<span class="badge-item">{badge}</span>'
                for badge in st.session_state.reputation["badges"]
            ])
            st.markdown(badge_html, unsafe_allow_html=True)

        # Badge preview
        if st.session_state.badge_path:
            st.markdown("### 🎨 Your NFT Badge")
            st.image(st.session_state.badge_path, width=400)

            # Download button
            with open(st.session_state.badge_path, "rb") as f:
                st.download_button(
                    "⬇️ Download Badge",
                    f,
                    file_name=f"reputation_badge_{wallet_address[:8]}.png",
                    mime="image/png"
                )

        # Export option
        st.markdown("### 📤 Export Profile")

        export_data = {
            "address": wallet_address,
            "analysis": st.session_state.analysis,
            "reputation": st.session_state.reputation,
            "export_date": datetime.now().isoformat()
        }

        st.download_button(
            "📥 Export as JSON",
            json.dumps(export_data, indent=2),
            file_name=f"web3_profile_{wallet_address[:8]}.json",
            mime="application/json"
        )

elif "Analysis" in page:
    st.markdown("### 📊 Detailed Analysis")

    if st.session_state.analysis:
        analysis = st.session_state.analysis

        # Wallet info
        st.markdown("#### 💼 Wallet Information")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Balance", f"{analysis['balance']:.4f} ETH")

        with col2:
            st.metric("Wallet Age", f"{analysis['wallet_age_days']} days")

        with col3:
            st.metric("Activity Level", analysis['activity_level'].title())

        # On-chain activity
        st.markdown("#### ⛓️ On-Chain Activity")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("NFTs Owned", analysis['nft_count'])

        with col2:
            st.metric("Token Diversity", analysis['token_diversity'])

        with col3:
            st.metric("DAO Memberships", len(analysis['dao_participations']))

        # DeFi activity
        st.markdown("#### 🏦 DeFi Activity")

        defi = analysis['defi_interactions']
        defi_df = pd.DataFrame([
            {"Protocol": "Uniswap", "Interactions": defi['uniswap_swaps']},
            {"Protocol": "Aave", "Interactions": defi['aave_interactions']},
            {"Protocol": "Total Protocols", "Interactions": defi['total_defi_protocols']}
        ])

        st.dataframe(defi_df, use_container_width=True)

        # DAO participation
        if analysis['dao_participations']:
            st.markdown("#### 🗳️ DAO Participation")

            dao_df = pd.DataFrame(analysis['dao_participations'])
            st.dataframe(dao_df, use_container_width=True)

        # ENS
        if analysis.get('ens_name'):
            st.success(f"✓ ENS Name: {analysis['ens_name']}")

    else:
        st.info("ℹ️ No analysis data available. Analyze a wallet from the Home page.")

elif "Leaderboard" in page:
    st.markdown("### 🏆 Reputation Leaderboard")

    try:
        with open("../data/leaderboard.json", "r") as f:
            leaderboard = json.load(f)

        if leaderboard:
            # Sort by score
            leaderboard_sorted = sorted(leaderboard, key=lambda x: x["score"], reverse=True)

            # Create dataframe
            leaderboard_df = pd.DataFrame([
                {
                    "Rank": idx + 1,
                    "Address": f"{entry['address'][:6]}...{entry['address'][-4:]}",
                    "Score": entry['score'],
                    "Tier": entry['tier'].title(),
                    "Badges": len(entry['badges'])
                }
                for idx, entry in enumerate(leaderboard_sorted[:100])
            ])

            # Display with styling
            st.dataframe(
                leaderboard_df,
                use_container_width=True,
                hide_index=True
            )

            # Stats
            st.markdown("---")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Participants", len(leaderboard))

            with col2:
                avg_score = sum(e["score"] for e in leaderboard) / len(leaderboard)
                st.metric("Average Score", f"{avg_score:.1f}")

            with col3:
                top_score = leaderboard_sorted[0]["score"]
                st.metric("Highest Score", f"{top_score:.1f}")

        else:
            st.info("ℹ️ Leaderboard is empty. Be the first to mint a badge!")

    except FileNotFoundError:
        st.info("ℹ️ Leaderboard not yet created. Start analyzing wallets!")

else:  # About page
    st.markdown("### ℹ️ About Web3 Reputation NFT")

    st.markdown("""
    ## 🌐 What is Web3 Reputation NFT?

    Web3 Reputation NFT is a decentralized application that analyzes your on-chain activity
    and generates a personalized NFT badge representing your Web3 reputation.

    ### 🎯 Features

    - **Wallet Analysis**: Comprehensive scanning of your blockchain activity
    - **Reputation Score**: 0-100 score based on multiple factors
    - **Tier System**: 6-tier classification from Novice to Legendary
    - **Achievement Badges**: Earn special badges for notable accomplishments
    - **NFT Minting**: Generate and mint your personalized reputation badge
    - **IPFS Storage**: Decentralized storage for images and metadata
    - **Leaderboard**: Compete with other users
    - **Profile Export**: Download your profile for DAO/recruitment

    ### 📊 Scoring Criteria

    - **Long-term Holder** (+10): Reward for wallet age and stability
    - **DAO Participation** (+20): Active governance involvement
    - **NFT Mints** (+5): Early adopter and collector
    - **Transaction Volume** (+15): Overall blockchain engagement
    - **Token Diversity** (+10): Diversified portfolio
    - **DeFi Usage** (+15): Protocol interaction
    - **Wallet Age** (+10): Time in ecosystem
    - **ENS Ownership** (+5): ENS domain holder
    - **Balance** (+5): Current holdings
    - **Frequent Swaps** (-5): Penalty for excessive trading

    ### 🏗️ Technology Stack

    - **Backend**: Python, FastAPI
    - **Blockchain**: Ethereum, Optimism, Base (EVM-compatible)
    - **Indexing**: TheGraph, Alchemy SDK
    - **Storage**: IPFS (Pinata)
    - **Smart Contracts**: Solidity (ERC-721)
    - **Frontend**: Streamlit

    ### 🚀 Getting Started

    1. Enter your Ethereum wallet address
    2. Click "Analyze Wallet" to scan your activity
    3. Click "Generate Badge" to create your NFT image
    4. Click "Mint NFT" to upload to IPFS and prepare for minting

    ### 🔗 Resources

    - GitHub: [github.com/reflekt](https://github.com)
    - Documentation: [docs.reflekt.app](https://docs.reflekt.app)
    - Smart Contract: View on Etherscan

    ### 📝 License

    MIT License - Open Source
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>Web3 Reputation NFT | Built with ❤️ by Reflekt Team</p>
    <p>Powered by Ethereum, IPFS, and TheGraph</p>
</div>
""", unsafe_allow_html=True)

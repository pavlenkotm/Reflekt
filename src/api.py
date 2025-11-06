"""
FastAPI Backend for Web3 Reputation NFT
Provides REST API for wallet analysis, reputation calculation, and NFT minting
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import os
from datetime import datetime
import json

from wallet_scanner import WalletScanner
from reputation_score import ReputationCalculator
from badge_generator import BadgeGenerator, IPFSUploader

# Initialize FastAPI app
app = FastAPI(
    title="Web3 Reputation NFT API",
    description="API for analyzing Web3 reputation and generating NFT badges",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
scanner = WalletScanner()
calculator = ReputationCalculator()
generator = BadgeGenerator()
uploader = IPFSUploader()

# In-memory storage (in production, use a database)
analysis_cache = {}
leaderboard_data = []


# Pydantic models
class WalletAnalysisRequest(BaseModel):
    address: str = Field(..., description="Ethereum wallet address to analyze")


class WalletAnalysisResponse(BaseModel):
    address: str
    transaction_count: int
    balance: float
    wallet_age_days: int
    activity_level: str
    nft_count: int
    dao_participations: List[Dict]
    token_diversity: int
    ens_name: Optional[str]
    defi_interactions: Dict
    timestamp: str


class ReputationResponse(BaseModel):
    total_score: float
    score_breakdown: Dict
    tier: str
    badges: List[str]
    calculated_at: str
    address: str


class MintNFTRequest(BaseModel):
    address: str = Field(..., description="Address to mint NFT for")


class MintNFTResponse(BaseModel):
    success: bool
    message: str
    image_ipfs_hash: Optional[str] = None
    metadata_ipfs_hash: Optional[str] = None
    token_uri: Optional[str] = None


class LeaderboardEntry(BaseModel):
    rank: int
    address: str
    score: float
    tier: str
    badges: List[str]


# API Routes

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Web3 Reputation NFT API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "analyze": "/api/analyze",
            "reputation": "/api/reputation",
            "mint": "/api/mint",
            "leaderboard": "/api/leaderboard",
            "export": "/api/export"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/analyze", response_model=WalletAnalysisResponse)
async def analyze_wallet(request: WalletAnalysisRequest):
    """
    Analyze a wallet address
    Returns comprehensive wallet metrics
    """
    try:
        # Validate address
        if not scanner.is_valid_address(request.address):
            raise HTTPException(status_code=400, detail="Invalid Ethereum address")

        # Check cache (simple caching for 5 minutes)
        cache_key = request.address.lower()
        if cache_key in analysis_cache:
            cached = analysis_cache[cache_key]
            cached_time = datetime.fromisoformat(cached["timestamp"])
            if (datetime.now() - cached_time).seconds < 300:  # 5 minutes
                return cached

        # Analyze wallet
        analysis = scanner.analyze_wallet(request.address)

        # Cache result
        analysis_cache[cache_key] = analysis

        return analysis

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/reputation", response_model=ReputationResponse)
async def calculate_reputation(request: WalletAnalysisRequest):
    """
    Calculate reputation score for a wallet
    Returns score, tier, and badges
    """
    try:
        # First analyze wallet
        if not scanner.is_valid_address(request.address):
            raise HTTPException(status_code=400, detail="Invalid Ethereum address")

        analysis = scanner.analyze_wallet(request.address)

        # Calculate reputation
        reputation = calculator.calculate_score(analysis)

        return reputation

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reputation calculation failed: {str(e)}")


@app.post("/api/mint", response_model=MintNFTResponse)
async def mint_nft(request: MintNFTRequest, background_tasks: BackgroundTasks):
    """
    Generate and mint NFT badge
    Returns IPFS hashes for image and metadata
    """
    try:
        # Validate address
        if not scanner.is_valid_address(request.address):
            raise HTTPException(status_code=400, detail="Invalid Ethereum address")

        # Analyze wallet
        print(f"Analyzing wallet: {request.address}")
        analysis = scanner.analyze_wallet(request.address)

        # Calculate reputation
        print("Calculating reputation...")
        reputation = calculator.calculate_score(analysis)

        # Generate badge image
        print("Generating badge image...")
        badge_path = generator.generate_badge(reputation, analysis)

        # Upload to IPFS
        print("Uploading to IPFS...")
        image_hash = uploader.upload_image(
            badge_path,
            f"reputation_badge_{request.address}"
        )

        if not image_hash:
            return MintNFTResponse(
                success=False,
                message="Failed to upload image to IPFS. Please configure PINATA credentials."
            )

        # Create and upload metadata
        metadata = uploader.create_nft_metadata(reputation, image_hash, analysis)
        metadata_hash = uploader.upload_metadata(
            metadata,
            f"metadata_{request.address}"
        )

        if not metadata_hash:
            return MintNFTResponse(
                success=False,
                message="Failed to upload metadata to IPFS"
            )

        # Update leaderboard in background
        background_tasks.add_task(update_leaderboard, request.address, reputation)

        return MintNFTResponse(
            success=True,
            message="NFT badge created successfully!",
            image_ipfs_hash=image_hash,
            metadata_ipfs_hash=metadata_hash,
            token_uri=f"ipfs://{metadata_hash}"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Minting failed: {str(e)}")


@app.get("/api/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(limit: int = 100):
    """
    Get reputation leaderboard
    Returns top addresses by reputation score
    """
    try:
        # Sort by score descending
        sorted_leaderboard = sorted(
            leaderboard_data,
            key=lambda x: x["score"],
            reverse=True
        )[:limit]

        # Add ranks
        result = []
        for idx, entry in enumerate(sorted_leaderboard, 1):
            result.append(LeaderboardEntry(
                rank=idx,
                address=entry["address"],
                score=entry["score"],
                tier=entry["tier"],
                badges=entry["badges"]
            ))

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch leaderboard: {str(e)}")


@app.post("/api/export")
async def export_profile(request: WalletAnalysisRequest):
    """
    Export wallet profile as JSON
    Useful for DAO/recruitment purposes
    """
    try:
        # Validate address
        if not scanner.is_valid_address(request.address):
            raise HTTPException(status_code=400, detail="Invalid Ethereum address")

        # Get full analysis
        analysis = scanner.analyze_wallet(request.address)
        reputation = calculator.calculate_score(analysis)

        # Create export data
        export_data = {
            "wallet_address": request.address,
            "analysis": analysis,
            "reputation": reputation,
            "export_date": datetime.now().isoformat(),
            "profile_summary": {
                "tier": reputation["tier"],
                "score": reputation["total_score"],
                "badges": reputation["badges"],
                "activity_level": analysis["activity_level"],
                "dao_participation": len(analysis["dao_participations"]),
                "transaction_count": analysis["transaction_count"]
            }
        }

        return export_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@app.get("/api/tiers")
async def get_tiers():
    """Get information about reputation tiers"""
    return {
        "tiers": [
            {
                "name": "legendary",
                "min_score": 90,
                "description": calculator.get_tier_description("legendary")
            },
            {
                "name": "epic",
                "min_score": 75,
                "description": calculator.get_tier_description("epic")
            },
            {
                "name": "rare",
                "min_score": 60,
                "description": calculator.get_tier_description("rare")
            },
            {
                "name": "uncommon",
                "min_score": 40,
                "description": calculator.get_tier_description("uncommon")
            },
            {
                "name": "common",
                "min_score": 20,
                "description": calculator.get_tier_description("common")
            },
            {
                "name": "novice",
                "min_score": 0,
                "description": calculator.get_tier_description("novice")
            }
        ]
    }


# Helper functions

def update_leaderboard(address: str, reputation: Dict):
    """Update leaderboard with new entry"""
    global leaderboard_data

    # Remove existing entry for this address
    leaderboard_data = [
        entry for entry in leaderboard_data
        if entry["address"].lower() != address.lower()
    ]

    # Add new entry
    leaderboard_data.append({
        "address": address,
        "score": reputation["total_score"],
        "tier": reputation["tier"],
        "badges": reputation["badges"],
        "updated_at": datetime.now().isoformat()
    })

    # Keep only top 1000
    leaderboard_data = sorted(
        leaderboard_data,
        key=lambda x: x["score"],
        reverse=True
    )[:1000]

    # Save to file
    try:
        os.makedirs("./data", exist_ok=True)
        with open("./data/leaderboard.json", "w") as f:
            json.dump(leaderboard_data, f, indent=2)
    except Exception as e:
        print(f"Failed to save leaderboard: {e}")


# Load leaderboard on startup
@app.on_event("startup")
async def load_leaderboard():
    """Load leaderboard from file on startup"""
    global leaderboard_data

    try:
        if os.path.exists("./data/leaderboard.json"):
            with open("./data/leaderboard.json", "r") as f:
                leaderboard_data = json.load(f)
            print(f"✓ Loaded {len(leaderboard_data)} leaderboard entries")
    except Exception as e:
        print(f"Failed to load leaderboard: {e}")
        leaderboard_data = []


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))

    print(f"\n🚀 Starting Web3 Reputation NFT API")
    print(f"📍 Server: http://{host}:{port}")
    print(f"📖 Docs: http://{host}:{port}/docs")
    print(f"🔄 Interactive API: http://{host}:{port}/redoc\n")

    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=True
    )

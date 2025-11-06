"""
Badge Generator Module
Generates personalized NFT badge images and uploads to IPFS
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import Dict, Optional, Tuple
import io
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class BadgeGenerator:
    """Generates NFT badge images based on reputation data"""

    # Color schemes for different tiers
    TIER_COLORS = {
        "legendary": {
            "bg": "#1a0033",
            "primary": "#FFD700",
            "secondary": "#FF6B35",
            "accent": "#9D4EDD"
        },
        "epic": {
            "bg": "#1a1a2e",
            "primary": "#A020F0",
            "secondary": "#00D9FF",
            "accent": "#FF2E63"
        },
        "rare": {
            "bg": "#0f1419",
            "primary": "#00B4D8",
            "secondary": "#90E0EF",
            "accent": "#48CAE4"
        },
        "uncommon": {
            "bg": "#1a1a1a",
            "primary": "#06FFA5",
            "secondary": "#2EC4B6",
            "accent": "#20A4F3"
        },
        "common": {
            "bg": "#161616",
            "primary": "#4ECDC4",
            "secondary": "#44A1A0",
            "accent": "#247BA0"
        },
        "novice": {
            "bg": "#0d1117",
            "primary": "#58A6FF",
            "secondary": "#79C0FF",
            "accent": "#1F6FEB"
        }
    }

    def __init__(self, output_dir: str = "./data/badges"):
        """Initialize badge generator"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Badge dimensions
        self.width = 1000
        self.height = 1000

    def generate_badge(
        self,
        reputation: Dict,
        wallet_analysis: Dict,
        output_filename: Optional[str] = None
    ) -> str:
        """
        Generate NFT badge image

        Args:
            reputation: Reputation data from ReputationCalculator
            wallet_analysis: Wallet analysis data
            output_filename: Optional custom filename

        Returns:
            Path to generated image
        """
        # Create new image
        img = Image.new('RGB', (self.width, self.height), 'white')
        draw = ImageDraw.Draw(img)

        tier = reputation.get("tier", "novice")
        score = reputation.get("total_score", 0)
        badges = reputation.get("badges", [])
        address = reputation.get("address", "Unknown")

        # Get color scheme
        colors = self.TIER_COLORS.get(tier, self.TIER_COLORS["novice"])

        # Draw background
        self._draw_background(draw, colors)

        # Draw decorative elements
        self._draw_decorations(draw, colors, tier)

        # Draw main content
        self._draw_header(draw, tier, colors)
        self._draw_score(draw, score, colors)
        self._draw_address(draw, address, colors)
        self._draw_badges(draw, badges, colors)
        self._draw_stats(draw, reputation, colors)
        self._draw_footer(draw, colors)

        # Add glow effect for higher tiers
        if tier in ["legendary", "epic"]:
            img = self._add_glow_effect(img)

        # Save image
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"badge_{address[:8]}_{timestamp}.png"

        output_path = os.path.join(self.output_dir, output_filename)
        img.save(output_path, 'PNG', quality=95)

        return output_path

    def _draw_background(self, draw: ImageDraw, colors: Dict):
        """Draw gradient background"""
        # Simple gradient from top to bottom
        bg_color = colors["bg"]
        draw.rectangle([(0, 0), (self.width, self.height)], fill=bg_color)

        # Add subtle gradient effect
        for y in range(0, self.height, 10):
            alpha = int(255 * (y / self.height) * 0.3)
            color = self._hex_to_rgb(colors["primary"], alpha=alpha)
            draw.rectangle(
                [(0, y), (self.width, y + 10)],
                fill=color
            )

    def _draw_decorations(self, draw: ImageDraw, colors: Dict, tier: str):
        """Draw decorative elements based on tier"""
        # Corner decorations
        corner_color = colors["accent"]

        # Top corners
        draw.rectangle([(0, 0), (100, 5)], fill=corner_color)
        draw.rectangle([(self.width - 100, 0), (self.width, 5)], fill=corner_color)

        # Bottom corners
        draw.rectangle([(0, self.height - 5), (100, self.height)], fill=corner_color)
        draw.rectangle([(self.width - 100, self.height - 5), (self.width, self.height)], fill=corner_color)

        # Side decorations
        if tier in ["legendary", "epic", "rare"]:
            # Draw hexagon pattern
            for i in range(5):
                y = 200 + i * 150
                self._draw_hexagon(draw, (100, y), 30, colors["secondary"], alpha=30)
                self._draw_hexagon(draw, (self.width - 100, y), 30, colors["secondary"], alpha=30)

    def _draw_hexagon(self, draw: ImageDraw, center: Tuple[int, int], size: int, color: str, alpha: int = 255):
        """Draw a hexagon"""
        x, y = center
        points = []
        for i in range(6):
            angle = i * 60
            import math
            px = x + size * math.cos(math.radians(angle))
            py = y + size * math.sin(math.radians(angle))
            points.append((px, py))

        draw.polygon(points, outline=self._hex_to_rgb(color, alpha))

    def _draw_header(self, draw: ImageDraw, tier: str, colors: Dict):
        """Draw header with tier name"""
        # Tier title
        tier_text = f"⬢ {tier.upper()} ⬢"
        font_size = 60

        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # Get text size and center it
        bbox = draw.textbbox((0, 0), tier_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        y = 80

        # Draw text with shadow
        shadow_offset = 3
        draw.text((x + shadow_offset, y + shadow_offset), tier_text, fill="#000000", font=font)
        draw.text((x, y), tier_text, fill=colors["primary"], font=font)

    def _draw_score(self, draw: ImageDraw, score: float, colors: Dict):
        """Draw reputation score"""
        score_text = f"{int(score)}"
        label_text = "REPUTATION SCORE"

        try:
            score_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
            label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            score_font = ImageFont.load_default()
            label_font = ImageFont.load_default()

        # Score number
        bbox = draw.textbbox((0, 0), score_text, font=score_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        y = 200

        draw.text((x, y), score_text, fill=colors["primary"], font=score_font)

        # Label
        bbox = draw.textbbox((0, 0), label_text, font=label_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        y = 340

        draw.text((x, y), label_text, fill=colors["secondary"], font=label_font)

        # Score bar
        bar_width = 600
        bar_height = 30
        bar_x = (self.width - bar_width) // 2
        bar_y = 380

        # Background bar
        draw.rectangle(
            [(bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height)],
            fill="#222222",
            outline=colors["accent"]
        )

        # Fill bar based on score
        fill_width = int((score / 100) * bar_width)
        draw.rectangle(
            [(bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height)],
            fill=colors["primary"]
        )

    def _draw_address(self, draw: ImageDraw, address: str, colors: Dict):
        """Draw wallet address"""
        # Shorten address
        short_address = f"{address[:6]}...{address[-4:]}"

        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 28)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), short_address, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        y = 450

        draw.text((x, y), short_address, fill=colors["secondary"], font=font)

    def _draw_badges(self, draw: ImageDraw, badges: list, colors: Dict):
        """Draw achievement badges"""
        if not badges:
            return

        y_start = 520
        badge_text = "🏆 ACHIEVEMENTS"

        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
            badge_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            title_font = ImageFont.load_default()
            badge_font = ImageFont.load_default()

        # Title
        bbox = draw.textbbox((0, 0), badge_text, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, y_start), badge_text, fill=colors["accent"], font=title_font)

        # Draw badges (max 6)
        display_badges = badges[:6]
        y = y_start + 40

        for badge in display_badges:
            badge_display = f"• {badge}"
            bbox = draw.textbbox((0, 0), badge_display, font=badge_font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2

            draw.text((x, y), badge_display, fill=colors["secondary"], font=badge_font)
            y += 30

    def _draw_stats(self, draw: ImageDraw, reputation: Dict, colors: Dict):
        """Draw key statistics"""
        y_start = 750
        breakdown = reputation.get("score_breakdown", {})

        # Select top 3 scores
        top_scores = sorted(
            [(k, v) for k, v in breakdown.items() if v > 0],
            key=lambda x: x[1],
            reverse=True
        )[:3]

        if not top_scores:
            return

        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            font = ImageFont.load_default()

        y = y_start
        for category, score in top_scores:
            stat_text = f"{category.replace('_', ' ').title()}: +{score}"
            bbox = draw.textbbox((0, 0), stat_text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2

            draw.text((x, y), stat_text, fill=colors["secondary"], font=font)
            y += 25

    def _draw_footer(self, draw: ImageDraw, colors: Dict):
        """Draw footer"""
        footer_text = "Web3 Reputation NFT • Reflekt"
        timestamp = datetime.now().strftime("%Y-%m-%d")

        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        except:
            font = ImageFont.load_default()

        # Footer text
        bbox = draw.textbbox((0, 0), footer_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        y = 920

        draw.text((x, y), footer_text, fill=colors["secondary"], font=font)

        # Timestamp
        bbox = draw.textbbox((0, 0), timestamp, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        y = 945

        draw.text((x, y), timestamp, fill=colors["accent"], font=font)

    def _add_glow_effect(self, img: Image) -> Image:
        """Add glow effect for legendary/epic tiers"""
        # Apply subtle blur for glow
        blurred = img.filter(ImageFilter.GaussianBlur(2))
        return Image.blend(img, blurred, 0.3)

    def _hex_to_rgb(self, hex_color: str, alpha: int = 255) -> Tuple[int, int, int, int]:
        """Convert hex color to RGBA tuple"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (r, g, b, alpha)


class IPFSUploader:
    """Uploads badge images and metadata to IPFS via Pinata"""

    def __init__(self):
        """Initialize IPFS uploader"""
        self.pinata_api_key = os.getenv("PINATA_API_KEY")
        self.pinata_secret_key = os.getenv("PINATA_SECRET_KEY")
        self.pinata_jwt = os.getenv("PINATA_JWT")

        self.pinata_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        self.json_url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    def upload_image(self, image_path: str, name: str) -> Optional[str]:
        """
        Upload image to IPFS

        Returns:
            IPFS hash or None if failed
        """
        if not self.pinata_jwt:
            print("Warning: PINATA_JWT not set. Skipping IPFS upload.")
            return None

        try:
            with open(image_path, 'rb') as file:
                files = {'file': file}

                headers = {
                    'Authorization': f'Bearer {self.pinata_jwt}'
                }

                data = {
                    'pinataMetadata': json.dumps({'name': name})
                }

                response = requests.post(
                    self.pinata_url,
                    files=files,
                    data=data,
                    headers=headers
                )

                if response.status_code == 200:
                    result = response.json()
                    ipfs_hash = result['IpfsHash']
                    print(f"Image uploaded to IPFS: {ipfs_hash}")
                    return ipfs_hash
                else:
                    print(f"Upload failed: {response.text}")
                    return None

        except Exception as e:
            print(f"Error uploading to IPFS: {e}")
            return None

    def upload_metadata(self, metadata: Dict, name: str) -> Optional[str]:
        """
        Upload NFT metadata to IPFS

        Returns:
            IPFS hash or None if failed
        """
        if not self.pinata_jwt:
            print("Warning: PINATA_JWT not set. Skipping IPFS upload.")
            return None

        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.pinata_jwt}'
            }

            data = {
                'pinataContent': metadata,
                'pinataMetadata': {'name': name}
            }

            response = requests.post(
                self.json_url,
                json=data,
                headers=headers
            )

            if response.status_code == 200:
                result = response.json()
                ipfs_hash = result['IpfsHash']
                print(f"Metadata uploaded to IPFS: {ipfs_hash}")
                return ipfs_hash
            else:
                print(f"Upload failed: {response.text}")
                return None

        except Exception as e:
            print(f"Error uploading metadata to IPFS: {e}")
            return None

    def create_nft_metadata(
        self,
        reputation: Dict,
        image_ipfs_hash: str,
        wallet_analysis: Dict
    ) -> Dict:
        """Create NFT metadata following OpenSea standard"""
        tier = reputation.get("tier", "novice")
        score = reputation.get("total_score", 0)
        badges = reputation.get("badges", [])

        metadata = {
            "name": f"Web3 Reputation Badge - {tier.title()}",
            "description": f"This NFT represents the Web3 reputation for address {reputation.get('address', 'Unknown')}. "
                          f"Score: {score}/100. Tier: {tier.title()}.",
            "image": f"ipfs://{image_ipfs_hash}",
            "external_url": "https://reflekt.app",
            "attributes": [
                {
                    "trait_type": "Reputation Score",
                    "value": score
                },
                {
                    "trait_type": "Tier",
                    "value": tier.title()
                },
                {
                    "trait_type": "Transaction Count",
                    "value": wallet_analysis.get("transaction_count", 0)
                },
                {
                    "trait_type": "Wallet Age (days)",
                    "value": wallet_analysis.get("wallet_age_days", 0)
                },
                {
                    "trait_type": "DAO Participations",
                    "value": len(wallet_analysis.get("dao_participations", []))
                },
                {
                    "trait_type": "NFT Count",
                    "value": wallet_analysis.get("nft_count", 0)
                },
                {
                    "trait_type": "Token Diversity",
                    "value": wallet_analysis.get("token_diversity", 0)
                }
            ]
        }

        # Add badges as properties
        for badge in badges:
            metadata["attributes"].append({
                "trait_type": "Achievement",
                "value": badge
            })

        return metadata


if __name__ == "__main__":
    # Example usage
    from wallet_scanner import WalletScanner
    from reputation_score import ReputationCalculator

    scanner = WalletScanner()
    calculator = ReputationCalculator()
    generator = BadgeGenerator()
    uploader = IPFSUploader()

    # Example address
    test_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

    try:
        print(f"Generating badge for: {test_address}\n")

        # Analyze wallet
        analysis = scanner.analyze_wallet(test_address)

        # Calculate reputation
        reputation = calculator.calculate_score(analysis)

        # Generate badge
        badge_path = generator.generate_badge(reputation, analysis)
        print(f"\n✓ Badge generated: {badge_path}")

        # Upload to IPFS (if credentials configured)
        image_hash = uploader.upload_image(badge_path, f"reputation_badge_{test_address}")

        if image_hash:
            # Create and upload metadata
            metadata = uploader.create_nft_metadata(reputation, image_hash, analysis)
            metadata_hash = uploader.upload_metadata(metadata, f"metadata_{test_address}")

            if metadata_hash:
                print(f"\n✓ NFT Ready!")
                print(f"Image IPFS: ipfs://{image_hash}")
                print(f"Metadata IPFS: ipfs://{metadata_hash}")

    except Exception as e:
        print(f"Error: {e}")

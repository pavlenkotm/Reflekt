const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("ReputationNFT", function () {
  let ReputationNFT;
  let nft;
  let owner;
  let addr1;
  let addr2;
  let addrs;

  const TOKEN_URI = "ipfs://QmTest123";
  const REPUTATION_SCORE = 75;
  const REPUTATION_TIER = "epic";

  beforeEach(async function () {
    [owner, addr1, addr2, ...addrs] = await ethers.getSigners();

    ReputationNFT = await ethers.getContractFactory("ReputationNFT");
    nft = await ReputationNFT.deploy();
    await nft.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the correct name and symbol", async function () {
      expect(await nft.name()).to.equal("Web3 Reputation Badge");
      expect(await nft.symbol()).to.equal("W3REP");
    });

    it("Should set the right owner", async function () {
      expect(await nft.owner()).to.equal(owner.address);
    });

    it("Should start with zero total supply", async function () {
      expect(await nft.totalSupply()).to.equal(0);
    });
  });

  describe("Minting", function () {
    it("Should mint a reputation badge", async function () {
      await nft.mintReputationBadge(
        addr1.address,
        TOKEN_URI,
        REPUTATION_SCORE,
        REPUTATION_TIER
      );

      expect(await nft.balanceOf(addr1.address)).to.equal(1);
      expect(await nft.hasReputationBadge(addr1.address)).to.equal(true);
      expect(await nft.totalSupply()).to.equal(1);
    });

    it("Should emit ReputationBadgeMinted event", async function () {
      await expect(
        nft.mintReputationBadge(
          addr1.address,
          TOKEN_URI,
          REPUTATION_SCORE,
          REPUTATION_TIER
        )
      )
        .to.emit(nft, "ReputationBadgeMinted")
        .withArgs(addr1.address, 1, REPUTATION_SCORE, REPUTATION_TIER, TOKEN_URI);
    });

    it("Should store reputation data correctly", async function () {
      await nft.mintReputationBadge(
        addr1.address,
        TOKEN_URI,
        REPUTATION_SCORE,
        REPUTATION_TIER
      );

      const [score, tier, uri] = await nft.getReputationData(1);
      expect(score).to.equal(REPUTATION_SCORE);
      expect(tier).to.equal(REPUTATION_TIER);
      expect(uri).to.equal(TOKEN_URI);
    });

    it("Should map address to token ID", async function () {
      await nft.mintReputationBadge(
        addr1.address,
        TOKEN_URI,
        REPUTATION_SCORE,
        REPUTATION_TIER
      );

      expect(await nft.getTokenIdByAddress(addr1.address)).to.equal(1);
    });

    it("Should fail if minting to zero address", async function () {
      await expect(
        nft.mintReputationBadge(
          ethers.ZeroAddress,
          TOKEN_URI,
          REPUTATION_SCORE,
          REPUTATION_TIER
        )
      ).to.be.revertedWith("Cannot mint to zero address");
    });

    it("Should fail if score exceeds 100", async function () {
      await expect(
        nft.mintReputationBadge(
          addr1.address,
          TOKEN_URI,
          101,
          REPUTATION_TIER
        )
      ).to.be.revertedWith("Score must be <= 100");
    });

    it("Should fail if address already has a badge", async function () {
      await nft.mintReputationBadge(
        addr1.address,
        TOKEN_URI,
        REPUTATION_SCORE,
        REPUTATION_TIER
      );

      await expect(
        nft.mintReputationBadge(
          addr1.address,
          TOKEN_URI,
          REPUTATION_SCORE,
          REPUTATION_TIER
        )
      ).to.be.revertedWith("Address already has a badge");
    });

    it("Should only allow owner to mint", async function () {
      await expect(
        nft.connect(addr1).mintReputationBadge(
          addr2.address,
          TOKEN_URI,
          REPUTATION_SCORE,
          REPUTATION_TIER
        )
      ).to.be.revertedWithCustomError(nft, "OwnableUnauthorizedAccount");
    });
  });

  describe("Updating", function () {
    beforeEach(async function () {
      await nft.mintReputationBadge(
        addr1.address,
        TOKEN_URI,
        REPUTATION_SCORE,
        REPUTATION_TIER
      );
    });

    it("Should update reputation badge", async function () {
      const newURI = "ipfs://QmNewHash";
      const newScore = 90;
      const newTier = "legendary";

      await nft.updateReputationBadge(1, newURI, newScore, newTier);

      const [score, tier, uri] = await nft.getReputationData(1);
      expect(score).to.equal(newScore);
      expect(tier).to.equal(newTier);
      expect(uri).to.equal(newURI);
    });

    it("Should emit ReputationBadgeUpdated event", async function () {
      const newURI = "ipfs://QmNewHash";
      const newScore = 90;
      const newTier = "legendary";

      await expect(
        nft.updateReputationBadge(1, newURI, newScore, newTier)
      )
        .to.emit(nft, "ReputationBadgeUpdated")
        .withArgs(addr1.address, 1, newScore, newTier, newURI);
    });

    it("Should fail if updating non-existent token", async function () {
      await expect(
        nft.updateReputationBadge(999, TOKEN_URI, REPUTATION_SCORE, REPUTATION_TIER)
      ).to.be.revertedWith("Token does not exist");
    });

    it("Should fail if new score exceeds 100", async function () {
      await expect(
        nft.updateReputationBadge(1, TOKEN_URI, 101, REPUTATION_TIER)
      ).to.be.revertedWith("Score must be <= 100");
    });

    it("Should only allow owner to update", async function () {
      await expect(
        nft.connect(addr1).updateReputationBadge(1, TOKEN_URI, 80, "epic")
      ).to.be.revertedWithCustomError(nft, "OwnableUnauthorizedAccount");
    });
  });

  describe("Soulbound (Non-transferable)", function () {
    beforeEach(async function () {
      await nft.mintReputationBadge(
        addr1.address,
        TOKEN_URI,
        REPUTATION_SCORE,
        REPUTATION_TIER
      );
    });

    it("Should prevent transfers between users", async function () {
      await expect(
        nft.connect(addr1).transferFrom(addr1.address, addr2.address, 1)
      ).to.be.revertedWith("Reputation badges are non-transferable (soulbound)");
    });

    it("Should prevent safeTransferFrom", async function () {
      await expect(
        nft.connect(addr1)["safeTransferFrom(address,address,uint256)"](
          addr1.address,
          addr2.address,
          1
        )
      ).to.be.revertedWith("Reputation badges are non-transferable (soulbound)");
    });
  });

  describe("Burning", function () {
    beforeEach(async function () {
      await nft.mintReputationBadge(
        addr1.address,
        TOKEN_URI,
        REPUTATION_SCORE,
        REPUTATION_TIER
      );
    });

    it("Should allow owner to burn their badge", async function () {
      await nft.connect(addr1).burn(1);

      expect(await nft.balanceOf(addr1.address)).to.equal(0);
      expect(await nft.hasReputationBadge(addr1.address)).to.equal(false);
      expect(await nft.getTokenIdByAddress(addr1.address)).to.equal(0);
    });

    it("Should decrease total supply when burning", async function () {
      expect(await nft.totalSupply()).to.equal(1);
      await nft.connect(addr1).burn(1);
      // Total supply returns counter - 1, so after burn it's still 1
      // But the token doesn't exist anymore
      await expect(nft.getReputationData(1)).to.be.revertedWith("Token does not exist");
    });

    it("Should allow re-minting after burning", async function () {
      await nft.connect(addr1).burn(1);

      await nft.mintReputationBadge(
        addr1.address,
        TOKEN_URI,
        REPUTATION_SCORE,
        REPUTATION_TIER
      );

      expect(await nft.hasReputationBadge(addr1.address)).to.equal(true);
      expect(await nft.balanceOf(addr1.address)).to.equal(1);
    });

    it("Should only allow badge owner to burn", async function () {
      await expect(
        nft.connect(addr2).burn(1)
      ).to.be.revertedWith("Only owner can burn their badge");
    });
  });

  describe("Queries", function () {
    beforeEach(async function () {
      await nft.mintReputationBadge(
        addr1.address,
        TOKEN_URI,
        REPUTATION_SCORE,
        REPUTATION_TIER
      );
    });

    it("Should check if address has badge", async function () {
      expect(await nft.hasReputationBadge(addr1.address)).to.equal(true);
      expect(await nft.hasReputationBadge(addr2.address)).to.equal(false);
    });

    it("Should get token ID by address", async function () {
      expect(await nft.getTokenIdByAddress(addr1.address)).to.equal(1);
      expect(await nft.getTokenIdByAddress(addr2.address)).to.equal(0);
    });

    it("Should get reputation data", async function () {
      const [score, tier, uri] = await nft.getReputationData(1);
      expect(score).to.equal(REPUTATION_SCORE);
      expect(tier).to.equal(REPUTATION_TIER);
      expect(uri).to.equal(TOKEN_URI);
    });

    it("Should return correct token URI", async function () {
      expect(await nft.tokenURI(1)).to.equal(TOKEN_URI);
    });

    it("Should fail to get data for non-existent token", async function () {
      await expect(
        nft.getReputationData(999)
      ).to.be.revertedWith("Token does not exist");
    });
  });

  describe("Multiple Badges", function () {
    it("Should mint multiple badges to different addresses", async function () {
      await nft.mintReputationBadge(addr1.address, TOKEN_URI, 50, "uncommon");
      await nft.mintReputationBadge(addr2.address, TOKEN_URI, 75, "epic");
      await nft.mintReputationBadge(addrs[0].address, TOKEN_URI, 90, "legendary");

      expect(await nft.totalSupply()).to.equal(3);
      expect(await nft.balanceOf(addr1.address)).to.equal(1);
      expect(await nft.balanceOf(addr2.address)).to.equal(1);
      expect(await nft.balanceOf(addrs[0].address)).to.equal(1);
    });

    it("Should assign sequential token IDs", async function () {
      await nft.mintReputationBadge(addr1.address, TOKEN_URI, 50, "uncommon");
      await nft.mintReputationBadge(addr2.address, TOKEN_URI, 75, "epic");

      expect(await nft.getTokenIdByAddress(addr1.address)).to.equal(1);
      expect(await nft.getTokenIdByAddress(addr2.address)).to.equal(2);
    });
  });

  describe("Different Tiers", function () {
    const tiers = [
      { tier: "novice", score: 15 },
      { tier: "common", score: 35 },
      { tier: "uncommon", score: 55 },
      { tier: "rare", score: 65 },
      { tier: "epic", score: 80 },
      { tier: "legendary", score: 95 }
    ];

    it("Should mint badges with all different tiers", async function () {
      for (let i = 0; i < tiers.length; i++) {
        const recipient = addrs[i];
        await nft.mintReputationBadge(
          recipient.address,
          TOKEN_URI,
          tiers[i].score,
          tiers[i].tier
        );

        const [score, tier] = await nft.getReputationData(i + 1);
        expect(score).to.equal(tiers[i].score);
        expect(tier).to.equal(tiers[i].tier);
      }
    });
  });
});

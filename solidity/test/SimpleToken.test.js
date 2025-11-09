const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SimpleToken", function () {
  let SimpleToken;
  let token;
  let owner;
  let addr1;
  let addr2;
  let addrs;

  const TOKEN_NAME = "Test Token";
  const TOKEN_SYMBOL = "TEST";
  const INITIAL_SUPPLY = 1000000;
  const DECIMALS = 18;

  beforeEach(async function () {
    // Get signers
    [owner, addr1, addr2, ...addrs] = await ethers.getSigners();

    // Deploy contract
    SimpleToken = await ethers.getContractFactory("SimpleToken");
    token = await SimpleToken.deploy(
      TOKEN_NAME,
      TOKEN_SYMBOL,
      INITIAL_SUPPLY,
      DECIMALS
    );
    await token.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the correct name and symbol", async function () {
      expect(await token.name()).to.equal(TOKEN_NAME);
      expect(await token.symbol()).to.equal(TOKEN_SYMBOL);
    });

    it("Should set the correct decimals", async function () {
      expect(await token.decimals()).to.equal(DECIMALS);
    });

    it("Should assign the total supply to the owner", async function () {
      const ownerBalance = await token.balanceOf(owner.address);
      const expectedBalance = ethers.parseUnits(INITIAL_SUPPLY.toString(), DECIMALS);
      expect(ownerBalance).to.equal(expectedBalance);
    });

    it("Should set the right owner", async function () {
      expect(await token.owner()).to.equal(owner.address);
    });

    it("Should have correct total supply", async function () {
      const totalSupply = await token.totalSupply();
      const expectedSupply = ethers.parseUnits(INITIAL_SUPPLY.toString(), DECIMALS);
      expect(totalSupply).to.equal(expectedSupply);
    });
  });

  describe("Transactions", function () {
    it("Should transfer tokens between accounts", async function () {
      const transferAmount = ethers.parseUnits("50", DECIMALS);

      // Transfer from owner to addr1
      await token.transfer(addr1.address, transferAmount);
      expect(await token.balanceOf(addr1.address)).to.equal(transferAmount);

      // Transfer from addr1 to addr2
      await token.connect(addr1).transfer(addr2.address, transferAmount);
      expect(await token.balanceOf(addr2.address)).to.equal(transferAmount);
      expect(await token.balanceOf(addr1.address)).to.equal(0);
    });

    it("Should fail if sender doesn't have enough tokens", async function () {
      const initialOwnerBalance = await token.balanceOf(owner.address);
      const tooMuchTokens = initialOwnerBalance + 1n;

      await expect(
        token.connect(addr1).transfer(owner.address, tooMuchTokens)
      ).to.be.reverted;
    });

    it("Should update balances after transfers", async function () {
      const initialOwnerBalance = await token.balanceOf(owner.address);
      const transferAmount = ethers.parseUnits("100", DECIMALS);

      await token.transfer(addr1.address, transferAmount);
      await token.transfer(addr2.address, transferAmount);

      const finalOwnerBalance = await token.balanceOf(owner.address);
      expect(finalOwnerBalance).to.equal(initialOwnerBalance - transferAmount * 2n);

      const addr1Balance = await token.balanceOf(addr1.address);
      expect(addr1Balance).to.equal(transferAmount);

      const addr2Balance = await token.balanceOf(addr2.address);
      expect(addr2Balance).to.equal(transferAmount);
    });
  });

  describe("Minting", function () {
    it("Should allow owner to mint new tokens", async function () {
      const mintAmount = ethers.parseUnits("1000", DECIMALS);
      const initialSupply = await token.totalSupply();

      await token.mint(addr1.address, mintAmount);

      expect(await token.balanceOf(addr1.address)).to.equal(mintAmount);
      expect(await token.totalSupply()).to.equal(initialSupply + mintAmount);
    });

    it("Should not allow non-owner to mint tokens", async function () {
      const mintAmount = ethers.parseUnits("1000", DECIMALS);

      await expect(
        token.connect(addr1).mint(addr2.address, mintAmount)
      ).to.be.revertedWithCustomError(token, "OwnableUnauthorizedAccount");
    });

    it("Should emit Transfer event when minting", async function () {
      const mintAmount = ethers.parseUnits("1000", DECIMALS);

      await expect(token.mint(addr1.address, mintAmount))
        .to.emit(token, "Transfer")
        .withArgs(ethers.ZeroAddress, addr1.address, mintAmount);
    });
  });

  describe("Burning", function () {
    it("Should allow users to burn their own tokens", async function () {
      const burnAmount = ethers.parseUnits("1000", DECIMALS);
      const initialBalance = await token.balanceOf(owner.address);
      const initialSupply = await token.totalSupply();

      await token.burn(burnAmount);

      expect(await token.balanceOf(owner.address)).to.equal(initialBalance - burnAmount);
      expect(await token.totalSupply()).to.equal(initialSupply - burnAmount);
    });

    it("Should fail if user tries to burn more than they have", async function () {
      const userBalance = await token.balanceOf(addr1.address);
      const burnAmount = userBalance + ethers.parseUnits("1", DECIMALS);

      await expect(
        token.connect(addr1).burn(burnAmount)
      ).to.be.reverted;
    });

    it("Should emit Transfer event when burning", async function () {
      const burnAmount = ethers.parseUnits("1000", DECIMALS);

      await expect(token.burn(burnAmount))
        .to.emit(token, "Transfer")
        .withArgs(owner.address, ethers.ZeroAddress, burnAmount);
    });
  });

  describe("Allowances", function () {
    it("Should approve tokens for delegated transfer", async function () {
      const approveAmount = ethers.parseUnits("100", DECIMALS);

      await token.approve(addr1.address, approveAmount);
      expect(await token.allowance(owner.address, addr1.address)).to.equal(approveAmount);
    });

    it("Should allow delegated transfers", async function () {
      const approveAmount = ethers.parseUnits("100", DECIMALS);
      const transferAmount = ethers.parseUnits("50", DECIMALS);

      await token.approve(addr1.address, approveAmount);
      await token.connect(addr1).transferFrom(owner.address, addr2.address, transferAmount);

      expect(await token.balanceOf(addr2.address)).to.equal(transferAmount);
      expect(await token.allowance(owner.address, addr1.address)).to.equal(
        approveAmount - transferAmount
      );
    });

    it("Should fail if transfer amount exceeds allowance", async function () {
      const approveAmount = ethers.parseUnits("100", DECIMALS);
      const transferAmount = ethers.parseUnits("150", DECIMALS);

      await token.approve(addr1.address, approveAmount);

      await expect(
        token.connect(addr1).transferFrom(owner.address, addr2.address, transferAmount)
      ).to.be.reverted;
    });
  });

  describe("Edge Cases", function () {
    it("Should handle zero transfers", async function () {
      await expect(token.transfer(addr1.address, 0)).to.not.be.reverted;
      expect(await token.balanceOf(addr1.address)).to.equal(0);
    });

    it("Should handle transfers to self", async function () {
      const transferAmount = ethers.parseUnits("100", DECIMALS);
      const initialBalance = await token.balanceOf(owner.address);

      await token.transfer(owner.address, transferAmount);
      expect(await token.balanceOf(owner.address)).to.equal(initialBalance);
    });

    it("Should prevent transfers to zero address", async function () {
      const transferAmount = ethers.parseUnits("100", DECIMALS);

      await expect(
        token.transfer(ethers.ZeroAddress, transferAmount)
      ).to.be.revertedWithCustomError(token, "ERC20InvalidReceiver");
    });
  });
});

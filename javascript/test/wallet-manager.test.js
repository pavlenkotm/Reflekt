/**
 * Tests for WalletManager
 */

const { expect } = require('chai');
const WalletManager = require('../wallet-manager');

describe('WalletManager', function () {
  let manager;

  before(function () {
    // Use public RPC for tests
    manager = new WalletManager('https://eth.llamarpc.com');
  });

  describe('Initialization', function () {
    it('should create manager instance', function () {
      expect(manager).to.be.instanceOf(WalletManager);
      expect(manager.web3).to.exist;
    });

    it('should connect to Ethereum network', async function () {
      const connected = await manager.isConnected();
      expect(connected).to.be.true;
    });
  });

  describe('Network Operations', function () {
    it('should get network information', async function () {
      const info = await manager.getNetworkInfo();

      expect(info).to.have.property('chainId');
      expect(info).to.have.property('blockNumber');
      expect(info).to.have.property('gasPrice');
      expect(info.chainId).to.be.a('number');
      expect(info.chainId).to.equal(1); // Mainnet
    });

    it('should get block information', async function () {
      const block = await manager.getBlock('latest');

      expect(block).to.have.property('number');
      expect(block).to.have.property('hash');
      expect(block).to.have.property('timestamp');
      expect(block.number).to.be.a('number');
      expect(block.number).to.be.greaterThan(0);
    });

    it('should get specific block by number', async function () {
      const blockNumber = 1;
      const block = await manager.getBlock(blockNumber);

      expect(block.number).to.equal(blockNumber);
    });
  });

  describe('Wallet Operations', function () {
    it('should create new wallet', function () {
      const wallet = manager.createWallet();

      expect(wallet).to.have.property('address');
      expect(wallet).to.have.property('privateKey');
      expect(wallet.address).to.match(/^0x[a-fA-F0-9]{40}$/);
      expect(wallet.privateKey).to.match(/^0x[a-fA-F0-9]{64}$/);
    });

    it('should create unique wallets', function () {
      const wallet1 = manager.createWallet();
      const wallet2 = manager.createWallet();

      expect(wallet1.address).to.not.equal(wallet2.address);
      expect(wallet1.privateKey).to.not.equal(wallet2.privateKey);
    });

    it('should get balance for address', async function () {
      // Vitalik's address
      const address = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045';
      const balance = await manager.getBalance(address);

      expect(balance).to.have.property('address');
      expect(balance).to.have.property('balanceWei');
      expect(balance).to.have.property('balanceEth');
      expect(balance.address).to.equal(address);
    });
  });

  describe('Signing Operations', function () {
    let wallet;
    const message = 'Hello Web3!';

    beforeEach(function () {
      wallet = manager.createWallet();
    });

    it('should sign a message', function () {
      const signature = manager.signMessage(wallet.privateKey, message);

      expect(signature).to.have.property('message');
      expect(signature).to.have.property('signature');
      expect(signature).to.have.property('messageHash');
      expect(signature.signature).to.match(/^0x[a-fA-F0-9]{130}$/);
    });

    it('should recover address from signature', function () {
      const signature = manager.signMessage(wallet.privateKey, message);
      const recovered = manager.recoverAddress(message, signature.signature);

      expect(recovered.toLowerCase()).to.equal(wallet.address.toLowerCase());
    });

    it('should fail to recover wrong message', function () {
      const signature = manager.signMessage(wallet.privateKey, message);
      const recovered = manager.recoverAddress('Wrong message', signature.signature);

      expect(recovered.toLowerCase()).to.not.equal(wallet.address.toLowerCase());
    });

    it('should produce different signatures for different messages', function () {
      const sig1 = manager.signMessage(wallet.privateKey, 'Message 1');
      const sig2 = manager.signMessage(wallet.privateKey, 'Message 2');

      expect(sig1.signature).to.not.equal(sig2.signature);
    });
  });

  describe('Transaction Operations', function () {
    it('should get transaction details', async function () {
      // Known transaction hash
      const txHash = '0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060';

      const tx = await manager.getTransaction(txHash);

      expect(tx).to.have.property('hash');
      expect(tx).to.have.property('from');
      expect(tx).to.have.property('to');
      expect(tx).to.have.property('value');
      expect(tx.hash).to.equal(txHash);
    });
  });

  describe('Utility Functions', function () {
    it('should validate Ethereum addresses', function () {
      expect(manager.isValidAddress('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0')).to.be.true;
      expect(manager.isValidAddress('0x0000000000000000000000000000000000000000')).to.be.true;
      expect(manager.isValidAddress('0x123')).to.be.false;
      expect(manager.isValidAddress('invalid')).to.be.false;
    });

    it('should convert to checksum address', function () {
      const address = '0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed';
      const checksum = manager.toChecksumAddress(address.toLowerCase());

      expect(checksum).to.equal(address);
    });

    it('should hash data with keccak256', function () {
      const data = 'Hello World';
      const hash = manager.keccak256(data);

      expect(hash).to.match(/^0x[a-fA-F0-9]{64}$/);
    });

    it('should produce same hash for same data', function () {
      const data = 'Test';
      const hash1 = manager.keccak256(data);
      const hash2 = manager.keccak256(data);

      expect(hash1).to.equal(hash2);
    });

    it('should convert Wei to Ether', function () {
      const wei = '1000000000000000000';
      const eth = manager.toEther(wei);

      expect(eth).to.equal('1');
    });

    it('should convert Ether to Wei', function () {
      const eth = '1';
      const wei = manager.toWei(eth);

      expect(wei).to.equal('1000000000000000000');
    });

    it('should handle decimal conversions', function () {
      const eth = '0.5';
      const wei = manager.toWei(eth);
      const ethBack = manager.toEther(wei);

      expect(ethBack).to.equal(eth);
    });
  });

  describe('ERC-20 Operations', function () {
    it('should get ERC-20 token balance', async function () {
      // USDT contract
      const tokenAddress = '0xdAC17F958D2ee523a2206206994597C13D831ec7';
      // Random holder
      const holderAddress = '0x5754284f345afc66a98fbB0a0Afe71e0F007B949';

      const balance = await manager.getERC20Balance(tokenAddress, holderAddress);

      expect(balance).to.have.property('tokenAddress');
      expect(balance).to.have.property('holderAddress');
      expect(balance).to.have.property('symbol');
      expect(balance).to.have.property('decimals');
      expect(balance).to.have.property('balance');
      expect(balance.symbol).to.equal('USDT');
    });
  });

  describe('Gas Estimation', function () {
    it('should estimate gas for transaction', async function () {
      const tx = {
        from: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0',
        to: '0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed',
        value: manager.toWei('0.1'),
      };

      const estimate = await manager.estimateGas(tx);

      expect(estimate).to.have.property('gasEstimate');
      expect(estimate).to.have.property('gasPrice');
      expect(estimate).to.have.property('gasCost');
      expect(estimate.gasEstimate).to.be.a('number');
      expect(estimate.gasEstimate).to.be.greaterThan(0);
    });
  });
});

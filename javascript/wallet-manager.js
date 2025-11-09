/**
 * Web3.js Wallet Manager
 * Demonstrates classic JavaScript Web3 patterns
 */

const { Web3 } = require('web3');

class WalletManager {
  /**
   * Initialize wallet manager with RPC endpoint
   * @param {string} rpcUrl - Ethereum RPC endpoint
   */
  constructor(rpcUrl = 'https://eth.llamarpc.com') {
    this.web3 = new Web3(rpcUrl);
  }

  /**
   * Get connection status
   * @returns {Promise<boolean>}
   */
  async isConnected() {
    try {
      await this.web3.eth.getBlockNumber();
      return true;
    } catch (error) {
      return false;
    }
  }

  /**
   * Get current network information
   * @returns {Promise<Object>}
   */
  async getNetworkInfo() {
    const chainId = await this.web3.eth.getChainId();
    const blockNumber = await this.web3.eth.getBlockNumber();
    const gasPrice = await this.web3.eth.getGasPrice();

    return {
      chainId: Number(chainId),
      blockNumber: Number(blockNumber),
      gasPrice: this.web3.utils.fromWei(gasPrice, 'gwei') + ' gwei',
      gasPriceWei: gasPrice.toString(),
    };
  }

  /**
   * Create a new wallet
   * @returns {Object} - Wallet with address and private key
   */
  createWallet() {
    const account = this.web3.eth.accounts.create();
    return {
      address: account.address,
      privateKey: account.privateKey,
      warning: '⚠️  NEVER share your private key!',
    };
  }

  /**
   * Get ETH balance for an address
   * @param {string} address - Ethereum address
   * @returns {Promise<Object>}
   */
  async getBalance(address) {
    const balanceWei = await this.web3.eth.getBalance(address);
    const balanceEth = this.web3.utils.fromWei(balanceWei, 'ether');

    return {
      address,
      balanceWei: balanceWei.toString(),
      balanceEth,
      balanceFormatted: `${balanceEth} ETH`,
    };
  }

  /**
   * Send ETH transaction
   * @param {string} privateKey - Sender's private key
   * @param {string} to - Recipient address
   * @param {string} valueEth - Amount in ETH
   * @returns {Promise<Object>}
   */
  async sendTransaction(privateKey, to, valueEth) {
    const account = this.web3.eth.accounts.privateKeyToAccount(privateKey);
    this.web3.eth.accounts.wallet.add(account);

    const valueWei = this.web3.utils.toWei(valueEth, 'ether');
    const gasPrice = await this.web3.eth.getGasPrice();

    const tx = {
      from: account.address,
      to,
      value: valueWei,
      gas: '21000',
      gasPrice: gasPrice.toString(),
    };

    const receipt = await this.web3.eth.sendTransaction(tx);

    return {
      transactionHash: receipt.transactionHash,
      from: receipt.from,
      to: receipt.to,
      blockNumber: Number(receipt.blockNumber),
      gasUsed: Number(receipt.gasUsed),
      status: receipt.status ? 'success' : 'failed',
    };
  }

  /**
   * Get transaction details
   * @param {string} txHash - Transaction hash
   * @returns {Promise<Object>}
   */
  async getTransaction(txHash) {
    const tx = await this.web3.eth.getTransaction(txHash);
    const receipt = await this.web3.eth.getTransactionReceipt(txHash);

    return {
      hash: tx.hash,
      from: tx.from,
      to: tx.to,
      value: this.web3.utils.fromWei(tx.value, 'ether') + ' ETH',
      valueWei: tx.value.toString(),
      gas: Number(tx.gas),
      gasPrice: this.web3.utils.fromWei(tx.gasPrice, 'gwei') + ' gwei',
      nonce: Number(tx.nonce),
      blockNumber: Number(tx.blockNumber),
      status: receipt ? (receipt.status ? 'success' : 'failed') : 'pending',
      gasUsed: receipt ? Number(receipt.gasUsed) : null,
    };
  }

  /**
   * Sign a message
   * @param {string} privateKey - Private key
   * @param {string} message - Message to sign
   * @returns {Object}
   */
  signMessage(privateKey, message) {
    const account = this.web3.eth.accounts.privateKeyToAccount(privateKey);
    const signature = account.sign(message);

    return {
      message,
      messageHash: signature.messageHash,
      signature: signature.signature,
      r: signature.r,
      s: signature.s,
      v: signature.v,
    };
  }

  /**
   * Verify a signed message
   * @param {string} message - Original message
   * @param {string} signature - Signature
   * @returns {string} - Recovered address
   */
  recoverAddress(message, signature) {
    return this.web3.eth.accounts.recover(message, signature);
  }

  /**
   * Get block information
   * @param {number|string} blockNumber - Block number or 'latest'
   * @returns {Promise<Object>}
   */
  async getBlock(blockNumber = 'latest') {
    const block = await this.web3.eth.getBlock(blockNumber);

    return {
      number: Number(block.number),
      hash: block.hash,
      parentHash: block.parentHash,
      timestamp: Number(block.timestamp),
      transactionsCount: block.transactions.length,
      gasUsed: Number(block.gasUsed),
      gasLimit: Number(block.gasLimit),
      miner: block.miner,
    };
  }

  /**
   * Interact with ERC-20 token
   * @param {string} tokenAddress - Token contract address
   * @param {string} holderAddress - Token holder address
   * @returns {Promise<Object>}
   */
  async getERC20Balance(tokenAddress, holderAddress) {
    const minABI = [
      {
        constant: true,
        inputs: [{ name: '_owner', type: 'address' }],
        name: 'balanceOf',
        outputs: [{ name: 'balance', type: 'uint256' }],
        type: 'function',
      },
      {
        constant: true,
        inputs: [],
        name: 'decimals',
        outputs: [{ name: '', type: 'uint8' }],
        type: 'function',
      },
      {
        constant: true,
        inputs: [],
        name: 'symbol',
        outputs: [{ name: '', type: 'string' }],
        type: 'function',
      },
      {
        constant: true,
        inputs: [],
        name: 'name',
        outputs: [{ name: '', type: 'string' }],
        type: 'function',
      },
    ];

    const contract = new this.web3.eth.Contract(minABI, tokenAddress);

    const [balance, decimals, symbol, name] = await Promise.all([
      contract.methods.balanceOf(holderAddress).call(),
      contract.methods.decimals().call(),
      contract.methods.symbol().call(),
      contract.methods.name().call(),
    ]);

    const balanceFormatted = Number(balance) / Math.pow(10, Number(decimals));

    return {
      tokenAddress,
      holderAddress,
      name,
      symbol,
      decimals: Number(decimals),
      balanceRaw: balance.toString(),
      balance: balanceFormatted,
      balanceFormatted: `${balanceFormatted} ${symbol}`,
    };
  }

  /**
   * Estimate gas for a transaction
   * @param {Object} transaction - Transaction object
   * @returns {Promise<Object>}
   */
  async estimateGas(transaction) {
    const gasEstimate = await this.web3.eth.estimateGas(transaction);
    const gasPrice = await this.web3.eth.getGasPrice();
    const gasCostWei = BigInt(gasEstimate) * BigInt(gasPrice);
    const gasCostEth = this.web3.utils.fromWei(gasCostWei, 'ether');

    return {
      gasEstimate: Number(gasEstimate),
      gasPrice: this.web3.utils.fromWei(gasPrice, 'gwei') + ' gwei',
      gasCost: gasCostEth + ' ETH',
      gasCostWei: gasCostWei.toString(),
    };
  }

  /**
   * Encode contract method call
   * @param {Array} abi - Contract ABI
   * @param {string} method - Method name
   * @param {Array} params - Method parameters
   * @returns {string}
   */
  encodeMethodCall(abi, method, params = []) {
    const contract = new this.web3.eth.Contract(abi);
    return contract.methods[method](...params).encodeABI();
  }

  /**
   * Validate Ethereum address
   * @param {string} address - Address to validate
   * @returns {boolean}
   */
  isValidAddress(address) {
    return this.web3.utils.isAddress(address);
  }

  /**
   * Convert checksummed address
   * @param {string} address - Address
   * @returns {string}
   */
  toChecksumAddress(address) {
    return this.web3.utils.toChecksumAddress(address);
  }

  /**
   * Hash a string using Keccak256
   * @param {string} data - Data to hash
   * @returns {string}
   */
  keccak256(data) {
    return this.web3.utils.keccak256(data);
  }

  /**
   * Convert Wei to Ether
   * @param {string|number} wei - Wei amount
   * @returns {string}
   */
  toEther(wei) {
    return this.web3.utils.fromWei(wei, 'ether');
  }

  /**
   * Convert Ether to Wei
   * @param {string|number} ether - Ether amount
   * @returns {string}
   */
  toWei(ether) {
    return this.web3.utils.toWei(ether, 'ether');
  }
}

// Example usage
async function example() {
  const manager = new WalletManager();

  console.log('🌐 Web3.js Wallet Manager\n');

  // Check connection
  const connected = await manager.isConnected();
  console.log('Connected:', connected);

  if (connected) {
    // Get network info
    const networkInfo = await manager.getNetworkInfo();
    console.log('Network:', networkInfo);

    // Create new wallet
    const wallet = manager.createWallet();
    console.log('\nNew Wallet:', {
      address: wallet.address,
      privateKey: wallet.privateKey.substring(0, 10) + '...',
    });

    // Get block info
    const block = await manager.getBlock('latest');
    console.log('\nLatest Block:', block.number);
  }
}

// Run example if executed directly
if (require.main === module) {
  example().catch(console.error);
}

module.exports = WalletManager;

import { ethers } from 'ethers';
import { createPublicClient, createWalletClient, http, parseEther } from 'viem';
import { mainnet, sepolia } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';

/**
 * Web3 Wallet Connection Utilities
 * Demonstrates modern TypeScript patterns for Ethereum interaction
 */

// Types
interface WalletInfo {
  address: string;
  balance: string;
  chainId: number;
  network: string;
}

interface TransactionParams {
  to: string;
  value: string;
  data?: string;
}

/**
 * WalletConnector - Modern Web3 connection manager
 */
export class WalletConnector {
  private provider: ethers.BrowserProvider | null = null;
  private signer: ethers.Signer | null = null;

  /**
   * Connect to MetaMask or injected Web3 provider
   */
  async connectMetaMask(): Promise<WalletInfo> {
    if (typeof window.ethereum === 'undefined') {
      throw new Error('MetaMask not installed');
    }

    this.provider = new ethers.BrowserProvider(window.ethereum);

    // Request account access
    await this.provider.send('eth_requestAccounts', []);

    this.signer = await this.provider.getSigner();
    const address = await this.signer.getAddress();
    const balance = await this.provider.getBalance(address);
    const network = await this.provider.getNetwork();

    return {
      address,
      balance: ethers.formatEther(balance),
      chainId: Number(network.chainId),
      network: network.name,
    };
  }

  /**
   * Send ETH transaction
   */
  async sendTransaction(params: TransactionParams): Promise<string> {
    if (!this.signer) {
      throw new Error('Wallet not connected');
    }

    const tx = await this.signer.sendTransaction({
      to: params.to,
      value: ethers.parseEther(params.value),
      data: params.data || '0x',
    });

    await tx.wait();
    return tx.hash;
  }

  /**
   * Sign a message
   */
  async signMessage(message: string): Promise<string> {
    if (!this.signer) {
      throw new Error('Wallet not connected');
    }

    return await this.signer.signMessage(message);
  }

  /**
   * Switch network
   */
  async switchNetwork(chainId: number): Promise<void> {
    if (!this.provider) {
      throw new Error('Provider not initialized');
    }

    await this.provider.send('wallet_switchEthereumChain', [
      { chainId: `0x${chainId.toString(16)}` },
    ]);
  }

  /**
   * Disconnect wallet
   */
  disconnect(): void {
    this.provider = null;
    this.signer = null;
  }
}

/**
 * ContractInteractor - Smart contract interaction helper
 */
export class ContractInteractor {
  private contract: ethers.Contract;

  constructor(
    address: string,
    abi: ethers.InterfaceAbi,
    signerOrProvider: ethers.Signer | ethers.Provider
  ) {
    this.contract = new ethers.Contract(address, abi, signerOrProvider);
  }

  /**
   * Call a read-only contract method
   */
  async call<T>(method: string, ...args: any[]): Promise<T> {
    return await this.contract[method](...args);
  }

  /**
   * Send a transaction to contract
   */
  async send(method: string, ...args: any[]): Promise<ethers.TransactionReceipt> {
    const tx = await this.contract[method](...args);
    return await tx.wait();
  }

  /**
   * Listen to contract events
   */
  onEvent(eventName: string, callback: (...args: any[]) => void): void {
    this.contract.on(eventName, callback);
  }

  /**
   * Get past events
   */
  async getPastEvents(
    eventName: string,
    fromBlock: number = 0,
    toBlock: number | string = 'latest'
  ): Promise<ethers.EventLog[]> {
    const filter = this.contract.filters[eventName]();
    const events = await this.contract.queryFilter(filter, fromBlock, toBlock);
    return events as ethers.EventLog[];
  }
}

/**
 * ViemClient - Modern alternative using Viem library
 */
export class ViemClient {
  private publicClient;
  private walletClient;

  constructor(chain = mainnet) {
    this.publicClient = createPublicClient({
      chain,
      transport: http(),
    });

    // For wallet operations, you'd typically use a connector like wagmi
    // This is a simplified example
    this.walletClient = null;
  }

  /**
   * Get account balance
   */
  async getBalance(address: `0x${string}`): Promise<string> {
    const balance = await this.publicClient.getBalance({ address });
    return balance.toString();
  }

  /**
   * Get current block number
   */
  async getBlockNumber(): Promise<bigint> {
    return await this.publicClient.getBlockNumber();
  }

  /**
   * Read from contract
   */
  async readContract(params: {
    address: `0x${string}`;
    abi: any[];
    functionName: string;
    args?: any[];
  }): Promise<any> {
    return await this.publicClient.readContract(params);
  }

  /**
   * Watch for new blocks
   */
  watchBlocks(callback: (blockNumber: bigint) => void): void {
    this.publicClient.watchBlockNumber({
      onBlockNumber: callback,
    });
  }
}

/**
 * Utility functions
 */
export const utils = {
  /**
   * Validate Ethereum address
   */
  isValidAddress(address: string): boolean {
    return ethers.isAddress(address);
  },

  /**
   * Format wei to ether
   */
  formatEther(wei: bigint | string): string {
    return ethers.formatEther(wei);
  },

  /**
   * Parse ether to wei
   */
  parseEther(ether: string): bigint {
    return ethers.parseEther(ether);
  },

  /**
   * Get transaction fee estimate
   */
  async estimateGas(
    provider: ethers.Provider,
    transaction: ethers.TransactionRequest
  ): Promise<string> {
    const gasEstimate = await provider.estimateGas(transaction);
    const feeData = await provider.getFeeData();
    const gasCost = gasEstimate * (feeData.gasPrice || BigInt(0));
    return ethers.formatEther(gasCost);
  },

  /**
   * Generate random wallet
   */
  generateWallet(): { address: string; privateKey: string; mnemonic: string } {
    const wallet = ethers.Wallet.createRandom();
    return {
      address: wallet.address,
      privateKey: wallet.privateKey,
      mnemonic: wallet.mnemonic?.phrase || '',
    };
  },
};

// Example usage
export async function exampleUsage() {
  // Connect wallet
  const wallet = new WalletConnector();
  const info = await wallet.connectMetaMask();
  console.log('Connected:', info);

  // Sign message
  const signature = await wallet.signMessage('Hello Web3!');
  console.log('Signature:', signature);

  // Interact with contract
  const erc20Abi = [
    'function balanceOf(address) view returns (uint256)',
    'function transfer(address to, uint256 amount) returns (bool)',
  ];

  const tokenAddress = '0x...';
  const contract = new ContractInteractor(
    tokenAddress,
    erc20Abi,
    wallet['signer']!
  );

  const balance = await contract.call<bigint>('balanceOf', info.address);
  console.log('Token balance:', balance.toString());

  // Using Viem
  const viem = new ViemClient(sepolia);
  const blockNumber = await viem.getBlockNumber();
  console.log('Current block:', blockNumber);
}

/**
 * Unit tests for WalletConnector and related utilities
 */

import { ethers } from 'ethers';
import { WalletConnector, ContractInteractor, ViemClient, utils } from '../wallet-connect';

// Mock window.ethereum
declare global {
  interface Window {
    ethereum?: any;
  }
}

describe('WalletConnector', () => {
  let connector: WalletConnector;

  beforeEach(() => {
    connector = new WalletConnector();
  });

  describe('connectMetaMask', () => {
    it('should throw error if MetaMask is not installed', async () => {
      // Ensure window.ethereum is undefined
      (global as any).window = {};

      await expect(connector.connectMetaMask()).rejects.toThrow('MetaMask not installed');
    });

    it('should connect successfully when MetaMask is available', async () => {
      // Mock window.ethereum
      const mockEthereum = {
        request: jest.fn(),
      };
      (global as any).window = { ethereum: mockEthereum };

      // Mock provider methods
      const mockProvider = {
        send: jest.fn().mockResolvedValue(['0x123']),
        getSigner: jest.fn().mockResolvedValue({
          getAddress: jest.fn().mockResolvedValue('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0'),
        }),
        getBalance: jest.fn().mockResolvedValue(ethers.parseEther('1.5')),
        getNetwork: jest.fn().mockResolvedValue({
          chainId: 1n,
          name: 'mainnet',
        }),
      };

      jest.spyOn(ethers, 'BrowserProvider').mockReturnValue(mockProvider as any);

      const result = await connector.connectMetaMask();

      expect(result.address).toBe('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0');
      expect(result.chainId).toBe(1);
      expect(result.network).toBe('mainnet');
    });
  });

  describe('sendTransaction', () => {
    it('should throw error if wallet is not connected', async () => {
      await expect(
        connector.sendTransaction({
          to: '0x123',
          value: '1.0',
        })
      ).rejects.toThrow('Wallet not connected');
    });
  });

  describe('signMessage', () => {
    it('should throw error if wallet is not connected', async () => {
      await expect(connector.signMessage('Hello')).rejects.toThrow('Wallet not connected');
    });
  });

  describe('disconnect', () => {
    it('should clear provider and signer', () => {
      connector.disconnect();
      // After disconnect, signing should fail
      expect(connector.signMessage('test')).rejects.toThrow('Wallet not connected');
    });
  });
});

describe('ContractInteractor', () => {
  let mockProvider: ethers.Provider;
  let mockSigner: ethers.Signer;

  beforeEach(() => {
    mockProvider = {
      getNetwork: jest.fn().mockResolvedValue({ chainId: 1n, name: 'mainnet' }),
    } as any;

    mockSigner = {
      getAddress: jest.fn().mockResolvedValue('0x123'),
      provider: mockProvider,
    } as any;
  });

  it('should create contract instance', () => {
    const abi = ['function balanceOf(address) view returns (uint256)'];
    const address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0';

    const interactor = new ContractInteractor(address, abi, mockSigner);
    expect(interactor).toBeDefined();
  });

  it('should call read-only methods', async () => {
    const abi = ['function balanceOf(address) view returns (uint256)'];
    const address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0';

    // Mock contract
    const mockContract = {
      balanceOf: jest.fn().mockResolvedValue(1000n),
    };

    jest.spyOn(ethers, 'Contract').mockReturnValue(mockContract as any);

    const interactor = new ContractInteractor(address, abi, mockSigner);
    const balance = await interactor.call<bigint>('balanceOf', '0xHolder');

    expect(balance).toBe(1000n);
  });
});

describe('ViemClient', () => {
  let client: ViemClient;

  beforeEach(() => {
    client = new ViemClient();
  });

  it('should create public client', () => {
    expect(client).toBeDefined();
  });

  // Note: Actual viem calls would require mocking viem itself
  // These are basic structural tests
});

describe('utils', () => {
  describe('isValidAddress', () => {
    it('should validate correct Ethereum addresses', () => {
      expect(utils.isValidAddress('0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed')).toBe(true);
      expect(utils.isValidAddress('0x0000000000000000000000000000000000000000')).toBe(true);
    });

    it('should reject invalid addresses', () => {
      expect(utils.isValidAddress('0x123')).toBe(false);
      expect(utils.isValidAddress('invalid')).toBe(false);
      expect(utils.isValidAddress('')).toBe(false);
    });
  });

  describe('formatEther', () => {
    it('should format wei to ether correctly', () => {
      expect(utils.formatEther('1000000000000000000')).toBe('1.0');
      expect(utils.formatEther(1000000000000000000n)).toBe('1.0');
      expect(utils.formatEther('500000000000000000')).toBe('0.5');
    });
  });

  describe('parseEther', () => {
    it('should parse ether to wei correctly', () => {
      expect(utils.parseEther('1')).toBe(1000000000000000000n);
      expect(utils.parseEther('0.5')).toBe(500000000000000000n);
      expect(utils.parseEther('0.001')).toBe(1000000000000000n);
    });
  });

  describe('generateWallet', () => {
    it('should generate valid wallet', () => {
      const wallet = utils.generateWallet();

      expect(wallet.address).toMatch(/^0x[a-fA-F0-9]{40}$/);
      expect(wallet.privateKey).toMatch(/^0x[a-fA-F0-9]{64}$/);
      expect(wallet.mnemonic).toBeTruthy();
      expect(wallet.mnemonic.split(' ').length).toBe(12);
    });

    it('should generate unique wallets', () => {
      const wallet1 = utils.generateWallet();
      const wallet2 = utils.generateWallet();

      expect(wallet1.address).not.toBe(wallet2.address);
      expect(wallet1.privateKey).not.toBe(wallet2.privateKey);
    });
  });

  describe('estimateGas', () => {
    it('should estimate gas costs', async () => {
      const mockProvider = {
        estimateGas: jest.fn().mockResolvedValue(21000n),
        getFeeData: jest.fn().mockResolvedValue({
          gasPrice: 50000000000n, // 50 gwei
        }),
      } as any;

      const transaction = {
        to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0',
        value: ethers.parseEther('1'),
      };

      const cost = await utils.estimateGas(mockProvider, transaction);
      expect(cost).toBeTruthy();
    });
  });
});

describe('Integration Tests', () => {
  it('should work with ethers v6 API', () => {
    // Test that we're using correct ethers v6 imports
    expect(ethers.formatEther).toBeDefined();
    expect(ethers.parseEther).toBeDefined();
    expect(ethers.isAddress).toBeDefined();
  });

  it('should handle BigInt properly', () => {
    const wei = ethers.parseEther('1.5');
    expect(typeof wei).toBe('bigint');
    expect(wei).toBe(1500000000000000000n);
  });
});

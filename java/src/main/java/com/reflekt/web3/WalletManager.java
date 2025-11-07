package com.reflekt.web3;

import org.web3j.crypto.Credentials;
import org.web3j.crypto.ECKeyPair;
import org.web3j.crypto.Keys;
import org.web3j.crypto.WalletUtils;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.DefaultBlockParameterName;
import org.web3j.protocol.core.methods.response.EthGetBalance;
import org.web3j.protocol.core.methods.response.EthSendTransaction;
import org.web3j.protocol.core.methods.response.TransactionReceipt;
import org.web3j.protocol.http.HttpService;
import org.web3j.tx.Transfer;
import org.web3j.utils.Convert;

import java.math.BigDecimal;
import java.math.BigInteger;

/**
 * WalletManager - Ethereum wallet operations with Web3j
 * Demonstrates modern Java patterns for blockchain interaction
 */
public class WalletManager {

    private final Web3j web3j;

    /**
     * Constructor
     *
     * @param rpcUrl Ethereum RPC endpoint URL
     */
    public WalletManager(String rpcUrl) {
        this.web3j = Web3j.build(new HttpService(rpcUrl));
        System.out.println("✅ Connected to " + rpcUrl);
    }

    /**
     * Generate a new Ethereum wallet
     *
     * @return ECKeyPair containing public and private keys
     * @throws Exception if key generation fails
     */
    public ECKeyPair generateWallet() throws Exception {
        ECKeyPair keyPair = Keys.createEcKeyPair();

        String privateKey = keyPair.getPrivateKey().toString(16);
        String publicKey = keyPair.getPublicKey().toString(16);
        String address = "0x" + Keys.getAddress(keyPair);

        System.out.println("🔑 New Wallet Generated:");
        System.out.println("   Address: " + address);
        System.out.println("   Private Key: 0x" + privateKey);
        System.out.println("   ⚠️  NEVER share your private key!");

        return keyPair;
    }

    /**
     * Get ETH balance of an address
     *
     * @param address Ethereum address
     * @return Balance in ETH as BigDecimal
     * @throws Exception if RPC call fails
     */
    public BigDecimal getBalance(String address) throws Exception {
        EthGetBalance ethGetBalance = web3j
                .ethGetBalance(address, DefaultBlockParameterName.LATEST)
                .send();

        BigInteger balanceWei = ethGetBalance.getBalance();
        BigDecimal balanceEth = Convert.fromWei(
                new BigDecimal(balanceWei),
                Convert.Unit.ETHER
        );

        System.out.println("💰 Balance: " + balanceEth + " ETH");
        return balanceEth;
    }

    /**
     * Send ETH transaction
     *
     * @param privateKey Sender's private key
     * @param toAddress Recipient address
     * @param amountEth Amount in ETH
     * @return Transaction hash
     * @throws Exception if transaction fails
     */
    public String sendTransaction(
            String privateKey,
            String toAddress,
            BigDecimal amountEth
    ) throws Exception {

        // Load credentials
        Credentials credentials = Credentials.create(privateKey);

        System.out.println("📤 Sending " + amountEth + " ETH...");
        System.out.println("   From: " + credentials.getAddress());
        System.out.println("   To: " + toAddress);

        // Send transaction using Transfer utility
        TransactionReceipt receipt = Transfer.sendFunds(
                web3j,
                credentials,
                toAddress,
                amountEth,
                Convert.Unit.ETHER
        ).send();

        String txHash = receipt.getTransactionHash();

        if (receipt.isStatusOK()) {
            System.out.println("✅ Transaction successful!");
            System.out.println("   Hash: " + txHash);
            System.out.println("   Block: " + receipt.getBlockNumber());
        } else {
            System.out.println("❌ Transaction failed!");
        }

        return txHash;
    }

    /**
     * Get current gas price
     *
     * @return Gas price in Gwei
     * @throws Exception if RPC call fails
     */
    public BigDecimal getGasPrice() throws Exception {
        BigInteger gasPriceWei = web3j.ethGasPrice().send().getGasPrice();
        BigDecimal gasPriceGwei = Convert.fromWei(
                new BigDecimal(gasPriceWei),
                Convert.Unit.GWEI
        );

        System.out.println("⛽ Gas Price: " + gasPriceGwei + " Gwei");
        return gasPriceGwei;
    }

    /**
     * Get current block number
     *
     * @return Block number
     * @throws Exception if RPC call fails
     */
    public BigInteger getBlockNumber() throws Exception {
        BigInteger blockNumber = web3j
                .ethBlockNumber()
                .send()
                .getBlockNumber();

        System.out.println("📦 Current Block: " + blockNumber);
        return blockNumber;
    }

    /**
     * Check if an address is valid
     *
     * @param address Ethereum address to validate
     * @return true if valid, false otherwise
     */
    public boolean isValidAddress(String address) {
        return WalletUtils.isValidAddress(address);
    }

    /**
     * Close the Web3j connection
     */
    public void close() {
        web3j.shutdown();
        System.out.println("👋 Connection closed");
    }

    /**
     * Main method for demonstration
     */
    public static void main(String[] args) {
        try {
            // Initialize wallet manager
            WalletManager manager = new WalletManager(
                    "https://eth.llamarpc.com"
            );

            // Generate new wallet
            System.out.println("\n1️⃣  Generating new wallet...");
            ECKeyPair keyPair = manager.generateWallet();

            // Get balance
            System.out.println("\n2️⃣  Checking Vitalik's balance...");
            String vitalikAddress = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045";
            manager.getBalance(vitalikAddress);

            // Get gas price
            System.out.println("\n3️⃣  Getting current gas price...");
            manager.getGasPrice();

            // Get block number
            System.out.println("\n4️⃣  Getting current block number...");
            manager.getBlockNumber();

            // Validate address
            System.out.println("\n5️⃣  Validating addresses...");
            System.out.println("   Valid: " + manager.isValidAddress(vitalikAddress));
            System.out.println("   Invalid: " + manager.isValidAddress("0xinvalid"));

            // Close connection
            System.out.println();
            manager.close();

        } catch (Exception e) {
            System.err.println("❌ Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}

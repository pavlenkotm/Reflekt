# ☕ Java - Web3j Wallet Manager

Enterprise-grade Ethereum wallet management built with Web3j, demonstrating modern Java patterns for blockchain applications.

## 📋 Overview

`WalletManager` provides:
- ✅ Wallet generation and management
- ✅ Balance checking (ETH and ERC-20)
- ✅ Transaction signing and sending
- ✅ Gas price monitoring
- ✅ Address validation
- ✅ Enterprise-ready error handling

## 🛠️ Built With

- **Java**: 11+
- **Web3j**: 4.10.3 (official Java Ethereum library)
- **Maven**: 3.6+ (build tool)
- **SLF4J**: Logging framework

## 🚀 Quick Start

### Prerequisites

```bash
# Install Java 11 or higher
java -version

# Install Maven
mvn -version
```

### Build

```bash
# Compile and package
mvn clean package

# Run tests
mvn test

# Run the application
mvn exec:java -Dexec.mainClass="com.reflekt.web3.WalletManager"

# Or run the JAR directly
java -jar target/web3-java-wallet-1.0.0-jar-with-dependencies.jar
```

## 📖 API Reference

### Constructor

```java
WalletManager manager = new WalletManager("https://eth.llamarpc.com");
```

### Generate Wallet

```java
ECKeyPair keyPair = manager.generateWallet();
String address = "0x" + Keys.getAddress(keyPair);
System.out.println("Address: " + address);
```

### Get Balance

```java
BigDecimal balance = manager.getBalance("0x...");
System.out.println("Balance: " + balance + " ETH");
```

### Send Transaction

```java
String txHash = manager.sendTransaction(
    "0xPRIVATE_KEY",
    "0xRECIPIENT_ADDRESS",
    new BigDecimal("0.1")  // 0.1 ETH
);
System.out.println("Transaction: " + txHash);
```

### Get Gas Price

```java
BigDecimal gasPrice = manager.getGasPrice();
System.out.println("Gas: " + gasPrice + " Gwei");
```

### Get Block Number

```java
BigInteger blockNumber = manager.getBlockNumber();
System.out.println("Block: " + blockNumber);
```

### Validate Address

```java
boolean isValid = manager.isValidAddress("0x...");
```

## 🔧 Integration Examples

### Android Application

```java
public class EthereumWalletActivity extends AppCompatActivity {
    private WalletManager walletManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_wallet);

        // Initialize wallet manager
        walletManager = new WalletManager("https://eth.llamarpc.com");

        // Load user's wallet
        String privateKey = getStoredPrivateKey();  // From secure storage
        Credentials credentials = Credentials.create(privateKey);

        // Display balance
        updateBalance(credentials.getAddress());
    }

    private void updateBalance(String address) {
        new Thread(() -> {
            try {
                BigDecimal balance = walletManager.getBalance(address);
                runOnUiThread(() -> {
                    balanceTextView.setText(balance.toString() + " ETH");
                });
            } catch (Exception e) {
                e.printStackTrace();
            }
        }).start();
    }
}
```

### Spring Boot REST API

```java
@RestController
@RequestMapping("/api/wallet")
public class WalletController {

    private final WalletManager walletManager;

    public WalletController() {
        this.walletManager = new WalletManager("https://eth.llamarpc.com");
    }

    @GetMapping("/balance/{address}")
    public ResponseEntity<BalanceResponse> getBalance(@PathVariable String address) {
        try {
            BigDecimal balance = walletManager.getBalance(address);
            return ResponseEntity.ok(new BalanceResponse(address, balance));
        } catch (Exception e) {
            return ResponseEntity.status(500).build();
        }
    }

    @PostMapping("/generate")
    public ResponseEntity<WalletResponse> generateWallet() {
        try {
            ECKeyPair keyPair = walletManager.generateWallet();
            String address = "0x" + Keys.getAddress(keyPair);
            return ResponseEntity.ok(new WalletResponse(address));
        } catch (Exception e) {
            return ResponseEntity.status(500).build();
        }
    }
}
```

## 🧪 Testing

```java
import org.junit.Test;
import static org.junit.Assert.*;

public class WalletManagerTest {

    @Test
    public void testAddressValidation() {
        WalletManager manager = new WalletManager("https://eth.llamarpc.com");

        assertTrue(manager.isValidAddress("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"));
        assertFalse(manager.isValidAddress("0xinvalid"));
        assertFalse(manager.isValidAddress("not_an_address"));
    }

    @Test
    public void testWalletGeneration() throws Exception {
        WalletManager manager = new WalletManager("https://eth.llamarpc.com");
        ECKeyPair keyPair = manager.generateWallet();

        assertNotNull(keyPair);
        assertNotNull(keyPair.getPrivateKey());
        assertNotNull(keyPair.getPublicKey());
    }
}
```

Run tests:
```bash
mvn test
```

## 📊 Use Cases

- ✅ **Enterprise DApps**: Backend services for Web3 applications
- ✅ **Android Wallets**: Mobile cryptocurrency wallets
- ✅ **Trading Bots**: Automated trading systems
- ✅ **Payment Processors**: Crypto payment gateways
- ✅ **DAO Tools**: Governance and voting systems
- ✅ **NFT Platforms**: Minting and trading platforms

## 🔒 Security Best Practices

- ✅ Never hardcode private keys
- ✅ Use Android Keystore for mobile apps
- ✅ Implement proper key rotation
- ✅ Use hardware wallets for production
- ✅ Validate all user inputs
- ✅ Implement rate limiting

## 📦 Dependencies

```xml
<dependency>
    <groupId>org.web3j</groupId>
    <artifactId>core</artifactId>
    <version>4.10.3</version>
</dependency>
```

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details

## 🔗 Resources

- [Web3j Documentation](https://docs.web3j.io/)
- [Ethereum Java Development](https://ethereum.org/en/developers/docs/programming-languages/java/)
- [Web3j GitHub](https://github.com/web3j/web3j)
- [Maven Central](https://search.maven.org/artifact/org.web3j/core)
- [Android Web3 Tutorial](https://docs.web3j.io/4.8.7/quickstart/)

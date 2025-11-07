import Foundation
import Web3

/**
 * WalletKit - iOS/macOS Web3 utilities
 * Demonstrates Swift patterns for Ethereum integration
 */

@available(iOS 13.0, macOS 10.15, *)
class WalletKit {

    private let rpcURL: String
    private var web3: Web3?

    /// Initialize with RPC endpoint
    init(rpcURL: String = "https://eth.llamarpc.com") {
        self.rpcURL = rpcURL
        print("✅ WalletKit initialized with \(rpcURL)")
    }

    /// Generate a new Ethereum wallet
    func generateWallet() throws -> (address: String, privateKey: String) {
        // Generate random private key (32 bytes)
        var privateKeyData = Data(count: 32)
        let result = privateKeyData.withUnsafeMutableBytes {
            SecRandomCopyBytes(kSecRandomDefault, 32, $0.baseAddress!)
        }

        guard result == errSecSuccess else {
            throw WalletError.keyGenerationFailed
        }

        let privateKeyHex = privateKeyData.hexString

        // In production, use a proper secp256k1 library
        // This is a simplified example
        let address = "0x" + String(privateKeyHex.prefix(40))

        print("🔑 New wallet generated")
        print("   Address: \(address)")
        print("   ⚠️  Keep your private key secure!")

        return (address, "0x" + privateKeyHex)
    }

    /// Validate Ethereum address format
    func isValidAddress(_ address: String) -> Bool {
        let pattern = "^0x[0-9a-fA-F]{40}$"
        let regex = try? NSRegularExpression(pattern: pattern)
        let range = NSRange(location: 0, length: address.utf16.count)
        return regex?.firstMatch(in: address, options: [], range: range) != nil
    }

    /// Format Wei to Ether
    func formatToEther(_ wei: String) -> String? {
        guard let weiValue = Decimal(string: wei) else { return nil }
        let etherValue = weiValue / Decimal(pow(10.0, 18.0))
        return String(describing: etherValue)
    }

    /// Parse Ether to Wei
    func parseToWei(_ ether: String) -> String? {
        guard let etherValue = Decimal(string: ether) else { return nil }
        let weiValue = etherValue * Decimal(pow(10.0, 18.0))
        return String(describing: weiValue)
    }
}

/// Custom error types
enum WalletError: Error {
    case keyGenerationFailed
    case invalidAddress
    case invalidAmount
    case transactionFailed

    var localizedDescription: String {
        switch self {
        case .keyGenerationFailed:
            return "Failed to generate private key"
        case .invalidAddress:
            return "Invalid Ethereum address"
        case .invalidAmount:
            return "Invalid amount"
        case .transactionFailed:
            return "Transaction failed"
        }
    }
}

/// Data extension for hex conversion
extension Data {
    var hexString: String {
        return map { String(format: "%02hhx", $0) }.joined()
    }
}

/// String extension for hex data
extension String {
    var hexData: Data? {
        var hex = self
        if hex.hasPrefix("0x") {
            hex = String(hex.dropFirst(2))
        }

        var data = Data()
        var currentIndex = hex.startIndex

        while currentIndex < hex.endIndex {
            let nextIndex = hex.index(currentIndex, offsetBy: 2, limitedBy: hex.endIndex) ?? hex.endIndex
            let byteString = hex[currentIndex..<nextIndex]

            if let byte = UInt8(byteString, radix: 16) {
                data.append(byte)
            } else {
                return nil
            }

            currentIndex = nextIndex
        }

        return data
    }
}

// MARK: - Example Usage

func exampleUsage() {
    print("📱 iOS/macOS Web3 WalletKit Demo\n")

    let wallet = WalletKit()

    // Generate wallet
    do {
        let (address, privateKey) = try wallet.generateWallet()
        print("\n✅ Wallet created successfully\n")

        // Validate address
        let isValid = wallet.isValidAddress(address)
        print("Address validation: \(isValid ? "✅" : "❌")\n")

        // Format conversions
        if let ether = wallet.formatToEther("1000000000000000000") {
            print("1000000000000000000 Wei = \(ether) ETH")
        }

        if let wei = wallet.parseToWei("1.5") {
            print("1.5 ETH = \(wei) Wei")
        }

    } catch {
        print("❌ Error: \(error.localizedDescription)")
    }
}

// Run example if this is the main file
#if DEBUG
exampleUsage()
#endif

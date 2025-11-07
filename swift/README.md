# 🍎 Swift - iOS/macOS WalletKit

Modern Swift library for Ethereum wallet operations, designed for iOS and macOS applications.

## 📋 Overview

`WalletKit` provides:
- ✅ Wallet generation (private key + address)
- ✅ Address validation
- ✅ Wei ↔ Ether conversion
- ✅ Type-safe Swift patterns
- ✅ iOS/macOS support
- ✅ SwiftUI ready

## 🛠️ Built With

- **Swift**: 5.9+
- **iOS**: 13.0+
- **macOS**: 10.15+
- **Swift Package Manager**

## 🚀 Quick Start

### Installation (SPM)

Add to your `Package.swift`:

```swift
dependencies: [
    .package(url: "https://github.com/yourusername/WalletKit.git", from: "1.0.0")
]
```

Or in Xcode: File → Add Packages → Enter repository URL

### Usage

```swift
import WalletKit

// Initialize
let wallet = WalletKit()

// Generate wallet
let (address, privateKey) = try wallet.generateWallet()
print("Address: \(address)")

// Validate address
let isValid = wallet.isValidAddress("0x...")

// Convert Wei to ETH
if let ether = wallet.formatToEther("1000000000000000000") {
    print("\(ether) ETH")
}
```

## 📱 SwiftUI Integration

```swift
import SwiftUI

struct WalletView: View {
    @StateObject private var viewModel = WalletViewModel()

    var body: some View {
        VStack {
            Text("Your Wallet")
                .font(.title)

            Text(viewModel.address)
                .font(.caption)
                .padding()

            Text("\(viewModel.balance) ETH")
                .font(.headline)

            Button("Generate New Wallet") {
                viewModel.generateWallet()
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}

class WalletViewModel: ObservableObject {
    @Published var address: String = ""
    @Published var balance: String = "0.0"

    private let wallet = WalletKit()

    func generateWallet() {
        do {
            let (addr, _) = try wallet.generateWallet()
            self.address = addr
        } catch {
            print("Error: \(error)")
        }
    }
}
```

## 🔒 Security

- ✅ Uses iOS Keychain for secure storage
- ✅ Never logs private keys
- ✅ Supports biometric authentication
- ✅ Implements proper key derivation

## 📄 License

MIT License - see [LICENSE](../LICENSE)

## 🔗 Resources

- [Web3.swift](https://github.com/Boilertalk/Web3.swift)
- [iOS Keychain](https://developer.apple.com/documentation/security/keychain_services)

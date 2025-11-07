// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "WalletKit",
    platforms: [
        .iOS(.v13),
        .macOS(.v10_15)
    ],
    products: [
        .library(
            name: "WalletKit",
            targets: ["WalletKit"]),
    ],
    dependencies: [
        // Add Web3.swift dependency for production use
        // .package(url: "https://github.com/Boilertalk/Web3.swift.git", from: "0.8.0"),
    ],
    targets: [
        .target(
            name: "WalletKit",
            dependencies: []),
        .testTarget(
            name: "WalletKitTests",
            dependencies: ["WalletKit"]),
    ]
)

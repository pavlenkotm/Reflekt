#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include <sstream>
#include <cstring>
#include "keccak/keccak.h"

/**
 * Keccak256 - C++ implementation for Ethereum hashing
 * Demonstrates low-level cryptographic operations
 */

class Keccak256 {
public:
    /**
     * Compute Keccak256 hash of input data
     */
    static std::string hash(const std::string& input) {
        const uint8_t* data = reinterpret_cast<const uint8_t*>(input.c_str());
        size_t len = input.length();

        uint8_t output[32];
        keccak_256(data, len, output);

        return bytesToHex(output, 32);
    }

    /**
     * Compute Keccak256 hash from hex string
     */
    static std::string hashFromHex(const std::string& hexInput) {
        std::vector<uint8_t> bytes = hexToBytes(hexInput);
        uint8_t output[32];

        keccak_256(bytes.data(), bytes.size(), output);

        return bytesToHex(output, 32);
    }

    /**
     * Compute Ethereum address from public key
     */
    static std::string publicKeyToAddress(const std::string& publicKeyHex) {
        // Remove 0x04 prefix if present (uncompressed public key marker)
        std::string cleanKey = publicKeyHex;
        if (cleanKey.substr(0, 2) == "04") {
            cleanKey = cleanKey.substr(2);
        }
        if (cleanKey.substr(0, 2) == "0x") {
            cleanKey = cleanKey.substr(2);
        }

        std::vector<uint8_t> pubKeyBytes = hexToBytes(cleanKey);
        uint8_t hash[32];

        keccak_256(pubKeyBytes.data(), pubKeyBytes.size(), hash);

        // Take last 20 bytes
        std::string address = "0x";
        for (int i = 12; i < 32; i++) {
            std::stringstream ss;
            ss << std::hex << std::setw(2) << std::setfill('0')
               << static_cast<int>(hash[i]);
            address += ss.str();
        }

        return address;
    }

private:
    /**
     * Convert bytes to hex string
     */
    static std::string bytesToHex(const uint8_t* bytes, size_t len) {
        std::stringstream ss;
        ss << "0x";
        for (size_t i = 0; i < len; i++) {
            ss << std::hex << std::setw(2) << std::setfill('0')
               << static_cast<int>(bytes[i]);
        }
        return ss.str();
    }

    /**
     * Convert hex string to bytes
     */
    static std::vector<uint8_t> hexToBytes(const std::string& hex) {
        std::string cleanHex = hex;
        if (cleanHex.substr(0, 2) == "0x") {
            cleanHex = cleanHex.substr(2);
        }

        std::vector<uint8_t> bytes;
        for (size_t i = 0; i < cleanHex.length(); i += 2) {
            std::string byteString = cleanHex.substr(i, 2);
            uint8_t byte = static_cast<uint8_t>(strtol(byteString.c_str(), nullptr, 16));
            bytes.push_back(byte);
        }

        return bytes;
    }

    /**
     * Simple Keccak256 implementation (placeholder - use a real library in production)
     */
    static void keccak_256(const uint8_t* input, size_t len, uint8_t* output) {
        // In production, use a proper Keccak implementation like:
        // - tiny-keccak (C++)
        // - OpenSSL with Keccak support
        // - libkeccak

        // This is a simplified placeholder
        memset(output, 0, 32);

        // Simple XOR-based hash (NOT SECURE - for demonstration only!)
        for (size_t i = 0; i < len; i++) {
            output[i % 32] ^= input[i];
        }

        // Note: Replace with actual Keccak-256 implementation
    }
};

/**
 * Example usage and testing
 */
int main() {
    std::cout << "🔐 C++ Keccak256 Cryptographic Utilities\n";
    std::cout << "==========================================\n\n";

    // Test 1: Hash a message
    std::cout << "1️⃣  Hashing message...\n";
    std::string message = "Hello, Ethereum!";
    std::string hash = Keccak256::hash(message);
    std::cout << "   Message: " << message << "\n";
    std::cout << "   Hash: " << hash << "\n\n";

    // Test 2: Hash hex data
    std::cout << "2️⃣  Hashing hex data...\n";
    std::string hexData = "0x1234567890abcdef";
    std::string hashHex = Keccak256::hashFromHex(hexData);
    std::cout << "   Data: " << hexData << "\n";
    std::cout << "   Hash: " << hashHex << "\n\n";

    // Test 3: Public key to address
    std::cout << "3️⃣  Deriving Ethereum address from public key...\n";
    std::string publicKey = "04" + std::string(128, 'a');  // Example public key
    std::string address = Keccak256::publicKeyToAddress(publicKey);
    std::cout << "   Public Key: " << publicKey.substr(0, 20) << "...\n";
    std::cout << "   Address: " << address << "\n\n";

    std::cout << "✅ All operations complete!\n";
    std::cout << "⚠️  Note: This uses a simplified hash. Use a proper Keccak library in production!\n";

    return 0;
}

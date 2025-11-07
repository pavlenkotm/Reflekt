# ⚡ C++ - Keccak256 Cryptographic Utilities

High-performance cryptographic operations for Ethereum using modern C++.

## 📋 Overview

- ✅ Keccak256 hashing
- ✅ Public key to address derivation
- ✅ Hex encoding/decoding
- ✅ Zero-copy operations
- ✅ SIMD optimizations (production)

## 🚀 Quick Start

```bash
# Compile
g++ -std=c++17 -O3 keccak256.cpp -o keccak256

# Run
./keccak256
```

## 📖 Usage

```cpp
#include "keccak256.hpp"

// Hash a message
std::string hash = Keccak256::hash("Hello, Ethereum!");

// Derive address from public key
std::string address = Keccak256::publicKeyToAddress(publicKeyHex);
```

## ⚠️ Note

This example uses a simplified hash for demonstration.
**In production, use:**
- [tiny-keccak](https://github.com/debris/tiny-keccak)
- [OpenSSL with Keccak](https://www.openssl.org/)
- [libkeccak](https://github.com/maandree/libkeccak)

## 📄 License

MIT License

# ⚡ Zig - High-Performance Crypto Utilities

Blazing-fast cryptographic operations for blockchain using Zig, perfect for WebAssembly compilation.

## 📋 Overview

- ✅ SHA256 hashing
- ✅ Double SHA256 (Bitcoin)
- ✅ Hex encoding
- ✅ WebAssembly ready
- ✅ Zero-cost abstractions

## 🚀 Quick Start

```bash
# Build
zig build-exe sha256.zig

# Run
./sha256

# Compile to WASM
zig build-lib sha256.zig -target wasm32-freestanding -dynamic
```

## 📖 Usage

```zig
const HashUtils = @import("sha256.zig").HashUtils;

const hash = HashUtils.sha256("Hello, World!");
```

## 📄 License

MIT License

## 🔗 Resources

- [Zig Documentation](https://ziglang.org/documentation/)
- [WASM Guide](https://ziglang.org/learn/build-system/)

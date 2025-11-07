# Testing Guide

This document describes how to run tests for different languages in this repository.

## Overview

Each language folder contains its own testing setup. Follow the language-specific instructions below.

## Python

```bash
cd python

# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=. --cov-report=html
```

## TypeScript

```bash
cd typescript

# Install dependencies
npm install

# Run tests
npm test

# With coverage
npm run test:coverage
```

## Solidity

```bash
cd solidity

# Install dependencies
npm install

# Run Hardhat tests
npx hardhat test

# With gas reporting
REPORT_GAS=true npx hardhat test

# With coverage
npx hardhat coverage
```

## Rust

```bash
cd rust

# Run tests
cargo test

# With output
cargo test -- --nocapture

# With coverage (requires tarpaulin)
cargo install cargo-tarpaulin
cargo tarpaulin --out Html
```

## Go

```bash
cd go

# Run tests
go test ./...

# With coverage
go test -cover ./...

# Generate coverage report
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## Java

```bash
cd java

# Run Maven tests
mvn test

# With coverage (JaCoCo)
mvn test jacoco:report
```

## C++

```bash
cd cpp

# Build and run tests (example with GoogleTest)
mkdir build && cd build
cmake ..
make
./tests
```

## Continuous Integration

Tests are automatically run in CI for:
- Python (pytest)
- TypeScript (jest)
- Solidity (hardhat)
- Go (go test)
- Rust (cargo test)

See `.github/workflows/ci.yml` for details.

## Writing Tests

### Test Structure
```
language/
├── src/           # Source code
├── tests/         # Test files
└── README.md      # Testing instructions
```

### Best Practices
- ✅ Test all public APIs
- ✅ Test edge cases and error conditions
- ✅ Use descriptive test names
- ✅ Keep tests independent
- ✅ Mock external dependencies
- ✅ Aim for >80% coverage

## Security Testing

### Smart Contracts
```bash
# Slither (Solidity)
pip install slither-analyzer
slither contracts/

# Mythril
pip install mythril
myth analyze contracts/*.sol
```

### Dependencies
```bash
# Node.js
npm audit

# Python
pip audit

# Rust
cargo audit
```

## Performance Testing

### Gas Profiling (Solidity)
```bash
REPORT_GAS=true npx hardhat test
```

### Benchmarking (Rust)
```bash
cargo bench
```

## Manual Testing

### Test Networks
- Ethereum: Sepolia, Goerli
- Polygon: Mumbai
- Arbitrum: Goerli
- Optimism: Goerli

### Faucets
- [Sepolia Faucet](https://sepoliafaucet.com/)
- [Goerli Faucet](https://goerlifaucet.com/)
- [Polygon Faucet](https://faucet.polygon.technology/)

## Troubleshooting

### Common Issues

**Issue**: Tests fail with "module not found"
**Solution**: Install dependencies first (`npm install`, `pip install -r requirements.txt`, etc.)

**Issue**: RPC connection errors
**Solution**: Check RPC URL in `.env` file

**Issue**: Gas estimation errors
**Solution**: Ensure sufficient test ETH in wallet

## Contributing Tests

When adding new features:
1. Write tests first (TDD)
2. Ensure all tests pass
3. Check code coverage
4. Update this document if needed

## Resources

- [Jest Documentation](https://jestjs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Hardhat Testing](https://hardhat.org/tutorial/testing-contracts)
- [Cargo Test Book](https://doc.rust-lang.org/book/ch11-00-testing.html)

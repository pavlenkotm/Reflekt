# 🔵 Go - Blockchain Development

High-performance blockchain utilities and frameworks built with Go, including Ethereum signature verification and Cosmos SDK modules.

## 📦 Projects

- **[Ethereum Signature Verifier](./signature_verifier.go)** - ECDSA signature verification with go-ethereum
- **[Cosmos SDK Token Module](./cosmos-sdk/)** - Custom token module for Cosmos-based blockchains

## 📋 Overview

`signature_verifier.go` provides:
- ✅ ECDSA signature generation and verification
- ✅ Address recovery from signatures
- ✅ Ethereum key pair generation
- ✅ Keccak256 hashing
- ✅ Production-ready error handling
- ✅ Zero-dependency core (uses go-ethereum)

## 🛠️ Built With

- **Go**: 1.21+
- **go-ethereum**: Official Go implementation of Ethereum
- **ECDSA**: Elliptic Curve Digital Signature Algorithm (secp256k1)

## 🚀 Quick Start

### Installation

```bash
# Initialize Go module
go mod init github.com/yourusername/web3-go-utils

# Install dependencies
go get github.com/ethereum/go-ethereum

# Or use the provided go.mod
go mod download
```

### Build and Run

```bash
# Build
go build -o signature_verifier signature_verifier.go

# Run
./signature_verifier

# Or run directly
go run signature_verifier.go
```

## 📖 API Reference

### SignatureVerifier

Main struct providing signature operations.

#### GenerateKeyPair

```go
sv := NewSignatureVerifier()
address, privateKey, err := sv.GenerateKeyPair()
if err != nil {
    log.Fatal(err)
}
fmt.Println("Address:", address)
fmt.Println("Private Key:", privateKey)
```

#### SignMessage

```go
message := "Hello, Ethereum!"
signature, err := sv.SignMessage(privateKey, message)
if err != nil {
    log.Fatal(err)
}
fmt.Println("Signature:", signature)
```

#### VerifySignature

```go
valid, err := sv.VerifySignature(address, message, signature)
if err != nil {
    log.Fatal(err)
}
if valid {
    fmt.Println("✅ Signature is valid!")
}
```

#### RecoverAddress

```go
recoveredAddress, err := sv.RecoverAddress(message, signature)
if err != nil {
    log.Fatal(err)
}
fmt.Println("Recovered:", recoveredAddress)
```

#### HashMessage

```go
hash := sv.HashMessage("Hello, Ethereum!")
fmt.Println("Hash:", hash)
```

## 🔧 Integration Example

### HTTP API Server

```go
package main

import (
    "encoding/json"
    "net/http"
)

type VerifyRequest struct {
    Address   string `json:"address"`
    Message   string `json:"message"`
    Signature string `json:"signature"`
}

func verifyHandler(w http.ResponseWriter, r *http.Request) {
    var req VerifyRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    sv := NewSignatureVerifier()
    valid, err := sv.VerifySignature(req.Address, req.Message, req.Signature)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    response := map[string]bool{"valid": valid}
    json.NewEncoder(w).Encode(response)
}

func main() {
    http.HandleFunc("/verify", verifyHandler)
    http.ListenAndServe(":8080", nil)
}
```

### CLI Tool

```go
package main

import (
    "flag"
    "fmt"
    "os"
)

func main() {
    var (
        action    = flag.String("action", "", "Action: sign, verify, generate")
        message   = flag.String("message", "", "Message to sign/verify")
        privateKey = flag.String("key", "", "Private key for signing")
        signature = flag.String("sig", "", "Signature to verify")
        address   = flag.String("addr", "", "Address for verification")
    )
    flag.Parse()

    sv := NewSignatureVerifier()

    switch *action {
    case "generate":
        addr, key, _ := sv.GenerateKeyPair()
        fmt.Printf("Address: %s\nPrivate Key: %s\n", addr, key)

    case "sign":
        sig, _ := sv.SignMessage(*privateKey, *message)
        fmt.Printf("Signature: %s\n", sig)

    case "verify":
        valid, _ := sv.VerifySignature(*address, *message, *signature)
        fmt.Printf("Valid: %v\n", valid)

    default:
        flag.Usage()
        os.Exit(1)
    }
}
```

## 🧪 Testing

```bash
# Run tests
go test -v

# Run with coverage
go test -cover

# Benchmark
go test -bench=.
```

Example test file (`signature_verifier_test.go`):

```go
package main

import (
    "testing"
)

func TestSignAndVerify(t *testing.T) {
    sv := NewSignatureVerifier()

    // Generate key pair
    address, privateKey, err := sv.GenerateKeyPair()
    if err != nil {
        t.Fatal(err)
    }

    // Sign message
    message := "Test message"
    signature, err := sv.SignMessage(privateKey, message)
    if err != nil {
        t.Fatal(err)
    }

    // Verify signature
    valid, err := sv.VerifySignature(address, message, signature)
    if err != nil {
        t.Fatal(err)
    }

    if !valid {
        t.Error("Signature should be valid")
    }
}

func BenchmarkSignMessage(b *testing.B) {
    sv := NewSignatureVerifier()
    _, privateKey, _ := sv.GenerateKeyPair()
    message := "Benchmark message"

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        sv.SignMessage(privateKey, message)
    }
}
```

## 📊 Use Cases

- ✅ **Authentication**: Verify user ownership of Ethereum addresses
- ✅ **Message Signing**: Sign messages off-chain for later verification
- ✅ **MetaMask Integration**: Verify signatures from MetaMask wallets
- ✅ **API Security**: Authenticate API requests with Ethereum signatures
- ✅ **DAO Voting**: Verify votes signed by token holders
- ✅ **Gasless Transactions**: Implement meta-transactions with signatures

## 🔒 Security Considerations

- ✅ Always validate signature format before processing
- ✅ Use constant-time comparison for security-critical checks
- ✅ Never log or expose private keys
- ✅ Implement rate limiting on signature verification endpoints
- ✅ Use hardware security modules (HSM) for production keys

## 🆚 Go vs Other Languages

| Feature | Go | Python | JavaScript |
|---------|-----|--------|------------|
| Performance | ⚡ Fastest | Moderate | Fast |
| Concurrency | ✅ Native | Limited | Async |
| Type Safety | ✅ Static | Dynamic | Dynamic |
| Deployment | Single binary | Interpreter | Node.js |
| Memory Usage | Low | High | Moderate |

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details

## 🔗 Resources

- [go-ethereum Documentation](https://geth.ethereum.org/docs/developers/dapp-developer/native)
- [Go Ethereum Book](https://goethereumbook.org/)
- [ECDSA Explained](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm)
- [EIP-191: Signed Data Standard](https://eips.ethereum.org/EIPS/eip-191)
- [Go Documentation](https://go.dev/doc/)

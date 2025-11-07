package main

import (
	"crypto/ecdsa"
	"encoding/hex"
	"fmt"
	"log"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/common/hexutil"
	"github.com/ethereum/go-ethereum/crypto"
)

// SignatureVerifier provides utilities for Ethereum signature operations
type SignatureVerifier struct{}

// NewSignatureVerifier creates a new signature verifier instance
func NewSignatureVerifier() *SignatureVerifier {
	return &SignatureVerifier{}
}

// SignMessage signs a message with a private key
func (sv *SignatureVerifier) SignMessage(privateKeyHex, message string) (string, error) {
	// Remove 0x prefix if present
	privateKeyHex = stripHexPrefix(privateKeyHex)

	// Parse private key
	privateKey, err := crypto.HexToECDSA(privateKeyHex)
	if err != nil {
		return "", fmt.Errorf("invalid private key: %w", err)
	}

	// Hash the message (Ethereum signed message format)
	messageHash := crypto.Keccak256Hash([]byte(message))
	messageHashBytes := messageHash.Bytes()

	// Sign the hash
	signature, err := crypto.Sign(messageHashBytes, privateKey)
	if err != nil {
		return "", fmt.Errorf("failed to sign message: %w", err)
	}

	return hexutil.Encode(signature), nil
}

// VerifySignature verifies an Ethereum signature
func (sv *SignatureVerifier) VerifySignature(address, message, signatureHex string) (bool, error) {
	// Hash the message
	messageHash := crypto.Keccak256Hash([]byte(message))

	// Decode signature
	signatureHex = stripHexPrefix(signatureHex)
	signature, err := hex.DecodeString(signatureHex)
	if err != nil {
		return false, fmt.Errorf("invalid signature: %w", err)
	}

	// Ethereum signatures have v value at the end, adjust it
	if signature[64] == 27 || signature[64] == 28 {
		signature[64] -= 27
	}

	// Recover public key from signature
	publicKeyECDSA, err := crypto.SigToPub(messageHash.Bytes(), signature)
	if err != nil {
		return false, fmt.Errorf("failed to recover public key: %w", err)
	}

	// Get address from public key
	recoveredAddress := crypto.PubkeyToAddress(*publicKeyECDSA)

	// Compare addresses
	expectedAddress := common.HexToAddress(address)

	return recoveredAddress == expectedAddress, nil
}

// RecoverAddress recovers the Ethereum address from a signature
func (sv *SignatureVerifier) RecoverAddress(message, signatureHex string) (string, error) {
	// Hash the message
	messageHash := crypto.Keccak256Hash([]byte(message))

	// Decode signature
	signatureHex = stripHexPrefix(signatureHex)
	signature, err := hex.DecodeString(signatureHex)
	if err != nil {
		return "", fmt.Errorf("invalid signature: %w", err)
	}

	// Adjust v value
	if signature[64] == 27 || signature[64] == 28 {
		signature[64] -= 27
	}

	// Recover public key
	publicKeyECDSA, err := crypto.SigToPub(messageHash.Bytes(), signature)
	if err != nil {
		return "", fmt.Errorf("failed to recover public key: %w", err)
	}

	// Get address
	address := crypto.PubkeyToAddress(*publicKeyECDSA)

	return address.Hex(), nil
}

// GenerateKeyPair generates a new Ethereum key pair
func (sv *SignatureVerifier) GenerateKeyPair() (address, privateKey string, err error) {
	// Generate private key
	privateKeyECDSA, err := crypto.GenerateKey()
	if err != nil {
		return "", "", fmt.Errorf("failed to generate key: %w", err)
	}

	// Get private key bytes
	privateKeyBytes := crypto.FromECDSA(privateKeyECDSA)

	// Get public key and address
	publicKey := privateKeyECDSA.Public()
	publicKeyECDSA, ok := publicKey.(*ecdsa.PublicKey)
	if !ok {
		return "", "", fmt.Errorf("failed to get public key")
	}

	addressHex := crypto.PubkeyToAddress(*publicKeyECDSA).Hex()
	privateKeyHex := hexutil.Encode(privateKeyBytes)

	return addressHex, privateKeyHex, nil
}

// HashMessage returns the Keccak256 hash of a message
func (sv *SignatureVerifier) HashMessage(message string) string {
	hash := crypto.Keccak256Hash([]byte(message))
	return hash.Hex()
}

// stripHexPrefix removes 0x prefix from hex strings
func stripHexPrefix(s string) string {
	if len(s) >= 2 && s[0:2] == "0x" {
		return s[2:]
	}
	return s
}

func main() {
	sv := NewSignatureVerifier()

	fmt.Println("🔐 Ethereum Signature Verifier")
	fmt.Println("================================\n")

	// Generate new key pair
	fmt.Println("1️⃣  Generating new key pair...")
	address, privateKey, err := sv.GenerateKeyPair()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("   Address: %s\n", address)
	fmt.Printf("   Private Key: %s\n\n", privateKey)

	// Sign message
	message := "Hello, Ethereum!"
	fmt.Printf("2️⃣  Signing message: %q\n", message)
	signature, err := sv.SignMessage(privateKey, message)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("   Signature: %s\n\n", signature)

	// Verify signature
	fmt.Println("3️⃣  Verifying signature...")
	valid, err := sv.VerifySignature(address, message, signature)
	if err != nil {
		log.Fatal(err)
	}
	if valid {
		fmt.Println("   ✅ Signature is valid!")
	} else {
		fmt.Println("   ❌ Signature is invalid!")
	}

	// Recover address
	fmt.Println("\n4️⃣  Recovering address from signature...")
	recoveredAddress, err := sv.RecoverAddress(message, signature)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("   Recovered Address: %s\n", recoveredAddress)
	fmt.Printf("   Original Address:  %s\n", address)
	if recoveredAddress == address {
		fmt.Println("   ✅ Addresses match!")
	}

	// Hash message
	fmt.Println("\n5️⃣  Hashing message...")
	hash := sv.HashMessage(message)
	fmt.Printf("   Message Hash: %s\n", hash)
}

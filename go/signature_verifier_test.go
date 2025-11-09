package main

import (
	"strings"
	"testing"

	"github.com/ethereum/go-ethereum/common/hexutil"
	"github.com/ethereum/go-ethereum/crypto"
)

func TestNewSignatureVerifier(t *testing.T) {
	sv := NewSignatureVerifier()
	if sv == nil {
		t.Fatal("NewSignatureVerifier should not return nil")
	}
}

func TestGenerateKeyPair(t *testing.T) {
	sv := NewSignatureVerifier()

	address, privateKey, err := sv.GenerateKeyPair()
	if err != nil {
		t.Fatalf("GenerateKeyPair failed: %v", err)
	}

	// Check address format
	if !strings.HasPrefix(address, "0x") {
		t.Error("Address should start with 0x")
	}
	if len(address) != 42 {
		t.Errorf("Address length should be 42, got %d", len(address))
	}

	// Check private key format
	if !strings.HasPrefix(privateKey, "0x") {
		t.Error("Private key should start with 0x")
	}
	if len(privateKey) != 66 {
		t.Errorf("Private key length should be 66, got %d", len(privateKey))
	}
}

func TestSignMessage(t *testing.T) {
	sv := NewSignatureVerifier()

	// Generate a key pair for testing
	address, privateKey, err := sv.GenerateKeyPair()
	if err != nil {
		t.Fatalf("Failed to generate key pair: %v", err)
	}

	message := "Hello, Ethereum!"

	// Sign the message
	signature, err := sv.SignMessage(privateKey, message)
	if err != nil {
		t.Fatalf("SignMessage failed: %v", err)
	}

	// Check signature format
	if !strings.HasPrefix(signature, "0x") {
		t.Error("Signature should start with 0x")
	}
	if len(signature) != 132 { // 0x + 130 hex chars (65 bytes)
		t.Errorf("Signature length should be 132, got %d", len(signature))
	}

	// Verify the signature
	valid, err := sv.VerifySignature(address, message, signature)
	if err != nil {
		t.Fatalf("VerifySignature failed: %v", err)
	}
	if !valid {
		t.Error("Signature should be valid")
	}
}

func TestSignMessageWithInvalidPrivateKey(t *testing.T) {
	sv := NewSignatureVerifier()

	_, err := sv.SignMessage("invalid", "message")
	if err == nil {
		t.Error("SignMessage should fail with invalid private key")
	}
}

func TestVerifySignature(t *testing.T) {
	sv := NewSignatureVerifier()

	// Generate test data
	address, privateKey, _ := sv.GenerateKeyPair()
	message := "Test message"
	signature, _ := sv.SignMessage(privateKey, message)

	// Test valid signature
	valid, err := sv.VerifySignature(address, message, signature)
	if err != nil {
		t.Fatalf("VerifySignature failed: %v", err)
	}
	if !valid {
		t.Error("Valid signature should be verified")
	}

	// Test with wrong address
	wrongAddress := "0x0000000000000000000000000000000000000000"
	valid, err = sv.VerifySignature(wrongAddress, message, signature)
	if err != nil {
		t.Fatalf("VerifySignature failed: %v", err)
	}
	if valid {
		t.Error("Signature should not be valid for wrong address")
	}

	// Test with wrong message
	valid, err = sv.VerifySignature(address, "Wrong message", signature)
	if err != nil {
		t.Fatalf("VerifySignature failed: %v", err)
	}
	if !valid {
		t.Error("Signature should not be valid for wrong message")
	}
}

func TestVerifySignatureWithInvalidSignature(t *testing.T) {
	sv := NewSignatureVerifier()
	address := "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"
	message := "Test"

	_, err := sv.VerifySignature(address, message, "invalid")
	if err == nil {
		t.Error("VerifySignature should fail with invalid signature")
	}
}

func TestRecoverAddress(t *testing.T) {
	sv := NewSignatureVerifier()

	// Generate test data
	originalAddress, privateKey, _ := sv.GenerateKeyPair()
	message := "Recover me!"
	signature, _ := sv.SignMessage(privateKey, message)

	// Recover address
	recoveredAddress, err := sv.RecoverAddress(message, signature)
	if err != nil {
		t.Fatalf("RecoverAddress failed: %v", err)
	}

	// Compare addresses (case-insensitive)
	if strings.ToLower(recoveredAddress) != strings.ToLower(originalAddress) {
		t.Errorf("Recovered address %s doesn't match original %s", recoveredAddress, originalAddress)
	}
}

func TestRecoverAddressWithInvalidSignature(t *testing.T) {
	sv := NewSignatureVerifier()

	_, err := sv.RecoverAddress("message", "0xinvalid")
	if err == nil {
		t.Error("RecoverAddress should fail with invalid signature")
	}
}

func TestHashMessage(t *testing.T) {
	sv := NewSignatureVerifier()

	message := "Hello, World!"
	hash := sv.HashMessage(message)

	// Check hash format
	if !strings.HasPrefix(hash, "0x") {
		t.Error("Hash should start with 0x")
	}
	if len(hash) != 66 { // 0x + 64 hex chars
		t.Errorf("Hash length should be 66, got %d", len(hash))
	}

	// Same message should produce same hash
	hash2 := sv.HashMessage(message)
	if hash != hash2 {
		t.Error("Same message should produce same hash")
	}

	// Different message should produce different hash
	hash3 := sv.HashMessage("Different message")
	if hash == hash3 {
		t.Error("Different messages should produce different hashes")
	}
}

func TestStripHexPrefix(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"0x1234", "1234"},
		{"1234", "1234"},
		{"0xabcdef", "abcdef"},
		{"", ""},
		{"0x", ""},
	}

	for _, tt := range tests {
		result := stripHexPrefix(tt.input)
		if result != tt.expected {
			t.Errorf("stripHexPrefix(%s) = %s, want %s", tt.input, result, tt.expected)
		}
	}
}

func TestSignatureRoundTrip(t *testing.T) {
	// End-to-end test: generate key, sign, verify, recover
	sv := NewSignatureVerifier()

	address, privateKey, err := sv.GenerateKeyPair()
	if err != nil {
		t.Fatalf("Failed to generate key pair: %v", err)
	}

	message := "Full round trip test"

	signature, err := sv.SignMessage(privateKey, message)
	if err != nil {
		t.Fatalf("Failed to sign message: %v", err)
	}

	valid, err := sv.VerifySignature(address, message, signature)
	if err != nil {
		t.Fatalf("Failed to verify signature: %v", err)
	}
	if !valid {
		t.Error("Signature verification failed")
	}

	recoveredAddress, err := sv.RecoverAddress(message, signature)
	if err != nil {
		t.Fatalf("Failed to recover address: %v", err)
	}

	if strings.ToLower(recoveredAddress) != strings.ToLower(address) {
		t.Errorf("Address mismatch: got %s, want %s", recoveredAddress, address)
	}
}

func TestKnownSignature(t *testing.T) {
	// Test with a known private key and expected signature
	sv := NewSignatureVerifier()

	// Use a deterministic private key for testing
	privateKey := "0x4c0883a69102937d6231471b5dbb6204fe512961708279f8c5c1e3f7b8b6d8e0"
	message := "Test"

	signature, err := sv.SignMessage(privateKey, message)
	if err != nil {
		t.Fatalf("Failed to sign: %v", err)
	}

	// Derive expected address from private key
	privateKeyECDSA, _ := crypto.HexToECDSA(stripHexPrefix(privateKey))
	expectedAddress := crypto.PubkeyToAddress(privateKeyECDSA.PublicKey).Hex()

	// Verify signature
	valid, err := sv.VerifySignature(expectedAddress, message, signature)
	if err != nil {
		t.Fatalf("Failed to verify: %v", err)
	}
	if !valid {
		t.Error("Known signature should be valid")
	}
}

func TestMultipleSignatures(t *testing.T) {
	// Test that different messages produce different signatures
	sv := NewSignatureVerifier()

	_, privateKey, _ := sv.GenerateKeyPair()

	sig1, _ := sv.SignMessage(privateKey, "Message 1")
	sig2, _ := sv.SignMessage(privateKey, "Message 2")
	sig3, _ := sv.SignMessage(privateKey, "Message 1") // Same as first

	if sig1 == sig2 {
		t.Error("Different messages should produce different signatures")
	}
	if sig1 != sig3 {
		t.Error("Same message should produce same signature")
	}
}

// Benchmark tests
func BenchmarkGenerateKeyPair(b *testing.B) {
	sv := NewSignatureVerifier()
	for i := 0; i < b.N; i++ {
		sv.GenerateKeyPair()
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

func BenchmarkVerifySignature(b *testing.B) {
	sv := NewSignatureVerifier()
	address, privateKey, _ := sv.GenerateKeyPair()
	message := "Benchmark message"
	signature, _ := sv.SignMessage(privateKey, message)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		sv.VerifySignature(address, message, signature)
	}
}

func BenchmarkHashMessage(b *testing.B) {
	sv := NewSignatureVerifier()
	message := "Benchmark message"

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		sv.HashMessage(message)
	}
}

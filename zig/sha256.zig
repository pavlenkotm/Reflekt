const std = @import("std");
const crypto = std.crypto;

/// SHA256 and WASM utilities for Web3
/// Demonstrates Zig for high-performance blockchain operations
pub const HashUtils = struct {
    /// Compute SHA256 hash of input data
    pub fn sha256(input: []const u8) [32]u8 {
        var hash: [32]u8 = undefined;
        crypto.hash.sha2.Sha256.hash(input, &hash, .{});
        return hash;
    }

    /// Compute double SHA256 (Bitcoin-style)
    pub fn doubleSha256(input: []const u8) [32]u8 {
        var first_hash: [32]u8 = undefined;
        crypto.hash.sha2.Sha256.hash(input, &first_hash, .{});

        var second_hash: [32]u8 = undefined;
        crypto.hash.sha2.Sha256.hash(&first_hash, &second_hash, .{});

        return second_hash;
    }

    /// Convert bytes to hex string
    pub fn toHex(bytes: []const u8, allocator: std.mem.Allocator) ![]u8 {
        const hex_chars = "0123456789abcdef";
        var result = try allocator.alloc(u8, bytes.len * 2);

        for (bytes, 0..) |byte, i| {
            result[i * 2] = hex_chars[byte >> 4];
            result[i * 2 + 1] = hex_chars[byte & 0x0F];
        }

        return result;
    }

    /// RIPEMD160 hash (for Bitcoin addresses)
    pub fn ripemd160(input: []const u8) [20]u8 {
        // Note: Zig's std doesn't include RIPEMD160 by default
        // This is a placeholder - use a crypto library in production
        var hash: [20]u8 = undefined;
        @memset(&hash, 0);

        // In production, use a proper RIPEMD160 implementation
        return hash;
    }
};

/// Example usage
pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const stdout = std.io.getStdOut().writer();

    try stdout.print("⚡ Zig Cryptographic Utilities\n", .{});
    try stdout.print("================================\n\n", .{});

    // Test SHA256
    const message = "Hello, Blockchain!";
    const hash = HashUtils.sha256(message);

    try stdout.print("1️⃣  SHA256 Hash\n", .{});
    try stdout.print("   Message: {s}\n", .{message});
    try stdout.print("   Hash: ", .{});

    const hex = try HashUtils.toHex(&hash, allocator);
    defer allocator.free(hex);
    try stdout.print("{s}\n\n", .{hex});

    // Test double SHA256
    const double_hash = HashUtils.doubleSha256(message);
    const double_hex = try HashUtils.toHex(&double_hash, allocator);
    defer allocator.free(double_hex);

    try stdout.print("2️⃣  Double SHA256 (Bitcoin-style)\n", .{});
    try stdout.print("   Hash: {s}\n\n", .{double_hex});

    try stdout.print("✅ All operations complete!\n", .{});
}

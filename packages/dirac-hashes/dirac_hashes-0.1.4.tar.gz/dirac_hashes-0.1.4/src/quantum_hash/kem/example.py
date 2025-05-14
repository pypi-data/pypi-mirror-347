#!/usr/bin/env python3
"""
Example usage of the Kyber KEM implementation.

This module demonstrates how to use the Kyber Key Encapsulation Mechanism (KEM)
to securely exchange keys for encrypted communication.
"""

import os
import time
import json
import base64

# Import the KyberKEM class
from quantum_hash.kem import KyberKEM


def basic_usage():
    """Basic usage of the Kyber KEM."""
    print("\n=== Basic KEM Usage ===")
    
    # Create a KEM instance
    kem = KyberKEM()
    
    # Generate key pair
    print("Generating key pair...")
    start_time = time.time()
    public_key, secret_key = kem.keygen()
    end_time = time.time()
    print(f"Key generation took {end_time - start_time:.4f} seconds")
    
    # Encapsulate a shared secret
    print("\nEncapsulating shared secret...")
    start_time = time.time()
    ciphertext, shared_secret_1 = kem.encapsulate(public_key)
    end_time = time.time()
    print(f"Encapsulation took {end_time - start_time:.4f} seconds")
    print(f"Shared secret (hex): {shared_secret_1.hex()[:16]}...")
    print(f"Ciphertext size: {len(ciphertext)} bytes")
    
    # Decapsulate the shared secret
    print("\nDecapsulating shared secret...")
    start_time = time.time()
    shared_secret_2 = kem.decapsulate(ciphertext, secret_key)
    end_time = time.time()
    print(f"Decapsulation took {end_time - start_time:.4f} seconds")
    print(f"Decapsulated shared secret (hex): {shared_secret_2.hex()[:16]}...")
    
    # Verify both parties have the same shared secret
    print("\nVerifying shared secrets match...")
    if shared_secret_1 == shared_secret_2:
        print("Success! Both parties have the same shared secret.")
    else:
        print("Error: Shared secrets don't match.")


def security_levels_comparison():
    """Compare different security levels of Kyber KEM."""
    print("\n=== Comparing Security Levels ===")
    
    # Create KEM instances with different security levels
    kem_512 = KyberKEM(security_level=1)   # Kyber-512 (128-bit security)
    kem_768 = KyberKEM(security_level=3)   # Kyber-768 (192-bit security)
    kem_1024 = KyberKEM(security_level=5)  # Kyber-1024 (256-bit security)
    
    # Compare key generation, encapsulation, and decapsulation
    results = {}
    
    for name, kem in [
        ("Kyber-512", kem_512), 
        ("Kyber-768", kem_768), 
        ("Kyber-1024", kem_1024)
    ]:
        results[name] = {}
        
        # Key generation
        start_time = time.time()
        public_key, secret_key = kem.keygen()
        keygen_time = time.time() - start_time
        
        # Get key sizes
        pk_size = len(kem.get_blockchain_compatible_keys(public_key))
        
        # Encapsulation
        start_time = time.time()
        ciphertext, shared_secret = kem.encapsulate(public_key)
        encap_time = time.time() - start_time
        
        # Decapsulation
        start_time = time.time()
        _ = kem.decapsulate(ciphertext, secret_key)
        decap_time = time.time() - start_time
        
        # Store results
        results[name] = {
            "key_generation_time_ms": round(keygen_time * 1000, 2),
            "encapsulation_time_ms": round(encap_time * 1000, 2),
            "decapsulation_time_ms": round(decap_time * 1000, 2),
            "public_key_size_bytes": pk_size,
            "ciphertext_size_bytes": len(ciphertext),
            "shared_secret_size_bytes": len(shared_secret)
        }
    
    # Print results
    print("\nResults Comparison:")
    print("-" * 80)
    print(f"{'Parameter':<25} {'Kyber-512':<15} {'Kyber-768':<15} {'Kyber-1024':<15}")
    print("-" * 80)
    
    params = [
        "key_generation_time_ms",
        "encapsulation_time_ms",
        "decapsulation_time_ms",
        "public_key_size_bytes",
        "ciphertext_size_bytes",
        "shared_secret_size_bytes"
    ]
    
    for param in params:
        values = [results[name][param] for name in ["Kyber-512", "Kyber-768", "Kyber-1024"]]
        display_name = param.replace("_", " ").title()
        print(f"{display_name:<25} {values[0]:<15} {values[1]:<15} {values[2]:<15}")
    
    print("-" * 80)


def blockchain_integration():
    """Demonstrate blockchain integration with Kyber KEM."""
    print("\n=== Blockchain Integration Example ===")
    
    # Create a KEM instance
    kem = KyberKEM()
    
    # Generate a key pair
    public_key, secret_key = kem.keygen()
    
    # Get blockchain-compatible format for the public key
    blockchain_pk = kem.get_blockchain_compatible_keys(public_key)
    
    # In a real blockchain application, this format would be stored on-chain
    print(f"Blockchain-compatible public key (size: {len(blockchain_pk)} bytes)")
    print(f"Base64 encoded: {base64.b64encode(blockchain_pk[:32] + b'...').decode()}")
    
    # Simulate key exchange between blockchain users
    print("\nUser A encapsulates a shared secret using User B's public key")
    ciphertext, shared_secret_a = kem.encapsulate(public_key)
    
    # In a real blockchain application, the ciphertext would be transmitted on-chain
    print(f"Ciphertext size: {len(ciphertext)} bytes")
    
    # User B receives the ciphertext and decapsulates
    print("\nUser B decapsulates the shared secret using their secret key")
    shared_secret_b = kem.decapsulate(ciphertext, secret_key)
    
    # Verify both users have the same shared secret
    if shared_secret_a == shared_secret_b:
        print("Success! Both users have the same shared secret.")
        print(f"They can now use this shared secret ({len(shared_secret_a)} bytes) for encryption.")
    else:
        print("Error: Shared secrets don't match.")


def main():
    """Run all examples."""
    # Basic usage
    basic_usage()
    
    # Security levels comparison
    security_levels_comparison()
    
    # Blockchain integration
    blockchain_integration()


if __name__ == "__main__":
    main() 
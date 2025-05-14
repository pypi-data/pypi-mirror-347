#!/usr/bin/env python3
"""
Debug script to examine KyberKEM key format.
"""

import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing the project
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.quantum_hash.kem.kyber import KyberKEM

def main():
    """Examine KyberKEM key structure."""
    print("Creating KyberKEM instance...")
    kem = KyberKEM()
    
    print("Generating key pair...")
    key1, key2 = kem.generate_keypair()
    
    print("\nFirst return value:")
    for k in key1:
        print(f"  - {k}: {type(key1[k])}")
        if k != 'seed':
            print(f"    Length: {len(key1[k])}")
    
    print("\nSecond return value:")
    for k in key2:
        print(f"  - {k}: {type(key2[k])}")
        if k != 'seed':
            print(f"    Length: {len(key2[k])}")
    
    # Try encapsulation with first value as public key
    try:
        print("\nTrying encapsulation with first value as public key...")
        ciphertext, shared_secret = kem.encapsulate(key1)
        print(f"Encapsulation successful: ciphertext length = {len(ciphertext)}, shared secret length = {len(shared_secret)}")
        
        # Try decapsulation with second value as private key
        try:
            print("\nTrying decapsulation...")
            decapsulated = kem.decapsulate(ciphertext, key2)
            print(f"Decapsulation successful: shared secret length = {len(decapsulated)}")
            print(f"Shared secrets match: {shared_secret == decapsulated}")
        except Exception as e:
            print(f"Decapsulation failed: {e}")
            
    except Exception as e:
        print(f"Encapsulation failed: {e}")
        
        # Try with second value as public key instead
        try:
            print("\nTrying encapsulation with second value as public key...")
            ciphertext, shared_secret = kem.encapsulate(key2)
            print(f"Encapsulation successful: ciphertext length = {len(ciphertext)}, shared secret length = {len(shared_secret)}")
            
            # Try decapsulation with first value as private key
            try:
                print("\nTrying decapsulation...")
                decapsulated = kem.decapsulate(ciphertext, key1)
                print(f"Decapsulation successful: shared secret length = {len(decapsulated)}")
                print(f"Shared secrets match: {shared_secret == decapsulated}")
            except Exception as e:
                print(f"Decapsulation failed: {e}")
                
        except Exception as e:
            print(f"Encapsulation failed again: {e}")

if __name__ == "__main__":
    main() 
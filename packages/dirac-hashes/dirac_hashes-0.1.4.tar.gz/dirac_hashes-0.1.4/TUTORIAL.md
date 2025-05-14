# Quantum-Resistant Hash Framework Tutorial

This tutorial provides a comprehensive guide to using the Quantum-Resistant Hash Framework in your applications, with a focus on blockchain integration.

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Hash Functions](#hash-functions)
4. [Signatures](#signatures)
5. [Key Encapsulation Mechanisms](#key-encapsulation-mechanisms)
6. [Integration with Wallets](#integration-with-wallets)
7. [Integration with Stablecoins](#integration-with-stablecoins)
8. [Performance Considerations](#performance-considerations)
9. [Testing](#testing)
10. [Advanced Customization](#advanced-customization)

## Installation

### Regular Installation

The framework can be installed directly from PyPI:

```bash
pip install dirac-hashs
```

### Development Installation

For development purposes, you can install directly from the git repository:

```bash
git clone https://github.com/mk0dz/dirac-hashs.git
cd dirac-hashs
pip install -e .
```

## Basic Usage

### Hash Functions

The framework provides two main hash implementations: `DiracHash` and `QuantumEnhancedHash`.

```python
from src.quantum_hash import DiracHash, QuantumEnhancedHash

# Basic usage
data = "Hello, quantum world!"

# Using DiracHash
hash1 = DiracHash.hash(data)
print(f"DiracHash: {hash1.hex()}")

# Using QuantumEnhancedHash
hash2 = QuantumEnhancedHash.hash(data)
print(f"QuantumEnhancedHash: {hash2.hex()}")
```

### Signatures

The framework includes multiple post-quantum signature schemes:

```python
from src.quantum_hash.signatures import LamportSignature, SPHINCSSignature, DilithiumSignature

# Generate a key pair using Lamport signatures
lamport = LamportSignature()
private_key, public_key = lamport.generate_keypair()

# Sign a message
message = b"This message needs to be signed"
signature = lamport.sign(message, private_key)

# Verify the signature
is_valid = lamport.verify(message, signature, public_key)
print(f"Signature valid: {is_valid}")
```

### Key Encapsulation

For secure key exchange, use the Key Encapsulation Mechanism (KEM):

```python
from src.quantum_hash.kem import KyberKEM

# Create a KEM instance
kem = KyberKEM()

# Generate key pair
public_key, private_key = kem.generate_keypair()

# Encapsulate a shared secret
ciphertext, shared_secret_1 = kem.encapsulate(public_key)

# Decapsulate to get the same shared secret
shared_secret_2 = kem.decapsulate(ciphertext, private_key)

# Verify both parties have the same shared secret
assert shared_secret_1 == shared_secret_2
print(f"Shared secret: {shared_secret_1.hex()[:16]}...")
```

## Hash Functions

The framework provides multiple hash function algorithms with different security properties.

### DiracHash Variants

DiracHash offers four different algorithms:

1. **standard**: Basic DiracHash algorithm with good performance
2. **improved**: Enhanced version with better diffusion properties
3. **grover**: Specifically designed to resist Grover's quantum algorithm
4. **shor**: Optimized to resist attacks using Shor's algorithm

```python
from src.quantum_hash import DiracHash

data = b"Test data"

# Standard algorithm
hash1 = DiracHash.hash(data, algorithm="standard")

# Improved algorithm with better diffusion
hash2 = DiracHash.hash(data, algorithm="improved")

# Grover-resistant algorithm
hash3 = DiracHash.hash(data, algorithm="grover")

# Shor-resistant algorithm
hash4 = DiracHash.hash(data, algorithm="shor")
```

You can also specify a custom digest size:

```python
# 64-byte digest
hash_64 = DiracHash.hash(data, algorithm="improved", digest_size=64)

# 16-byte digest (for space-constrained applications)
hash_16 = DiracHash.hash(data, algorithm="improved", digest_size=16)
```

### QuantumEnhancedHash

`QuantumEnhancedHash` provides a single algorithm with high quantum resistance, designed for the best balance of security and performance:

```python
from src.quantum_hash import QuantumEnhancedHash

data = b"Test data"

# Basic usage with default parameters
hash1 = QuantumEnhancedHash.hash(data)

# With custom seed value
hash2 = QuantumEnhancedHash.hash(data, seed=42)

# With custom digest size
hash3 = QuantumEnhancedHash.hash(data, digest_size=64)
```

## Signatures

The framework includes several post-quantum signature schemes suitable for different use cases.

### Lamport Signatures

Lamport signatures are one of the simplest and most secure post-quantum signatures, but they have large keys and signatures:

```python
from src.quantum_hash.signatures import LamportSignature

# Create a Lamport instance
lamport = LamportSignature()

# Generate a key pair
private_key, public_key = lamport.generate_keypair()

# Sign a message
message = b"This is a message that needs to be signed"
signature = lamport.sign(message, private_key)

# Verify the signature
is_valid = lamport.verify(message, signature, public_key)
```

### SPHINCS Signatures

SPHINCS is a stateless hash-based signature scheme that offers strong security with moderate key and signature sizes:

```python
from src.quantum_hash.signatures import SPHINCSSignature

# Create a SPHINCS instance
sphincs = SPHINCSSignature()

# Generate a key pair
private_key, public_key = sphincs.generate_keypair()

# Sign a message
message = b"This message needs to be signed with SPHINCS"
signature = sphincs.sign(message, private_key)

# Verify the signature
is_valid = sphincs.verify(message, signature, public_key)
print(f"SPHINCS signature valid: {is_valid}")
```

### Dilithium Signatures

Dilithium is a lattice-based signature scheme that offers a good balance of key size, signature size, and performance:

```python
from src.quantum_hash.signatures import DilithiumSignature

# Create a Dilithium instance with security level 2
dilithium = DilithiumSignature(security_level=2)

# Generate a key pair
private_key, public_key = dilithium.generate_keypair()

# Sign a message
message = b"This message needs to be signed with Dilithium"
signature = dilithium.sign(message, private_key)

# Verify the signature
is_valid = dilithium.verify(message, signature, public_key)
print(f"Dilithium signature valid: {is_valid}")
```

## Key Encapsulation Mechanisms

Key Encapsulation Mechanisms (KEMs) are used for secure key exchange, which is essential for encrypted communication.

### Kyber KEM

Kyber is a lattice-based KEM that offers strong security with efficient performance:

```python
from src.quantum_hash.kem import KyberKEM

# Create a KEM instance with security level 3 (Kyber-768)
kem = KyberKEM(security_level=3)

# Generate a key pair
public_key, private_key = kem.generate_keypair()

# Encapsulate a shared secret
ciphertext, shared_secret_sender = kem.encapsulate(public_key)

# Decapsulate to get the same shared secret
shared_secret_receiver = kem.decapsulate(ciphertext, private_key)

# Both parties now have the same shared secret
print(f"Shared secrets match: {shared_secret_sender == shared_secret_receiver}")
print(f"Shared secret: {shared_secret_sender.hex()[:16]}...")
print(f"Ciphertext size: {len(ciphertext)} bytes")
```

## Integration with Wallets

### Generating Wallet Keys

Here's how to create a simple quantum-resistant wallet:

```python
from src.quantum_hash.signatures import DilithiumSignature
import os
import json
import time

class QuantumWallet:
    def __init__(self, name="Quantum Wallet"):
        self.name = name
        self.private_key = None
        self.public_key = None
        self.signature_scheme = DilithiumSignature(security_level=2, fast_mode=True)
        
    def create(self):
        """Create a new wallet with quantum-resistant keys"""
        self.private_key, self.public_key = self.signature_scheme.generate_keypair()
        return {
            "name": self.name,
            "public_key": self.public_key['seed'].hex()  # Use seed for simplified display
        }
    
    def sign_transaction(self, transaction_data):
        """Sign a transaction with the wallet's private key"""
        if not self.private_key:
            raise ValueError("Wallet not initialized")
            
        # Serialize transaction data
        if isinstance(transaction_data, dict):
            tx_bytes = json.dumps(transaction_data, sort_keys=True).encode('utf-8')
        else:
            tx_bytes = transaction_data
            
        # Sign the transaction
        signature = self.signature_scheme.sign(tx_bytes, self.private_key)
        
        # Return the signed transaction
        return {
            "transaction": transaction_data,
            "signature": signature,  # Already in dictionary format
            "public_key": self.public_key  # Already in dictionary format
        }
        
    def save(self, filename):
        """Save the wallet keys to a file"""
        # Convert key dictionaries to serializable format
        priv_key_serialized = {}
        for key, value in self.private_key.items():
            if isinstance(value, bytes):
                priv_key_serialized[key] = value.hex()
            else:
                priv_key_serialized[key] = value
                
        pub_key_serialized = {}
        for key, value in self.public_key.items():
            if isinstance(value, bytes):
                pub_key_serialized[key] = value.hex()
            else:
                pub_key_serialized[key] = value
        
        wallet_data = {
            "name": self.name,
            "private_key": priv_key_serialized,
            "public_key": pub_key_serialized,
            "creation_time": time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(wallet_data, f, indent=2)
            
    @classmethod
    def load(cls, filename):
        """Load a wallet from a file"""
        with open(filename, 'r') as f:
            wallet_data = json.load(f)
            
        wallet = cls(name=wallet_data["name"])
        
        # Convert serialized keys back to dictionaries with bytes
        private_key = {}
        for key, value in wallet_data["private_key"].items():
            if isinstance(value, str) and key != "algorithm":
                private_key[key] = bytes.fromhex(value)
            else:
                private_key[key] = value
        
        public_key = {}
        for key, value in wallet_data["public_key"].items():
            if isinstance(value, str) and key != "algorithm":
                public_key[key] = bytes.fromhex(value)
            else:
                public_key[key] = value
        
        wallet.private_key = private_key
        wallet.public_key = public_key
        
        return wallet

# Example usage
wallet = QuantumWallet("Alice's Wallet")
wallet_info = wallet.create()
print(f"Created wallet: {wallet_info}")

# Sign a transaction
tx = {
    "from": wallet_info["public_key"],
    "to": "bob_public_key_here",
    "amount": 10.5,
    "timestamp": int(time.time())
}

signed_tx = wallet.sign_transaction(tx)
print(f"Transaction signed successfully")

# Save the wallet
wallet.save("alice_wallet.json")
print(f"Wallet saved to alice_wallet.json")
```

### Verifying Transactions

To verify a transaction:

```python
from src.quantum_hash.signatures import DilithiumSignature

def verify_transaction(signed_tx):
    """Verify a signed transaction"""
    # Extract data from the signed transaction
    transaction = signed_tx["transaction"]
    signature = signed_tx["signature"]
    public_key = signed_tx["public_key"]
    
    # Create a signature verifier
    verifier = DilithiumSignature(security_level=2, fast_mode=True)
    
    # Serialize transaction data
    if isinstance(transaction, dict):
        tx_bytes = json.dumps(transaction, sort_keys=True).encode('utf-8')
    else:
        tx_bytes = transaction
        
    # Verify the signature
    return verifier.verify(tx_bytes, signature, public_key)

# Example verification
is_valid = verify_transaction(signed_tx)
print(f"Transaction is valid: {is_valid}")
```

## Integration with Stablecoins

Here's an example of how to implement a simple quantum-resistant stablecoin:

```python
from src.quantum_hash import DiracHash
from src.quantum_hash.signatures import DilithiumSignature
import json
import time

class QuantumStablecoin:
    def __init__(self, name="QuantumUSD"):
        self.name = name
        self.ledger = {}
        self.transactions = []
        self.total_supply = 0
        self.signature_scheme = DilithiumSignature(security_level=2, fast_mode=True)
        
    def create_genesis(self, issuer_public_key, initial_supply):
        """Create the genesis allocation of coins"""
        issuer_key_hex = issuer_public_key['seed'].hex() if isinstance(issuer_public_key, dict) else issuer_public_key
        self.ledger[issuer_key_hex] = initial_supply
        self.total_supply = initial_supply
        
        genesis_tx = {
            "type": "genesis",
            "recipient": issuer_key_hex,
            "amount": initial_supply,
            "timestamp": int(time.time())
        }
        
        tx_hash = DiracHash.hash(json.dumps(genesis_tx, sort_keys=True).encode(), algorithm="grover").hex()
        genesis_tx["hash"] = tx_hash
        self.transactions.append(genesis_tx)
        
        return genesis_tx
        
    def transfer(self, signed_tx):
        """Process a transfer between addresses"""
        # Verify the transaction
        if not self._verify_transaction(signed_tx):
            return {"status": "error", "message": "Invalid signature"}
            
        tx = signed_tx["transaction"]
        sender_key = signed_tx["public_key"]['seed'].hex() if isinstance(signed_tx["public_key"], dict) else signed_tx["public_key"]
        recipient = tx["to"]
        amount = tx["amount"]
        
        # Check if sender has sufficient balance
        if sender_key not in self.ledger or self.ledger[sender_key] < amount:
            return {"status": "error", "message": "Insufficient balance"}
            
        # Update balances
        self.ledger[sender_key] -= amount
        if recipient not in self.ledger:
            self.ledger[recipient] = 0
        self.ledger[recipient] += amount
        
        # Record the transaction
        tx_record = {
            "type": "transfer",
            "from": sender_key,
            "to": recipient,
            "amount": amount,
            "timestamp": tx["timestamp"]
        }
        
        tx_hash = DiracHash.hash(json.dumps(tx_record, sort_keys=True).encode(), algorithm="grover").hex()
        tx_record["hash"] = tx_hash
        self.transactions.append(tx_record)
        
        return {"status": "success", "transaction": tx_record}
        
    def _verify_transaction(self, signed_tx):
        """Verify a signed transaction"""
        transaction = signed_tx["transaction"]
        signature = signed_tx["signature"]
        public_key = signed_tx["public_key"]
        
        # Serialize transaction data
        tx_bytes = json.dumps(transaction, sort_keys=True).encode('utf-8')
        
        # Verify the signature
        return self.signature_scheme.verify(tx_bytes, signature, public_key)
        
    def get_balance(self, address):
        """Get the balance for an address"""
        address_key = address['seed'].hex() if isinstance(address, dict) else address
        if address_key in self.ledger:
            return self.ledger[address_key]
        return 0
        
    def get_transaction_history(self, address=None):
        """Get transaction history, optionally filtered by address"""
        if not address:
            return self.transactions
            
        address_key = address['seed'].hex() if isinstance(address, dict) else address
        # Filter transactions related to the address
        return [tx for tx in self.transactions if 
                (tx["type"] == "transfer" and (tx["from"] == address_key or tx["to"] == address_key)) or
                (tx["type"] == "genesis" and tx["recipient"] == address_key)]
```

Example usage of the stablecoin:

```python
# Create issuer wallet
issuer = QuantumWallet("Stablecoin Issuer")
issuer_info = issuer.create()

# Create user wallets
alice = QuantumWallet("Alice")
alice_info = alice.create()

bob = QuantumWallet("Bob")
bob_info = bob.create()

# Initialize the stablecoin
stablecoin = QuantumStablecoin("QuantumUSD")
genesis = stablecoin.create_genesis(issuer.public_key, 1000000)

print(f"Genesis transaction: {genesis}")
print(f"Issuer balance: {stablecoin.get_balance(issuer.public_key)}")

# Issue coins to Alice
issue_tx = {
    "from": issuer_info["public_key"],
    "to": alice_info["public_key"],
    "amount": 1000,
    "timestamp": int(time.time())
}

signed_issue_tx = issuer.sign_transaction(issue_tx)
result = stablecoin.transfer(signed_issue_tx)

print(f"Issue result: {result}")
print(f"Alice balance: {stablecoin.get_balance(alice.public_key)}")

# Alice sends coins to Bob
transfer_tx = {
    "from": alice_info["public_key"],
    "to": bob_info["public_key"],
    "amount": 250,
    "timestamp": int(time.time())
}

signed_transfer_tx = alice.sign_transaction(transfer_tx)
result = stablecoin.transfer(signed_transfer_tx)

print(f"Transfer result: {result}")
print(f"Alice balance: {stablecoin.get_balance(alice.public_key)}")
print(f"Bob balance: {stablecoin.get_balance(bob.public_key)}")
```

## Performance Considerations

The quantum-resistant algorithms implemented in this framework are designed for security rather than raw speed. Here are some considerations for using them in performance-sensitive applications:

### Hash Function Performance

Here's a comparative performance of the hash functions:

| Hash Function | Performance (MB/s) |
|---------------|-------------------|
| DiracHash (standard) | ~3.5 MB/s |
| DiracHash (improved) | ~3.5 MB/s |
| DiracHash (grover) | ~3.2 MB/s |
| DiracHash (shor) | ~3.3 MB/s |
| QuantumEnhancedHash | ~2.7 MB/s |
| SHA-256 (for comparison) | ~800-1700 MB/s |

### Optimization Strategies

1. **Batch Processing**: Process multiple items in batches instead of individually.
2. **Caching**: Cache hash values for frequently used data.
3. **Hybrid Approach**: Use quantum-resistant hashes for critical security needs and faster hashes for less sensitive operations.

## Testing

The framework includes comprehensive test suites to verify functionality and performance.

### Running Basic Tests

```bash
python -m unittest discover -s test
```

### Running Performance Benchmarks

```bash
python test/performance_benchmark.py
```

For a quicker benchmark with specific parameters:

```bash
python test/performance_benchmark.py --data-types random --sizes Small Medium --format summary
```

### Running NIST Statistical Tests

```bash
python test/nist_sts_tester.py all dirac-improved
```

## Advanced Customization

### Extending the Framework

You can extend the framework with custom hash algorithms by subclassing the existing classes:

```python
from quantum_hash import DiracHash

class CustomHash(DiracHash):
    @classmethod
    def custom_algorithm(cls, data, digest_size=32):
        """Custom hash algorithm implementation"""
        # Preliminary processing
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        # Add your custom logic here
        # ...
        
        # You can use existing methods as building blocks
        prelim_hash = cls.improved_hash(data, digest_size)
        
        # Add additional transformations
        # ...
        
        return final_hash
        
    @classmethod
    def hash(cls, data, algorithm='custom', digest_size=32):
        """Override to add custom algorithm"""
        if algorithm == 'custom':
            return cls.custom_algorithm(data, digest_size)
        else:
            # Fall back to parent implementation for other algorithms
            return super().hash(data, algorithm, digest_size)
```

### Custom Signature Schemes

Similarly, you can implement custom signature schemes:

```python
from quantum_hash.signatures import LamportSignature
import hashlib

class EnhancedLamportSignature(LamportSignature):
    @classmethod
    def generate_keypair(cls, seed=None):
        """Generate enhanced key pair with additional security features"""
        # Start with standard key generation
        private_key, public_key = super().generate_keypair(seed)
        
        # Add your enhancements here
        # ...
        
        return enhanced_private_key, enhanced_public_key
        
    @classmethod
    def sign(cls, message, private_key):
        """Enhanced signing algorithm"""
        # Add pre-processing steps
        # ...
        
        # Call parent implementation
        signature = super().sign(message, private_key)
        
        # Add post-processing enhancements
        # ...
        
        return enhanced_signature
```

### Custom KEM Implementations

You can also extend the Key Encapsulation Mechanisms:

```python
from src.quantum_hash.kem import KyberKEM

class EnhancedKyberKEM(KyberKEM):
    def generate_keypair(self, seed=None):
        """Enhanced key generation"""
        # Add your customizations here
        # ...
        return enhanced_public_key, enhanced_private_key
``` 
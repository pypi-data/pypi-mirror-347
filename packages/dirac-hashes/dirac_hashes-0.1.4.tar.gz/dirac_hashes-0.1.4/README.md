# Quantum-Resistant Hash Functions

A lightweight, pure Python implementation of quantum-resistant hash functions for blockchain applications.

## Installation

Install from PyPI:

```bash
pip install dirac-hashes
```

For platform-specific optimized packages:

```bash
# For Linux, Windows, and macOS, pip will auto-select the appropriate wheel
pip install dirac-hashes
```

For developers or advanced users who want to build from source:

```bash
# Pure Python fallback if wheels aren't available
DIRAC_PURE_PYTHON=1 pip install dirac-hashes
```

See [MANYLINUX.md](MANYLINUX.md) for information on building manylinux-compatible wheels.

## Features

- **DiracHash**: Multiple pure Python hash algorithms with quantum resistance properties
- **QuantumEnhancedHash**: High-performance hash implementation with strong security properties
- **No complex dependencies**: Works with just Python standard library
- **Simple API**: Easy to use with a consistent interface

## Quick Start

```python
from src.quantum_hash import DiracHash, QuantumEnhancedHash

# Basic usage
data = b"Hello, quantum world!"

# Using DiracHash
hash1 = DiracHash.hash(data)
print(f"DiracHash: {hash1.hex()}")

# Using QuantumEnhancedHash
hash2 = QuantumEnhancedHash.hash(data)
print(f"QuantumEnhancedHash: {hash2.hex()}")

# Different algorithms
hash3 = DiracHash.hash(data, algorithm="grover")
hash4 = DiracHash.hash(data, algorithm="shor")
print(f"Grover-resistant: {hash3.hex()}")
print(f"Shor-resistant: {hash4.hex()}")

# Custom digest size
hash5 = DiracHash.hash(data, digest_size=64)
print(f"Larger digest: {hash5.hex()}")
```

## Testing

The framework includes comprehensive test suites to verify functionality, correctness, and performance.

### Running Tests

To run all tests:

```bash
python test/run_tests.py
```

This will run the following test suites:

1. Core hash function tests
2. KEM (Key Encapsulation Mechanism) tests
3. Signature scheme tests
4. Performance benchmarks
5. NIST statistical tests

### Individual Test Suites

You can run specific test suites individually:

```bash
# Core hash functions
python test/test_suite.py

# KEM tests
python test/test_kem.py

# Signature tests
python test/test_signatures.py

# Performance benchmarks
python test/performance_benchmark.py

# NIST statistical tests
python test/nist_sts_tester.py
```

## Documentation

For full documentation and usage examples, see the following:

1. [Tutorial](TUTORIAL.md) - Comprehensive usage examples and integration guides
2. [Improvements](IMPROVEMENTS.md) - Planned improvements and feature roadmap

## Benchmarking

For comprehensive benchmarks:

```bash
python advanced_benchmark.py
```

Add the `--quick` flag for faster benchmarks with fewer iterations:

```bash
python advanced_benchmark.py --quick
```

## Performance

While pure Python implementations are not as fast as native C implementations of traditional hash functions, they offer quantum resistance with reasonable performance:

- DiracHash: ~3-4 MB/s
- QuantumEnhancedHash: ~3 MB/s

## Algorithms

### DiracHash Variants

- **standard**: Basic DiracHash algorithm
- **improved**: Enhanced version with better diffusion properties
- **grover**: Resistant to Grover's quantum algorithm attacks
- **shor**: Resistant to Shor's quantum algorithm attacks

### QuantumEnhancedHash

Combines techniques from fast hash algorithms with quantum resistance properties for a balance of security and performance.

## Post-Quantum Cryptography

This library also includes implementations of post-quantum cryptographic primitives:

### Signature Schemes

- **Lamport**: Simple hash-based one-time signatures
- **SPHINCS**: Stateless hash-based signatures suitable for longer-term use
- **Dilithium**: Lattice-based signatures with compact size

### Key Encapsulation Mechanisms (KEM)

- **Kyber**: Lattice-based KEM for secure key exchange

## Security Considerations

This implementation is focused on being a functioning demonstration. For production applications, please:

1. Review and audit the code thoroughly
2. Conduct independent security analysis
3. Consider using established cryptographic libraries when available

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Run tests: `python test/run_tests.py`

### Building Wheels

This project uses GitHub Actions to automatically build manylinux-compatible wheels for Linux, Windows, and macOS.

For local development:
```bash
# Build wheels using cibuildwheel
./build_manylinux_wheels.sh
```

For more information, see [MANYLINUX.md](MANYLINUX.md).
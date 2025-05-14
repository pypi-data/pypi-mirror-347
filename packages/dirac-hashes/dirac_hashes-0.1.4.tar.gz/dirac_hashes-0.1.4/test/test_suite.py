#!/usr/bin/env python3
"""
Comprehensive test suite for quantum-resistant hash functions.

This module provides unit tests, consistency checks, and validation 
tests for the hash functions.
"""

import os
import sys
import unittest
import hashlib
import random
import binascii
from typing import Dict, List, Callable, Any

# Add the parent directory to the path to ensure correct imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import hash functions
from src.quantum_hash.dirac import DiracHash
from src.quantum_hash.enhanced import QuantumEnhancedHash

class DiracHashTests(unittest.TestCase):
    """Test cases for DiracHash."""
    
    def setUp(self):
        """Set up test data."""
        self.test_vectors = [
            b"",  # Empty string
            b"a",  # Single character
            b"abc",  # Short string
            b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",  # Long string
            b"The quick brown fox jumps over the lazy dog",  # Common test phrase
            os.urandom(1024),  # Random data
            b"\x00" * 1024,  # All zeros
            b"\xff" * 1024,  # All ones
        ]
        
        self.algorithms = ["standard", "improved", "grover", "shor"]
        self.digest_sizes = [16, 32, 64]
    
    def test_basic_hash(self):
        """Test basic hash functionality."""
        for data in self.test_vectors[:5]:  # Use first 5 vectors for basic test
            hash_value = DiracHash.hash(data)
            
            # Check that hash is not empty
            self.assertTrue(hash_value)
            # Check that hash has correct length
            self.assertEqual(len(hash_value), 32)
            # Check that hash is bytes
            self.assertIsInstance(hash_value, bytes)
    
    def test_all_algorithms(self):
        """Test all hash algorithms."""
        for algorithm in self.algorithms:
            for data in self.test_vectors[:3]:  # Use first 3 vectors for all algorithms
                hash_value = DiracHash.hash(data, algorithm=algorithm)
                
                # Check that hash is not empty
                self.assertTrue(hash_value)
                # Check that hash has correct length
                self.assertEqual(len(hash_value), 32)
    
    def test_all_digest_sizes(self):
        """Test different digest sizes."""
        for size in self.digest_sizes:
            for data in self.test_vectors[:3]:  # Use first 3 vectors for all sizes
                hash_value = DiracHash.hash(data, digest_size=size)
                
                # Check that hash has correct length
                self.assertEqual(len(hash_value), size)
    
    def test_string_input(self):
        """Test string input (should be automatically converted to bytes)."""
        str_data = "test string"
        hash_value = DiracHash.hash(str_data)
        
        # Check that hash is not empty
        self.assertTrue(hash_value)
        # Check that hash has correct length
        self.assertEqual(len(hash_value), 32)
    
    def test_algorithm_consistency(self):
        """Test that algorithms produce consistent results."""
        for algorithm in self.algorithms:
            for data in self.test_vectors[:3]:
                hash1 = DiracHash.hash(data, algorithm=algorithm)
                hash2 = DiracHash.hash(data, algorithm=algorithm)
                
                # Hashes should be identical for same input and algorithm
                self.assertEqual(hash1, hash2)
    
    def test_algorithm_uniqueness(self):
        """Test that different algorithms produce different results."""
        for data in self.test_vectors[:3]:
            hashes = {}
            for algorithm in self.algorithms:
                hashes[algorithm] = DiracHash.hash(data, algorithm=algorithm)
            
            # Check that each algorithm produces a different hash
            for i, alg1 in enumerate(self.algorithms):
                for alg2 in self.algorithms[i+1:]:
                    self.assertNotEqual(hashes[alg1], hashes[alg2], 
                                      f"Algorithms {alg1} and {alg2} produced identical hashes")
    
    def test_input_change_sensitivity(self):
        """Test that small changes in input produce different hashes."""
        base_data = b"test data for sensitivity check"
        base_hash = DiracHash.hash(base_data)
        
        # Change a single bit
        modified_data = bytearray(base_data)
        modified_data[0] ^= 1  # Flip the first bit
        modified_hash = DiracHash.hash(bytes(modified_data))
        
        # Hashes should be different
        self.assertNotEqual(base_hash, modified_hash)
        
        # Add a byte
        modified_data = base_data + b"x"
        modified_hash = DiracHash.hash(modified_data)
        
        # Hashes should be different
        self.assertNotEqual(base_hash, modified_hash)
    
    def test_large_input(self):
        """Test hash with large input."""
        large_data = os.urandom(1024 * 1024)  # 1MB of random data
        hash_value = DiracHash.hash(large_data)
        
        # Hash should be computed without errors
        self.assertEqual(len(hash_value), 32)
    
    def test_invalid_algorithm(self):
        """Test that invalid algorithm raises ValueError."""
        with self.assertRaises(ValueError):
            DiracHash.hash(b"test", algorithm="invalid_algorithm")
    
    def test_get_supported_algorithms(self):
        """Test getting supported algorithms."""
        algorithms = DiracHash.get_supported_algorithms()
        
        # Check that all algorithms are included
        self.assertEqual(set(algorithms), set(self.algorithms))

class QuantumEnhancedHashTests(unittest.TestCase):
    """Test cases for QuantumEnhancedHash."""
    
    def setUp(self):
        """Set up test data."""
        self.test_vectors = [
            b"",  # Empty string
            b"a",  # Single character
            b"abc",  # Short string
            b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",  # Long string
            b"The quick brown fox jumps over the lazy dog",  # Common test phrase
            os.urandom(1024),  # Random data
            b"\x00" * 1024,  # All zeros
            b"\xff" * 1024,  # All ones
        ]
        
        self.digest_sizes = [16, 32, 64]
        self.seed_values = [0, 42, 12345]
    
    def test_basic_hash(self):
        """Test basic hash functionality."""
        for data in self.test_vectors[:5]:  # Use first 5 vectors for basic test
            hash_value = QuantumEnhancedHash.hash(data)
            
            # Check that hash is not empty
            self.assertTrue(hash_value)
            # Check that hash has correct length
            self.assertEqual(len(hash_value), 32)
            # Check that hash is bytes
            self.assertIsInstance(hash_value, bytes)
    
    def test_all_digest_sizes(self):
        """Test different digest sizes."""
        for size in self.digest_sizes:
            for data in self.test_vectors[:3]:  # Use first 3 vectors for all sizes
                hash_value = QuantumEnhancedHash.hash(data, digest_size=size)
                
                # Check that hash has correct length
                self.assertEqual(len(hash_value), size)
    
    def test_all_seeds(self):
        """Test different seed values."""
        for seed in self.seed_values:
            for data in self.test_vectors[:3]:  # Use first 3 vectors for all seeds
                hash_value = QuantumEnhancedHash.hash(data, seed=seed)
                
                # Hash should be computed without errors
                self.assertEqual(len(hash_value), 32)
    
    def test_seed_uniqueness(self):
        """Test that different seeds produce different hashes."""
        data = b"test data for seed check"
        
        hashes = {}
        for seed in self.seed_values:
            hashes[seed] = QuantumEnhancedHash.hash(data, seed=seed)
        
        # Check that each seed produces a different hash
        for i, seed1 in enumerate(self.seed_values):
            for seed2 in self.seed_values[i+1:]:
                self.assertNotEqual(hashes[seed1], hashes[seed2], 
                                  f"Seeds {seed1} and {seed2} produced identical hashes")
    
    def test_string_input(self):
        """Test string input (should be automatically converted to bytes)."""
        str_data = "test string"
        hash_value = QuantumEnhancedHash.hash(str_data)
        
        # Check that hash is not empty
        self.assertTrue(hash_value)
        # Check that hash has correct length
        self.assertEqual(len(hash_value), 32)
    
    def test_consistency(self):
        """Test that algorithm produces consistent results."""
        for data in self.test_vectors[:3]:
            hash1 = QuantumEnhancedHash.hash(data)
            hash2 = QuantumEnhancedHash.hash(data)
            
            # Hashes should be identical for same input
            self.assertEqual(hash1, hash2)
    
    def test_input_change_sensitivity(self):
        """Test that small changes in input produce different hashes."""
        base_data = b"test data for sensitivity check"
        base_hash = QuantumEnhancedHash.hash(base_data)
        
        # Change a single bit
        modified_data = bytearray(base_data)
        modified_data[0] ^= 1  # Flip the first bit
        modified_hash = QuantumEnhancedHash.hash(bytes(modified_data))
        
        # Hashes should be different
        self.assertNotEqual(base_hash, modified_hash)
        
        # Add a byte
        modified_data = base_data + b"x"
        modified_hash = QuantumEnhancedHash.hash(modified_data)
        
        # Hashes should be different
        self.assertNotEqual(base_hash, modified_hash)
    
    def test_large_input(self):
        """Test hash with large input."""
        large_data = os.urandom(1024 * 1024)  # 1MB of random data
        hash_value = QuantumEnhancedHash.hash(large_data)
        
        # Hash should be computed without errors
        self.assertEqual(len(hash_value), 32)
    
    def test_block_boundary(self):
        """Test hash with data sizes at block boundaries."""
        block_size = 1024  # The block size used in QuantumEnhancedHash
        
        # Test exactly at block size
        data1 = os.urandom(block_size)
        hash1 = QuantumEnhancedHash.hash(data1)
        
        # Test just below block size
        data2 = os.urandom(block_size - 1)
        hash2 = QuantumEnhancedHash.hash(data2)
        
        # Test just above block size
        data3 = os.urandom(block_size + 1)
        hash3 = QuantumEnhancedHash.hash(data3)
        
        # Test at multiple block sizes
        data4 = os.urandom(block_size * 2)
        hash4 = QuantumEnhancedHash.hash(data4)
        
        # All hashes should be computed without errors
        self.assertEqual(len(hash1), 32)
        self.assertEqual(len(hash2), 32)
        self.assertEqual(len(hash3), 32)
        self.assertEqual(len(hash4), 32)

class HashComparisonTests(unittest.TestCase):
    """Comparison tests between different hash functions."""
    
    def setUp(self):
        """Set up test data and hash functions."""
        self.test_vectors = [
            b"",  # Empty string
            b"a",  # Single character
            b"abc",  # Short string
            b"The quick brown fox jumps over the lazy dog",  # Common test phrase
            os.urandom(1024),  # Random data
        ]
        
        self.hash_functions = {
            "DiracHash-standard": lambda data: DiracHash.hash(data, algorithm="standard"),
            "DiracHash-improved": lambda data: DiracHash.hash(data, algorithm="improved"),
            "DiracHash-grover": lambda data: DiracHash.hash(data, algorithm="grover"),
            "DiracHash-shor": lambda data: DiracHash.hash(data, algorithm="shor"),
            "QuantumEnhanced": lambda data: QuantumEnhancedHash.hash(data),
            "SHA-256": lambda data: hashlib.sha256(data).digest(),
            "SHA-512": lambda data: hashlib.sha512(data).digest()[:32],  # Truncate to 32 bytes
        }
    
    def test_uniqueness_across_functions(self):
        """Test that different hash functions produce different results."""
        for data in self.test_vectors:
            hashes = {}
            for name, func in self.hash_functions.items():
                hashes[name] = func(data)
            
            # Check that each function produces a different hash
            for name1, hash1 in hashes.items():
                for name2, hash2 in hashes.items():
                    if name1 != name2:
                        self.assertNotEqual(hash1, hash2, 
                                          f"Hash functions {name1} and {name2} produced identical hashes")
    
    def test_avalanche_properties(self):
        """Test avalanche properties of hash functions."""
        # This is a minimal test - more detailed avalanche testing is in nist_sts_tester.py
        data = b"test data for avalanche check"
        
        for name, func in self.hash_functions.items():
            # Get hash of original data
            original_hash = func(data)
            
            # Create a modified version (flip one bit)
            modified_data = bytearray(data)
            bit_pos = random.randint(0, len(data) * 8 - 1)
            byte_pos, bit_in_byte = divmod(bit_pos, 8)
            modified_data[byte_pos] ^= (1 << bit_in_byte)  # Flip the bit
            
            # Get hash of modified data
            modified_hash = func(bytes(modified_data))
            
            # Count the number of bits that differ
            different_bits = 0
            for b1, b2 in zip(original_hash, modified_hash):
                xor = b1 ^ b2
                # Count bits set in xor
                for i in range(8):
                    different_bits += (xor >> i) & 1
            
            # Calculate percentage of bits that changed
            percent_changed = (different_bits / (len(original_hash) * 8)) * 100
            
            # For a good hash function, around 50% of bits should change
            # We'll use a loose check here since this is a minimal test
            self.assertGreaterEqual(percent_changed, 25, 
                                   f"{name} showed poor avalanche effect ({percent_changed:.2f}%)")
            self.assertLessEqual(percent_changed, 75, 
                                f"{name} showed suspicious avalanche effect ({percent_changed:.2f}%)")

def run_tests():
    """Run all tests."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases - using TestLoader instead of makeSuite which is not available in Python 3.13
    loader = unittest.TestLoader()
    test_suite.addTest(loader.loadTestsFromTestCase(DiracHashTests))
    test_suite.addTest(loader.loadTestsFromTestCase(QuantumEnhancedHashTests))
    test_suite.addTest(loader.loadTestsFromTestCase(HashComparisonTests))
    
    # Create test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run tests
    return runner.run(test_suite)

if __name__ == "__main__":
    print(f"Running tests for quantum-resistant hash functions...")
    result = run_tests()
    
    # Report results
    tests_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    
    print(f"\nTest Summary:")
    print(f"- Tests Run: {tests_run}")
    print(f"- Failures: {failures}")
    print(f"- Errors: {errors}")
    
    # Set exit code
    sys.exit(1 if failures or errors else 0) 
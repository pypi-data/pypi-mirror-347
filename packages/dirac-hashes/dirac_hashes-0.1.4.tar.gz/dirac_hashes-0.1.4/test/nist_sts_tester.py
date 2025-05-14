#!/usr/bin/env python3
"""
NIST Statistical Test Suite (STS) compatibility test for quantum-resistant hash functions.

This module generates test data from our hash functions that can be used with the 
NIST Statistical Test Suite to evaluate randomness properties.
"""

import os
import sys
import random
import hashlib
import argparse
import binascii
from pathlib import Path
from typing import List, Callable, Dict, Any, Tuple

# Add the parent directory to the path to ensure correct imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our hash functions
from src.quantum_hash.dirac import DiracHash
from src.quantum_hash.enhanced import QuantumEnhancedHash

# Hash function registry
HASH_FUNCTIONS = {
    "dirac-standard": lambda data: DiracHash.hash(data, algorithm="standard"),
    "dirac-improved": lambda data: DiracHash.hash(data, algorithm="improved"),
    "dirac-grover": lambda data: DiracHash.hash(data, algorithm="grover"),
    "dirac-shor": lambda data: DiracHash.hash(data, algorithm="shor"),
    "quantum-enhanced": lambda data: QuantumEnhancedHash.hash(data),
    "sha256": lambda data: hashlib.sha256(data).digest(),
    "sha512": lambda data: hashlib.sha512(data).digest(),
}

def generate_binary_sequence(hash_function: Callable, seed: bytes, length: int) -> str:
    """
    Generate a binary sequence of specified length using the given hash function.
    
    Args:
        hash_function: Hash function to use
        seed: Initial seed
        length: Length of binary sequence in bits
        
    Returns:
        Binary sequence as string of 0's and 1's
    """
    result = ""
    data = seed
    
    while len(result) < length:
        # Hash the current data
        hash_value = hash_function(data)
        
        # Convert each byte to bits and add to result
        for byte in hash_value:
            # Convert byte to 8 bits
            bits = format(byte, '08b')
            result += bits
            
            if len(result) >= length:
                break
                
        # Use the hash as the next input
        data = hash_value
        
    # Truncate to exact length
    return result[:length]

def generate_test_data(hash_name: str, output_dir: str, sequence_length: int = 1_000_000,
                      num_sequences: int = 10, seed_size: int = 16) -> None:
    """
    Generate test data files for NIST STS testing.
    
    Args:
        hash_name: Name of the hash function to use
        output_dir: Directory to save output files
        sequence_length: Length of each sequence in bits
        num_sequences: Number of sequences to generate
        seed_size: Size of random seed in bytes
    """
    # Get the hash function
    if hash_name not in HASH_FUNCTIONS:
        raise ValueError(f"Unknown hash function: {hash_name}")
    
    hash_function = HASH_FUNCTIONS[hash_name]
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate sequences
    for i in range(num_sequences):
        # Generate random seed
        seed = os.urandom(seed_size)
        
        # Generate binary sequence
        binary_sequence = generate_binary_sequence(hash_function, seed, sequence_length)
        
        # Save to file
        filename = f"{hash_name}_seq_{i+1}.bin"
        file_path = os.path.join(output_dir, filename)
        
        # Convert binary string to bytes
        # NIST STS expects binary data, not ASCII text
        byte_data = bytearray()
        for j in range(0, len(binary_sequence), 8):
            chunk = binary_sequence[j:j+8].ljust(8, '0')
            byte_data.append(int(chunk, 2))
        
        with open(file_path, 'wb') as f:
            f.write(byte_data)
        
        print(f"Generated {filename} ({sequence_length} bits)")

def run_avalanche_test(hash_name: str, num_tests: int = 1000) -> Dict[str, float]:
    """
    Run avalanche effect test on the specified hash function.
    
    Avalanche effect: a small change in input should cause significant 
    changes in the output (ideally ~50% of output bits change).
    
    Args:
        hash_name: Name of the hash function to test
        num_tests: Number of test cases
        
    Returns:
        Dictionary with test results
    """
    if hash_name not in HASH_FUNCTIONS:
        raise ValueError(f"Unknown hash function: {hash_name}")
    
    hash_function = HASH_FUNCTIONS[hash_name]
    
    # Track bit changes
    total_bits = 0
    changed_bits = 0
    
    # Run tests
    for _ in range(num_tests):
        # Generate random data
        data_size = random.randint(1, 1024)  # 1 byte to 1KB
        data1 = os.urandom(data_size)
        
        # Change a single random bit to create data2
        bit_pos = random.randint(0, data_size * 8 - 1)
        byte_pos = bit_pos // 8
        bit_in_byte = bit_pos % 8
        
        # Convert to bytearray for mutation
        data2 = bytearray(data1)
        data2[byte_pos] ^= (1 << bit_in_byte)  # Flip the bit
        data2 = bytes(data2)
        
        # Hash both inputs
        hash1 = hash_function(data1)
        hash2 = hash_function(data2)
        
        # Count different bits
        hash_len = len(hash1)
        for i in range(hash_len):
            xor_byte = hash1[i] ^ hash2[i]
            # Count bits set in xor_byte (Hamming weight)
            for j in range(8):
                if xor_byte & (1 << j):
                    changed_bits += 1
            
        total_bits += hash_len * 8
    
    # Calculate avalanche percentage
    avalanche_percentage = (changed_bits / total_bits) * 100
    
    return {
        "hash_function": hash_name,
        "test_cases": num_tests,
        "changed_bits": changed_bits,
        "total_bits": total_bits,
        "avalanche_percentage": avalanche_percentage,
        "ideal_percentage": 50.0,
        "deviation": abs(50.0 - avalanche_percentage)
    }

def run_distribution_test(hash_name: str, num_tests: int = 1000) -> Dict[str, Any]:
    """
    Test the distribution of bits/bytes in the hash output.
    
    Args:
        hash_name: Name of the hash function to test
        num_tests: Number of test cases
        
    Returns:
        Dictionary with test results
    """
    if hash_name not in HASH_FUNCTIONS:
        raise ValueError(f"Unknown hash function: {hash_name}")
    
    hash_function = HASH_FUNCTIONS[hash_name]
    
    # Byte frequency counters
    byte_counts = [0] * 256
    
    # Generate random inputs and hash them
    for _ in range(num_tests):
        data_size = random.randint(1, 1024)
        data = os.urandom(data_size)
        
        hash_value = hash_function(data)
        
        # Count byte frequencies
        for byte in hash_value:
            byte_counts[byte] += 1
    
    # Calculate statistics
    total_bytes = sum(byte_counts)
    expected_count = total_bytes / 256
    
    # Chi-square test
    chi_square = sum((count - expected_count) ** 2 / expected_count for count in byte_counts)
    
    # Calculate highest and lowest frequencies
    max_byte = max(byte_counts)
    min_byte = min(byte_counts)
    max_deviation = (max_byte - expected_count) / expected_count * 100
    min_deviation = (expected_count - min_byte) / expected_count * 100
    
    return {
        "hash_function": hash_name,
        "test_cases": num_tests,
        "total_bytes": total_bytes,
        "expected_count": expected_count,
        "chi_square": chi_square,
        "max_deviation_percent": max_deviation,
        "min_deviation_percent": min_deviation,
        # Chi-square threshold for 255 degrees of freedom, 95% confidence: ~293.25
        "chi_square_threshold": 293.25,
        "distribution_quality": "good" if chi_square < 293.25 else "poor"
    }

def run_collision_test(hash_name: str, digest_size: int = 16, num_hashes: int = 100000) -> Dict[str, Any]:
    """
    Test for hash collisions by generating many hashes and checking for duplicates.
    
    Args:
        hash_name: Name of the hash function to test
        digest_size: Size of hash digest in bytes (smaller increases collision chance)
        num_hashes: Number of hashes to generate
        
    Returns:
        Dictionary with test results
    """
    if hash_name not in HASH_FUNCTIONS:
        raise ValueError(f"Unknown hash function: {hash_name}")
    
    # Create a customized hash function with the given digest size
    if hash_name.startswith("dirac"):
        parts = hash_name.split("-")
        if len(parts) > 1:
            algorithm = parts[1]
            hash_function = lambda data: DiracHash.hash(data, algorithm=algorithm, digest_size=digest_size)
        else:
            hash_function = lambda data: DiracHash.hash(data, digest_size=digest_size)
    elif hash_name == "quantum-enhanced":
        hash_function = lambda data: QuantumEnhancedHash.hash(data, digest_size=digest_size)
    elif hash_name == "sha256":
        hash_function = lambda data: hashlib.sha256(data).digest()[:digest_size]
    elif hash_name == "sha512":
        hash_function = lambda data: hashlib.sha512(data).digest()[:digest_size]
    else:
        hash_function = HASH_FUNCTIONS[hash_name]
    
    # Generate hashes and check for collisions
    hash_set = set()
    collisions = 0
    
    for i in range(num_hashes):
        # Generate random data
        data = f"test-data-{i}-{os.urandom(16).hex()}".encode()
        
        # Hash the data
        hash_value = hash_function(data)
        
        # Convert to hashable type
        hash_bytes = hash_value
        
        # Check for collision
        if hash_bytes in hash_set:
            collisions += 1
        else:
            hash_set.add(hash_bytes)
        
        # Progress indicator
        if (i + 1) % 10000 == 0:
            print(f"Processed {i + 1}/{num_hashes} hashes, found {collisions} collisions")
    
    # Calculate theoretical collision probability
    # Using birthday paradox approximation
    theoretical_prob = 1.0 - (2**(digest_size*8) - num_hashes) / 2**(digest_size*8)
    
    return {
        "hash_function": hash_name,
        "digest_size_bytes": digest_size,
        "digest_size_bits": digest_size * 8,
        "number_of_hashes": num_hashes,
        "collisions_found": collisions,
        "collision_percentage": (collisions / num_hashes) * 100,
        "theoretical_probability": theoretical_prob * 100,
        "space_utilization": len(hash_set) / num_hashes * 100
    }

def main():
    parser = argparse.ArgumentParser(description="NIST Statistical Test Suite data generator")
    
    # Define subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate test data for NIST STS")
    generate_parser.add_argument("hash_function", choices=HASH_FUNCTIONS.keys(), help="Hash function to test")
    generate_parser.add_argument("--output-dir", "-o", default="nist_test_data", help="Output directory")
    generate_parser.add_argument("--sequence-length", "-l", type=int, default=1_000_000, 
                                help="Length of each sequence in bits")
    generate_parser.add_argument("--num-sequences", "-n", type=int, default=10, 
                                help="Number of sequences to generate")
    
    # Avalanche command
    avalanche_parser = subparsers.add_parser("avalanche", help="Run avalanche effect test")
    avalanche_parser.add_argument("hash_function", choices=HASH_FUNCTIONS.keys(), help="Hash function to test")
    avalanche_parser.add_argument("--num-tests", "-n", type=int, default=1000, help="Number of test cases")
    
    # Distribution command
    dist_parser = subparsers.add_parser("distribution", help="Run distribution test")
    dist_parser.add_argument("hash_function", choices=HASH_FUNCTIONS.keys(), help="Hash function to test")
    dist_parser.add_argument("--num-tests", "-n", type=int, default=1000, help="Number of test cases")
    
    # Collision command
    collision_parser = subparsers.add_parser("collision", help="Run collision test")
    collision_parser.add_argument("hash_function", choices=HASH_FUNCTIONS.keys(), help="Hash function to test")
    collision_parser.add_argument("--digest-size", "-d", type=int, default=16, 
                                 help="Digest size in bytes (smaller increases collision chance)")
    collision_parser.add_argument("--num-hashes", "-n", type=int, default=100000, 
                                 help="Number of hashes to generate")
    
    # All command
    all_parser = subparsers.add_parser("all", help="Run all tests")
    all_parser.add_argument("hash_function", choices=HASH_FUNCTIONS.keys(), help="Hash function to test")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        generate_test_data(args.hash_function, args.output_dir, args.sequence_length, args.num_sequences)
        print(f"\nGenerated {args.num_sequences} test files in {args.output_dir}")
        print("Run these files through the NIST Statistical Test Suite for randomness analysis")
    
    elif args.command == "avalanche":
        results = run_avalanche_test(args.hash_function, args.num_tests)
        print("\nAvalanche Test Results:")
        print(f"Hash Function: {results['hash_function']}")
        print(f"Test Cases: {results['test_cases']}")
        print(f"Changed Bits: {results['changed_bits']}")
        print(f"Total Bits: {results['total_bits']}")
        print(f"Avalanche Effect: {results['avalanche_percentage']:.2f}%")
        print(f"Ideal: {results['ideal_percentage']:.2f}%")
        print(f"Deviation: {results['deviation']:.2f}%")
        
        # Evaluation
        if results['deviation'] < 1.0:
            print("Evaluation: EXCELLENT - Very close to ideal")
        elif results['deviation'] < 3.0:
            print("Evaluation: GOOD - Acceptable deviation")
        elif results['deviation'] < 5.0:
            print("Evaluation: FAIR - Some concerns about diffusion")
        else:
            print("Evaluation: POOR - Significant deviation from ideal, needs improvement")
    
    elif args.command == "distribution":
        results = run_distribution_test(args.hash_function, args.num_tests)
        print("\nDistribution Test Results:")
        print(f"Hash Function: {results['hash_function']}")
        print(f"Test Cases: {results['test_cases']}")
        print(f"Total Bytes: {results['total_bytes']}")
        print(f"Expected Count per Byte: {results['expected_count']:.2f}")
        print(f"Chi-square Value: {results['chi_square']:.2f}")
        print(f"Chi-square Threshold (95%): {results['chi_square_threshold']}")
        print(f"Max Deviation: {results['max_deviation_percent']:.2f}%")
        print(f"Min Deviation: {results['min_deviation_percent']:.2f}%")
        print(f"Distribution Quality: {results['distribution_quality'].upper()}")
        
        # Evaluation
        if results['chi_square'] < results['chi_square_threshold'] * 0.5:
            print("Evaluation: EXCELLENT - Very uniform distribution")
        elif results['chi_square'] < results['chi_square_threshold']:
            print("Evaluation: GOOD - Acceptable distribution")
        elif results['chi_square'] < results['chi_square_threshold'] * 1.5:
            print("Evaluation: FAIR - Some concerns about distribution")
        else:
            print("Evaluation: POOR - Non-uniform distribution, needs improvement")
    
    elif args.command == "collision":
        results = run_collision_test(args.hash_function, args.digest_size, args.num_hashes)
        print("\nCollision Test Results:")
        print(f"Hash Function: {results['hash_function']}")
        print(f"Digest Size: {results['digest_size_bytes']} bytes ({results['digest_size_bits']} bits)")
        print(f"Number of Hashes: {results['number_of_hashes']}")
        print(f"Collisions Found: {results['collisions_found']}")
        print(f"Collision Percentage: {results['collision_percentage']:.8f}%")
        print(f"Theoretical Probability: {results['theoretical_probability']:.8f}%")
        print(f"Space Utilization: {results['space_utilization']:.2f}%")
        
        # Evaluation
        observed = results['collisions_found']
        theoretical = results['theoretical_probability'] * results['number_of_hashes'] / 100
        
        if observed == 0 and theoretical < 1:
            print("Evaluation: EXCELLENT - No collisions as expected")
        elif observed <= theoretical * 1.1:
            print("Evaluation: GOOD - Collision rate close to theoretical expectation")
        elif observed <= theoretical * 2:
            print("Evaluation: FAIR - More collisions than expected")
        else:
            print("Evaluation: POOR - Significantly more collisions than expected, needs improvement")
    
    elif args.command == "all":
        # Run all tests
        print("\n=== Running Avalanche Test ===")
        avalanche_results = run_avalanche_test(args.hash_function)
        print(f"Avalanche Effect: {avalanche_results['avalanche_percentage']:.2f}%")
        
        print("\n=== Running Distribution Test ===")
        dist_results = run_distribution_test(args.hash_function)
        print(f"Distribution Quality: {dist_results['distribution_quality'].upper()}")
        
        print("\n=== Running Collision Test ===")
        collision_results = run_collision_test(args.hash_function)
        print(f"Collisions Found: {collision_results['collisions_found']}")
        
        print("\n=== Generating NIST STS Test Data ===")
        output_dir = f"nist_test_data_{args.hash_function}"
        generate_test_data(args.hash_function, output_dir, sequence_length=100000, num_sequences=3)
        print(f"Generated test files in {output_dir}")
        
        # Overall evaluation
        print("\n=== Overall Evaluation ===")
        issues = []
        
        if avalanche_results['deviation'] > 3.0:
            issues.append(f"Avalanche effect deviation: {avalanche_results['deviation']:.2f}%")
            
        if dist_results['distribution_quality'] != "good":
            issues.append(f"Distribution quality: {dist_results['distribution_quality']}")
            
        if collision_results['collisions_found'] > 0:
            issues.append(f"Collisions found: {collision_results['collisions_found']}")
            
        if issues:
            print("Issues that need improvement:")
            for issue in issues:
                print(f"- {issue}")
        else:
            print("All tests passed successfully!")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 
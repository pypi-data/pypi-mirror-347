#!/usr/bin/env python3
"""
Quantum Resistance Security Benchmarking

This script provides comprehensive security benchmarking for quantum-resistant 
cryptographic algorithms, focusing on resistance to quantum attacks, security margin 
evaluation, and formal security metrics.
"""

import os
import sys
import time
import hashlib
import argparse
import statistics
import platform
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Callable, Tuple, Any, Optional

# Add the parent directory to the path to ensure correct imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import quantum-resistant algorithms
from src.quantum_hash.dirac import DiracHash
from src.quantum_hash.enhanced import QuantumEnhancedHash
from src.quantum_hash.kem.kyber import KyberKEM
from src.quantum_hash.signatures import LamportSignature, SPHINCSSignature, DilithiumSignature

# Try to import colorama for colored output
try:
    from colorama import init, Fore, Style
    init()  # Initialize colorama
    HAVE_COLORS = True
except ImportError:
    HAVE_COLORS = False
    # Create dummy color codes
    class DummyFore:
        RED = ''
        GREEN = ''
        YELLOW = ''
        BLUE = ''
        CYAN = ''
        RESET = ''
    
    class DummyStyle:
        BRIGHT = ''
        RESET_ALL = ''
    
    Fore = DummyFore()
    Style = DummyStyle()

class QuantumSecurityBenchmark:
    """Comprehensive security benchmark for quantum-resistant algorithms."""
    
    def __init__(self):
        """Initialize the benchmark with algorithms to test."""
        # Hash functions to benchmark
        self.hash_functions = {
            "dirac-standard": lambda data: DiracHash.hash(data, algorithm="standard"),
            "dirac-improved": lambda data: DiracHash.hash(data, algorithm="improved"),
            "dirac-grover": lambda data: DiracHash.hash(data, algorithm="grover"),
            "dirac-shor": lambda data: DiracHash.hash(data, algorithm="shor"),
            "quantum-enhanced": lambda data: QuantumEnhancedHash.hash(data),
            "sha256": lambda data: hashlib.sha256(data).digest(),
            "sha512": lambda data: hashlib.sha512(data).digest(),
        }
        
        # KEM algorithms
        self.kem_algorithms = {
            "kyber-512": KyberKEM(security_level=1),
            "kyber-768": KyberKEM(security_level=3),
            "kyber-1024": KyberKEM(security_level=5),
        }
        
        # Signature algorithms
        self.signature_algorithms = {
            "lamport": LamportSignature(hash_algorithm='improved'),
            "sphincs-fast": SPHINCSSignature(fast_mode=True),
            "sphincs-secure": SPHINCSSignature(fast_mode=False),
            "dilithium-2": DilithiumSignature(security_level=2),
            "dilithium-3": DilithiumSignature(security_level=3),
            "dilithium-5": DilithiumSignature(security_level=5),
        }
        
        # Input data sizes (in bytes)
        self.sizes = [
            ("Small", 64),
            ("Medium", 1024),
            ("Large", 65536),
        ]
        
        # System info
        self.system_info = self._get_system_info()
    
    def _get_system_info(self) -> Dict[str, str]:
        """Get information about the system."""
        info = {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "processor": platform.processor(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        # Try to get more detailed CPU info on Linux
        if os.path.exists('/proc/cpuinfo'):
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if line.startswith('model name'):
                            info["cpu_model"] = line.split(':', 1)[1].strip()
                            break
            except:
                pass
        
        return info
    
    def benchmark_avalanche_effect(self, hash_name: str, hash_func: Callable,
                                  num_tests: int = 100) -> Dict[str, Any]:
        """
        Benchmark the avalanche effect of a hash function.
        
        Args:
            hash_name: Name of the hash function
            hash_func: Hash function to benchmark
            num_tests: Number of test iterations
            
        Returns:
            Dictionary with benchmark results
        """
        # Track bit changes
        total_bits = 0
        changed_bits = 0
        bit_change_percentages = []
        
        # Run tests
        for _ in range(num_tests):
            # Generate random data
            data_size = 64  # Fixed size for consistency
            data1 = os.urandom(data_size)
            
            # Create data2 by flipping a single bit
            bit_pos = _ % (data_size * 8)  # Cycle through all bit positions
            byte_pos = bit_pos // 8
            bit_in_byte = bit_pos % 8
            
            data2 = bytearray(data1)
            data2[byte_pos] ^= (1 << bit_in_byte)  # Flip the bit
            data2 = bytes(data2)
            
            # Hash both inputs
            hash1 = hash_func(data1)
            hash2 = hash_func(data2)
            
            # Count different bits
            hash_len = len(hash1)
            test_changed_bits = 0
            
            for i in range(hash_len):
                xor_byte = hash1[i] ^ hash2[i]
                for j in range(8):
                    if xor_byte & (1 << j):
                        test_changed_bits += 1
                        changed_bits += 1
            
            test_total_bits = hash_len * 8
            total_bits += test_total_bits
            
            # Calculate percentage for this test
            bit_change_percentages.append((test_changed_bits / test_total_bits) * 100)
        
        # Calculate statistics
        avalanche_percentage = (changed_bits / total_bits) * 100
        std_dev = statistics.stdev(bit_change_percentages) if len(bit_change_percentages) > 1 else 0
        
        return {
            "hash_function": hash_name,
            "test_cases": num_tests,
            "avalanche_percentage": avalanche_percentage,
            "ideal_percentage": 50.0,
            "deviation": abs(50.0 - avalanche_percentage),
            "std_deviation": std_dev,
            "consistency": "high" if std_dev < 5 else "medium" if std_dev < 10 else "low",
            "security_rating": self._rate_avalanche(avalanche_percentage, std_dev)
        }
    
    def _rate_avalanche(self, percentage: float, std_dev: float) -> str:
        """Rate the avalanche effect quality."""
        if abs(percentage - 50.0) < 1.0 and std_dev < 5.0:
            return "excellent"
        elif abs(percentage - 50.0) < 3.0 and std_dev < 8.0:
            return "good"
        elif abs(percentage - 50.0) < 5.0 and std_dev < 10.0:
            return "acceptable"
        else:
            return "poor"
    
    def benchmark_kem_security(self, name: str, kem: KyberKEM, 
                              num_tests: int = 10) -> Dict[str, Any]:
        """
        Benchmark the security properties of a KEM algorithm.
        
        Args:
            name: Name of the KEM algorithm
            kem: KEM instance to benchmark
            num_tests: Number of test iterations
            
        Returns:
            Dictionary with benchmark results
        """
        results = {
            "algorithm": name,
            "num_tests": num_tests,
            "key_sizes": {},
            "ciphertext_sizes": [],
            "shared_secret_sizes": [],
            "key_reuse_security": True,
            "ciphertext_tamper_resistance": True,
            "quantum_security_level": self._get_quantum_security_level(name)
        }
        
        # Generate key pairs and test properties
        pk, sk = kem.generate_keypair()
        
        # Record key sizes
        results["key_sizes"] = {
            "public_key": self._calculate_object_size(pk),
            "private_key": self._calculate_object_size(sk)
        }
        
        # Test encapsulation properties
        for _ in range(num_tests):
            # Encapsulate
            ciphertext, shared_secret_1 = kem.encapsulate(pk)
            
            # Record sizes
            results["ciphertext_sizes"].append(len(ciphertext))
            results["shared_secret_sizes"].append(len(shared_secret_1))
            
            # Test ciphertext tampering
            tampered = bytearray(ciphertext)
            # Modify random byte
            pos = _ % len(tampered)
            tampered[pos] ^= 0xFF
            tampered_shared = kem.decapsulate(bytes(tampered), sk)
            
            # If shared secrets match after tampering, security issue
            if tampered_shared == shared_secret_1:
                results["ciphertext_tamper_resistance"] = False
        
        # Get consistent sizes
        results["ciphertext_size"] = statistics.mean(results["ciphertext_sizes"])
        results["shared_secret_size"] = statistics.mean(results["shared_secret_sizes"])
        
        # Clean up lists that are just for calculations
        del results["ciphertext_sizes"]
        del results["shared_secret_sizes"]
        
        return results
    
    def benchmark_signature_security(self, name: str, signer: Any, 
                                    num_tests: int = 5) -> Dict[str, Any]:
        """
        Benchmark the security properties of a signature algorithm.
        
        Args:
            name: Name of the signature algorithm
            signer: Signature instance to benchmark
            num_tests: Number of test iterations
            
        Returns:
            Dictionary with benchmark results
        """
        results = {
            "algorithm": name,
            "num_tests": num_tests,
            "key_sizes": {},
            "signature_sizes": [],
            "signature_tampering_resistance": True,
            "message_tampering_resistance": True,
            "quantum_security_level": self._get_quantum_security_level(name)
        }
        
        # Generate key pair
        private_key, public_key = signer.generate_keypair()
        
        # Record key sizes
        results["key_sizes"] = {
            "public_key": self._calculate_object_size(public_key),
            "private_key": self._calculate_object_size(private_key),
        }
        
        # Test signing properties with different message sizes
        for size_name, size in self.sizes:
            # Generate random message
            message = os.urandom(size)
            
            # Sign the message
            signature = signer.sign(message, private_key)
            
            # Record signature size
            results["signature_sizes"].append(len(signature) if isinstance(signature, bytes) else self._calculate_object_size(signature))
            
            # Test message tampering
            tampered_message = bytearray(message)
            tampered_message[0] ^= 0x01  # Flip one bit
            tampered_verify = signer.verify(bytes(tampered_message), signature, public_key)
            
            # If verification succeeds with tampered message, security issue
            if tampered_verify:
                results["message_tampering_resistance"] = False
                
            # Test signature tampering (if signature is bytes)
            if isinstance(signature, bytes):
                tampered_sig = bytearray(signature)
                # Modify a byte in the signature
                pos = len(tampered_sig) // 2
                tampered_sig[pos] ^= 0xFF
                sig_tampered_verify = signer.verify(message, bytes(tampered_sig), public_key)
                
                # If verification succeeds with tampered signature, security issue
                if sig_tampered_verify:
                    results["signature_tampering_resistance"] = False
        
        # Calculate average signature size
        results["avg_signature_size"] = statistics.mean(results["signature_sizes"])
        del results["signature_sizes"]
        
        return results
    
    def _calculate_object_size(self, obj: Any) -> int:
        """Calculate the size of an object in bytes."""
        if isinstance(obj, bytes):
            return len(obj)
        elif isinstance(obj, (dict, list)):
            # Convert to JSON and measure
            return len(json.dumps(obj).encode('utf-8'))
        else:
            # Fallback: convert to string and measure
            return len(str(obj).encode('utf-8'))
    
    def _get_quantum_security_level(self, algorithm_name: str) -> Dict[str, Any]:
        """
        Get quantum security level information for an algorithm.
        
        Args:
            algorithm_name: Name of the algorithm
            
        Returns:
            Dictionary with security level information
        """
        # Security levels for different algorithms (in bits)
        # Values based on NIST PQC standardization estimates
        security_levels = {
            "kyber-512": {
                "classical_bits": 128, 
                "quantum_bits": 64,
                "nist_level": 1,
                "grover_resistance": "medium",
                "shor_resistance": "high"
            },
            "kyber-768": {
                "classical_bits": 192, 
                "quantum_bits": 96,
                "nist_level": 3,
                "grover_resistance": "high",
                "shor_resistance": "high"
            },
            "kyber-1024": {
                "classical_bits": 256, 
                "quantum_bits": 128,
                "nist_level": 5,
                "grover_resistance": "very high",
                "shor_resistance": "high"
            },
            "lamport": {
                "classical_bits": 256,
                "quantum_bits": 128,
                "nist_level": 5,
                "grover_resistance": "very high",
                "shor_resistance": "high",
                "note": "One-time signature scheme"
            },
            "sphincs-fast": {
                "classical_bits": 128,
                "quantum_bits": 64,
                "nist_level": 1,
                "grover_resistance": "medium",
                "shor_resistance": "high"
            },
            "sphincs-secure": {
                "classical_bits": 256,
                "quantum_bits": 128,
                "nist_level": 5,
                "grover_resistance": "very high",
                "shor_resistance": "high"
            },
            "dilithium-2": {
                "classical_bits": 128,
                "quantum_bits": 64,
                "nist_level": 2,
                "grover_resistance": "medium",
                "shor_resistance": "high"
            },
            "dilithium-3": {
                "classical_bits": 192,
                "quantum_bits": 96,
                "nist_level": 3,
                "grover_resistance": "high",
                "shor_resistance": "high"
            },
            "dilithium-5": {
                "classical_bits": 256,
                "quantum_bits": 128,
                "nist_level": 5,
                "grover_resistance": "very high",
                "shor_resistance": "high"
            },
            "dirac-standard": {
                "classical_bits": 128,
                "quantum_bits": 64,
                "grover_resistance": "medium",
                "shor_resistance": "high"
            },
            "dirac-improved": {
                "classical_bits": 256,
                "quantum_bits": 128,
                "grover_resistance": "high",
                "shor_resistance": "high"
            },
            "dirac-grover": {
                "classical_bits": 384,
                "quantum_bits": 192,
                "grover_resistance": "very high",
                "shor_resistance": "high",
                "note": "Specifically designed to resist Grover's algorithm"
            },
            "dirac-shor": {
                "classical_bits": 256,
                "quantum_bits": 128,
                "grover_resistance": "high",
                "shor_resistance": "very high",
                "note": "Specifically designed to resist Shor's algorithm"
            },
            "quantum-enhanced": {
                "classical_bits": 256,
                "quantum_bits": 128,
                "grover_resistance": "very high",
                "shor_resistance": "very high"
            },
            "sha256": {
                "classical_bits": 128,
                "quantum_bits": 64,
                "grover_resistance": "medium",
                "shor_resistance": "high",
                "note": "Vulnerable to Grover's algorithm"
            },
            "sha512": {
                "classical_bits": 256,
                "quantum_bits": 128,
                "grover_resistance": "high",
                "shor_resistance": "high",
                "note": "Partially resistant to Grover's algorithm due to larger output"
            }
        }
        
        # Return security level for the specified algorithm
        return security_levels.get(algorithm_name, {
            "classical_bits": "unknown",
            "quantum_bits": "unknown",
            "note": "Security level information not available"
        })
    
    def run_security_benchmark(self, hash_names: List[str] = None, 
                              kem_names: List[str] = None,
                              signature_names: List[str] = None,
                              verbose: bool = True) -> Dict[str, Any]:
        """
        Run comprehensive security benchmarks.
        
        Args:
            hash_names: List of hash function names to benchmark
            kem_names: List of KEM algorithm names to benchmark
            signature_names: List of signature algorithm names to benchmark
            verbose: Whether to print progress
            
        Returns:
            Dictionary with all benchmark results
        """
        results = {
            "system_info": self.system_info,
            "timestamp": datetime.now().isoformat(),
            "hash_functions": [],
            "kem_algorithms": [],
            "signature_algorithms": []
        }
        
        # Filter hash functions if specified
        if hash_names:
            hash_functions = {name: func for name, func in self.hash_functions.items() 
                            if name in hash_names}
        else:
            hash_functions = self.hash_functions
        
        # Filter KEMs if specified
        if kem_names:
            kem_algorithms = {name: algo for name, algo in self.kem_algorithms.items()
                             if name in kem_names}
        else:
            kem_algorithms = self.kem_algorithms
            
        # Filter signatures if specified
        if signature_names:
            signature_algorithms = {name: algo for name, algo in self.signature_algorithms.items()
                                  if name in signature_names}
        else:
            signature_algorithms = self.signature_algorithms
        
        # Display header
        if verbose:
            print(f"\n{Style.BRIGHT}{Fore.BLUE}Running Quantum-Resistance Security Benchmarks{Style.RESET_ALL}")
            print(f"System: {self.system_info.get('platform', 'Unknown')}")
            print(f"Processor: {self.system_info.get('cpu_model', self.system_info.get('processor', 'Unknown'))}")
            print(f"Date: {self.system_info.get('date', 'Unknown')}")
            print("-" * 80)
        
        # 1. Benchmark hash functions
        if hash_functions:
            if verbose:
                print(f"\n{Style.BRIGHT}{Fore.CYAN}Testing Hash Function Security Properties{Style.RESET_ALL}")
            
            for name, func in hash_functions.items():
                if verbose:
                    print(f"{Fore.YELLOW}Testing {name}...{Fore.RESET}")
                
                try:
                    # Benchmark avalanche effect
                    avalanche_results = self.benchmark_avalanche_effect(name, func)
                    
                    # Add to results
                    results["hash_functions"].append({
                        "name": name,
                        "avalanche_effect": avalanche_results,
                        "quantum_security": self._get_quantum_security_level(name)
                    })
                    
                    if verbose:
                        print(f"  Avalanche: {avalanche_results['avalanche_percentage']:.2f}% (ideal: 50%) - {avalanche_results['security_rating'].upper()}")
                except Exception as e:
                    if verbose:
                        print(f"{Fore.RED}Error testing {name}: {e}{Fore.RESET}")
        
        # 2. Benchmark KEM algorithms
        if kem_algorithms:
            if verbose:
                print(f"\n{Style.BRIGHT}{Fore.CYAN}Testing KEM Algorithm Security Properties{Style.RESET_ALL}")
            
            for name, algo in kem_algorithms.items():
                if verbose:
                    print(f"{Fore.YELLOW}Testing {name}...{Fore.RESET}")
                
                try:
                    # Benchmark KEM security
                    kem_results = self.benchmark_kem_security(name, algo)
                    
                    # Add to results
                    results["kem_algorithms"].append(kem_results)
                    
                    if verbose:
                        print(f"  Public key: {kem_results['key_sizes']['public_key']} bytes")
                        print(f"  Ciphertext: {kem_results['ciphertext_size']:.1f} bytes")
                        print(f"  Quantum security: NIST Level {kem_results['quantum_security_level'].get('nist_level', 'N/A')}")
                except Exception as e:
                    if verbose:
                        print(f"{Fore.RED}Error testing {name}: {e}{Fore.RESET}")
        
        # 3. Benchmark signature algorithms
        if signature_algorithms:
            if verbose:
                print(f"\n{Style.BRIGHT}{Fore.CYAN}Testing Signature Algorithm Security Properties{Style.RESET_ALL}")
            
            for name, algo in signature_algorithms.items():
                if verbose:
                    print(f"{Fore.YELLOW}Testing {name}...{Fore.RESET}")
                
                try:
                    # Benchmark signature security
                    sig_results = self.benchmark_signature_security(name, algo)
                    
                    # Add to results
                    results["signature_algorithms"].append(sig_results)
                    
                    if verbose:
                        print(f"  Public key: {sig_results['key_sizes']['public_key']} bytes")
                        print(f"  Signature size: {sig_results['avg_signature_size']:.1f} bytes")
                        print(f"  Quantum security: NIST Level {sig_results['quantum_security_level'].get('nist_level', 'N/A')}")
                except Exception as e:
                    if verbose:
                        print(f"{Fore.RED}Error testing {name}: {e}{Fore.RESET}")
        
        if verbose:
            print(f"\n{Fore.GREEN}Quantum-Resistance Security Benchmarking completed.{Fore.RESET}")
        
        return results
    
    def save_results(self, results: Dict[str, Any], filename: str) -> None:
        """
        Save benchmark results to a file.
        
        Args:
            results: Benchmark results
            filename: Output filename
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        # Save as JSON
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to {filename}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Quantum-Resistance Security Benchmark')
    
    parser.add_argument('--hash', nargs='+', choices=list(QuantumSecurityBenchmark().hash_functions.keys()),
                      help='Hash functions to benchmark')
    
    parser.add_argument('--kem', nargs='+', choices=list(QuantumSecurityBenchmark().kem_algorithms.keys()),
                      help='KEM algorithms to benchmark')
    
    parser.add_argument('--sig', nargs='+', choices=list(QuantumSecurityBenchmark().signature_algorithms.keys()),
                      help='Signature algorithms to benchmark')
    
    parser.add_argument('--all', action='store_true',
                      help='Benchmark all algorithms')
    
    parser.add_argument('--output', '-o', type=str, default='security_benchmark_results.json',
                      help='Output file for benchmark results')
    
    args = parser.parse_args()
    
    benchmark = QuantumSecurityBenchmark()
    
    # Determine which algorithms to benchmark
    hash_names = args.hash
    kem_names = args.kem
    signature_names = args.sig
    
    if args.all:
        hash_names = None  # Benchmark all hash functions
        kem_names = None  # Benchmark all KEM algorithms
        signature_names = None  # Benchmark all signature algorithms
    
    # Run benchmarks
    results = benchmark.run_security_benchmark(
        hash_names=hash_names,
        kem_names=kem_names,
        signature_names=signature_names,
        verbose=True
    )
    
    # Save results
    benchmark.save_results(results, args.output)


if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Performance benchmarking for quantum-resistant hash functions.

This module provides comprehensive benchmarking with different input sizes,
data types, and allows comparison against standard hash functions.
"""

import os
import sys
import time
import hashlib
import argparse
import statistics
import platform
from pathlib import Path
from typing import Dict, List, Callable, Tuple, Any
import json
from datetime import datetime

# Add the parent directory to the path to ensure correct imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our hash functions
from src.quantum_hash.dirac import DiracHash
from src.quantum_hash.enhanced import QuantumEnhancedHash

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

class PerformanceBenchmark:
    """Comprehensive performance benchmark for hash functions."""
    
    def __init__(self):
        """Initialize the benchmark with hash functions to test."""
        self.hash_functions = {
            "dirac-standard": lambda data: DiracHash.hash(data, algorithm="standard"),
            "dirac-improved": lambda data: DiracHash.hash(data, algorithm="improved"),
            "dirac-grover": lambda data: DiracHash.hash(data, algorithm="grover"),
            "dirac-shor": lambda data: DiracHash.hash(data, algorithm="shor"),
            "quantum-enhanced": lambda data: QuantumEnhancedHash.hash(data),
            "sha256": lambda data: hashlib.sha256(data).digest(),
            "sha512": lambda data: hashlib.sha512(data).digest(),
        }
        
        # Try to import additional hash functions
        try:
            import blake3
            self.hash_functions["blake3"] = lambda data: blake3.blake3(data).digest()
        except ImportError:
            pass
            
        # Input data sizes (in bytes)
        self.sizes = [
            ("Empty", 0),
            ("Tiny", 64),
            ("Small", 1024),  # 1 KB
            ("Medium", 65536),  # 64 KB
            ("Large", 1048576),  # 1 MB
            ("XLarge", 16777216),  # 16 MB
        ]
        
        # Different data patterns
        self.data_types = {
            "zeros": lambda size: b"\x00" * size,
            "ones": lambda size: b"\xff" * size,
            "random": lambda size: os.urandom(size),
            "sequential": lambda size: bytes(range(min(256, size))) * (size // 256 + 1),
            "alternating": lambda size: bytes([0, 255] * (size // 2 + 1))[:size],
        }
        
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
    
    def benchmark_function(self, name: str, func: Callable, data: bytes, 
                          iterations: int = 10) -> Dict[str, Any]:
        """
        Benchmark a single hash function.
        
        Args:
            name: Name of the hash function
            func: Hash function to benchmark
            data: Input data
            iterations: Number of iterations
            
        Returns:
            Dictionary with benchmark results
        """
        # Run a warmup iteration
        _ = func(data)
        
        # Run the actual benchmark
        times = []
        for _ in range(iterations):
            start_time = time.perf_counter()
            _ = func(data)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        # Calculate statistics
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0
        
        # Calculate throughput
        if len(data) > 0:
            throughput = len(data) / avg_time / (1024 * 1024)  # MB/s
        else:
            throughput = 0
        
        return {
            "hash_function": name,
            "iterations": iterations,
            "data_size": len(data),
            "avg_time": avg_time,
            "min_time": min_time,
            "max_time": max_time,
            "std_dev": std_dev,
            "throughput": throughput,
        }
    
    def run_benchmark(self, hash_names: List[str] = None, data_types: List[str] = None,
                     sizes: List[str] = None, iterations: int = 10, 
                     verbose: bool = True) -> List[Dict[str, Any]]:
        """
        Run benchmarks for specified hash functions, data types, and sizes.
        
        Args:
            hash_names: List of hash function names to benchmark
            data_types: List of data types to use
            sizes: List of data sizes to use
            iterations: Number of iterations for each benchmark
            verbose: Whether to print progress
            
        Returns:
            List of benchmark results
        """
        # Filter hash functions if specified
        if hash_names:
            hash_functions = {name: func for name, func in self.hash_functions.items() 
                            if name in hash_names}
        else:
            hash_functions = self.hash_functions
        
        # Filter data types if specified
        if data_types:
            data_generators = {name: gen for name, gen in self.data_types.items() 
                              if name in data_types}
        else:
            data_generators = self.data_types
        
        # Filter sizes if specified
        if sizes:
            size_specs = [(name, size) for name, size in self.sizes 
                         if name in sizes]
        else:
            size_specs = self.sizes
        
        results = []
        
        # Display header
        if verbose:
            print(f"\n{Style.BRIGHT}{Fore.BLUE}Running Performance Benchmarks{Style.RESET_ALL}")
            print(f"System: {self.system_info.get('platform', 'Unknown')}")
            print(f"Processor: {self.system_info.get('cpu_model', self.system_info.get('processor', 'Unknown'))}")
            print(f"Python: {self.system_info.get('python_version', 'Unknown')}")
            print(f"Iterations per test: {iterations}")
            print("-" * 80)
        
        # Calculate total benchmarks
        total_benchmarks = len(hash_functions) * len(data_generators) * len(size_specs)
        completed = 0
        
        # Run benchmarks
        for size_name, size in size_specs:
            for data_type, data_generator in data_generators.items():
                # Generate data for this size and type
                data = data_generator(size)
                
                # Benchmark each hash function
                for hash_name, hash_func in hash_functions.items():
                    completed += 1
                    
                    if verbose:
                        print(f"\r{Fore.YELLOW}Progress: {completed}/{total_benchmarks} "
                              f"({completed/total_benchmarks*100:.1f}%) - "
                              f"Testing {hash_name} with {size_name} {data_type} data...{Fore.RESET}", 
                              end="", flush=True)
                    
                    try:
                        result = self.benchmark_function(hash_name, hash_func, data, iterations)
                        result["size_name"] = size_name
                        result["data_type"] = data_type
                        results.append(result)
                    except Exception as e:
                        if verbose:
                            print(f"\n{Fore.RED}Error benchmarking {hash_name} with {size_name} {data_type} data: {e}{Fore.RESET}")
        
        if verbose:
            print(f"\r{Fore.GREEN}Completed {completed}/{total_benchmarks} benchmarks.{Fore.RESET}{"":60}")
        
        return results
    
    def print_results(self, results: List[Dict[str, Any]], format_type: str = "detailed") -> None:
        """
        Print benchmark results in a readable format.
        
        Args:
            results: List of benchmark results
            format_type: Format type ('detailed', 'summary', or 'comparison')
        """
        if not results:
            print(f"{Fore.RED}No results to display.{Fore.RESET}")
            return
        
        if format_type == "detailed":
            # Group by size and data type
            grouped = {}
            for r in results:
                key = (r["size_name"], r["data_type"])
                if key not in grouped:
                    grouped[key] = []
                grouped[key].append(r)
            
            # Print results for each group
            for (size_name, data_type), group in sorted(grouped.items()):
                print(f"\n{Style.BRIGHT}{Fore.CYAN}=== {size_name} - {data_type} ==={Style.RESET_ALL}")
                
                # Sort by throughput (descending)
                sorted_results = sorted(group, key=lambda x: x["throughput"] if x["throughput"] > 0 else float('inf'), reverse=True)
                
                # Determine fastest for highlighting
                if sorted_results and sorted_results[0]["throughput"] > 0:
                    fastest = sorted_results[0]["hash_function"]
                else:
                    fastest = None
                
                # Print table header
                print(f"{'Hash Function':<20} {'Avg Time (s)':<12} {'Throughput (MB/s)':<18} {'Std Dev (s)':<12}")
                print("-" * 70)
                
                # Print each result
                for r in sorted_results:
                    name = r["hash_function"]
                    avg_time = f"{r['avg_time']:.6f}"
                    throughput = f"{r['throughput']:.2f}" if r["throughput"] > 0 else "N/A"
                    std_dev = f"{r['std_dev']:.6f}"
                    
                    # Highlight the fastest
                    if name == fastest:
                        print(f"{Fore.GREEN}{name:<20} {avg_time:<12} {throughput:<18} {std_dev:<12}{Fore.RESET}")
                    else:
                        print(f"{name:<20} {avg_time:<12} {throughput:<18} {std_dev:<12}")
        
        elif format_type == "summary":
            # Group by hash function and size, average across data types
            grouped = {}
            for r in results:
                key = (r["hash_function"], r["size_name"])
                if key not in grouped:
                    grouped[key] = []
                grouped[key].append(r)
            
            # Calculate average throughput for each group
            summary = {}
            for (hash_name, size_name), group in grouped.items():
                avg_throughput = statistics.mean([r["throughput"] for r in group if r["throughput"] > 0] or [0])
                if hash_name not in summary:
                    summary[hash_name] = {}
                summary[hash_name][size_name] = avg_throughput
            
            # Print summary table
            print(f"\n{Style.BRIGHT}{Fore.CYAN}Summary of Average Throughput (MB/s){Style.RESET_ALL}")
            
            # Print header
            header = "Hash Function".ljust(20)
            for size_name, _ in self.sizes:
                if any(size_name in summary[hash_name] for hash_name in summary):
                    header += f"{size_name:>12}"
            print(header)
            print("-" * (20 + 12 * sum(1 for _, _ in self.sizes)))
            
            # Print each hash function
            for hash_name in sorted(summary.keys()):
                row = hash_name.ljust(20)
                for size_name, _ in self.sizes:
                    if size_name in summary[hash_name]:
                        throughput = summary[hash_name][size_name]
                        row += f"{throughput:>12.2f}" if throughput > 0 else f"{'N/A':>12}"
                print(row)
        
        elif format_type == "comparison":
            # Group by size and data type
            grouped = {}
            for r in results:
                key = (r["size_name"], r["data_type"])
                if key not in grouped:
                    grouped[key] = {}
                grouped[key][r["hash_function"]] = r
            
            # Find SHA-256 results for comparison
            for key, group in grouped.items():
                if "sha256" in group:
                    base_result = group["sha256"]
                    base_time = base_result["avg_time"] if base_result["avg_time"] > 0 else float('inf')
                    
                    size_name, data_type = key
                    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== {size_name} - {data_type} (relative to SHA-256) ==={Style.RESET_ALL}")
                    
                    # Print table header
                    print(f"{'Hash Function':<20} {'Relative Speed':<15} {'Absolute MB/s':<15}")
                    print("-" * 50)
                    
                    # Print each result
                    for hash_name, r in sorted(group.items()):
                        if r["avg_time"] > 0:
                            rel_speed = base_time / r["avg_time"]
                            throughput = r["throughput"]
                            
                            # Format for display
                            if hash_name == "sha256":
                                rel_text = "1.00x (baseline)"
                                print(f"{Fore.YELLOW}{hash_name:<20} {rel_text:<15} {throughput:>11.2f} MB/s{Fore.RESET}")
                            else:
                                rel_text = f"{rel_speed:.2f}x " + ("faster" if rel_speed > 1 else "slower")
                                color = Fore.GREEN if rel_speed > 1 else Fore.RED
                                print(f"{hash_name:<20} {color}{rel_text:<15}{Fore.RESET} {throughput:>11.2f} MB/s")
    
    def save_results(self, results: List[Dict[str, Any]], filename: str) -> None:
        """
        Save benchmark results to a file.
        
        Args:
            results: List of benchmark results
            filename: Filename to save to
        """
        # Add system information
        output = {
            "system_info": self.system_info,
            "results": results
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"{Fore.GREEN}Results saved to {filename}{Fore.RESET}")

def main():
    parser = argparse.ArgumentParser(description="Performance Benchmark for Hash Functions")
    
    # Main arguments
    parser.add_argument("--hash-functions", "-f", nargs="+",
                      help="Hash functions to benchmark (default: all)")
    parser.add_argument("--data-types", "-d", nargs="+",
                      help="Data types to use (default: all)")
    parser.add_argument("--sizes", "-s", nargs="+",
                      help="Data sizes to benchmark (default: all)")
    parser.add_argument("--iterations", "-i", type=int, default=10,
                      help="Number of iterations for each benchmark (default: 10)")
    parser.add_argument("--format", "-m", choices=["detailed", "summary", "comparison"],
                      default="detailed", help="Output format (default: detailed)")
    parser.add_argument("--output", "-o", 
                      help="Save results to file (JSON format)")
    parser.add_argument("--quiet", "-q", action="store_true",
                      help="Don't print progress")
    
    args = parser.parse_args()
    
    # Initialize benchmark
    benchmark = PerformanceBenchmark()
    
    # List available options if requested
    print(f"{Style.BRIGHT}Available Hash Functions:{Style.RESET_ALL} {', '.join(benchmark.hash_functions.keys())}")
    print(f"{Style.BRIGHT}Available Data Types:{Style.RESET_ALL} {', '.join(benchmark.data_types.keys())}")
    print(f"{Style.BRIGHT}Available Sizes:{Style.RESET_ALL} {', '.join(name for name, _ in benchmark.sizes)}")
    
    # Validate hash functions
    if args.hash_functions:
        for func in args.hash_functions:
            if func not in benchmark.hash_functions:
                print(f"{Fore.RED}Error: Unknown hash function '{func}'{Fore.RESET}")
                return
    
    # Validate data types
    if args.data_types:
        for dtype in args.data_types:
            if dtype not in benchmark.data_types:
                print(f"{Fore.RED}Error: Unknown data type '{dtype}'{Fore.RESET}")
                return
    
    # Validate sizes
    if args.sizes:
        size_names = [name for name, _ in benchmark.sizes]
        for size in args.sizes:
            if size not in size_names:
                print(f"{Fore.RED}Error: Unknown size '{size}'{Fore.RESET}")
                return
    
    # Run benchmarks
    results = benchmark.run_benchmark(
        hash_names=args.hash_functions,
        data_types=args.data_types,
        sizes=args.sizes,
        iterations=args.iterations,
        verbose=not args.quiet
    )
    
    # Print results
    benchmark.print_results(results, format_type=args.format)
    
    # Save results if requested
    if args.output:
        benchmark.save_results(results, args.output)

if __name__ == "__main__":
    main() 
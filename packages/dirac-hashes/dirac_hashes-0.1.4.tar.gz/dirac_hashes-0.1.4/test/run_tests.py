#!/usr/bin/env python3
"""
Script to setup and run all tests for the quantum hash library.
"""

import os
import sys
import subprocess
import venv
import platform
import importlib.util
from pathlib import Path

# Add the parent directory to the path to ensure correct imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Colors for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_color(text, color):
    """Print colored text."""
    print(f"{color}{text}{Colors.NC}")

def run_command(cmd, check=True, env=None):
    """Run a shell command."""
    try:
        # Create a copy of the current environment
        cmd_env = os.environ.copy()
        # Add project root to PYTHONPATH
        if 'PYTHONPATH' in cmd_env:
            cmd_env['PYTHONPATH'] = f"{project_root}:{cmd_env['PYTHONPATH']}"
        else:
            cmd_env['PYTHONPATH'] = project_root
        
        # Update with any provided environment variables
        if env:
            cmd_env.update(env)
            
        result = subprocess.run(
            cmd, 
            shell=False,  # Set to False to avoid shell parsing issues with spaces
            check=check, 
            capture_output=True, 
            text=True,
            env=cmd_env
        )
        return result.returncode == 0, result.stdout
    except subprocess.CalledProcessError as e:
        print_color(f"Command failed: {e}", Colors.RED)
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False, str(e)

def run_python_module(module_path, args="", python_exe=sys.executable):
    """Run a Python module directly."""
    # Convert relative path to absolute path
    if not os.path.isabs(module_path):
        module_path = os.path.join(project_root, module_path)
    
    # Ensure the module exists
    if not os.path.exists(module_path):
        print_color(f"Module not found: {module_path}", Colors.RED)
        return False, f"Module not found: {module_path}"
    
    # Split the arguments into a list to avoid shell parsing issues with spaces
    cmd_args = [python_exe, module_path] + (args.split() if args else [])
    
    # Run the module using subprocess.run directly without shell=True
    try:
        # Create environment with PYTHONPATH
        env = os.environ.copy()
        if 'PYTHONPATH' in env:
            env['PYTHONPATH'] = f"{project_root}:{env['PYTHONPATH']}"
        else:
            env['PYTHONPATH'] = project_root
            
        result = subprocess.run(
            cmd_args,
            check=True,
            capture_output=True,
            text=True,
            env=env
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print_color(f"Command failed: {e}", Colors.RED)
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False, str(e)

def check_imports():
    """Check if required modules are importable."""
    try:
        # Try to import critical modules
        import unittest
        
        # Check for quantum_hash module
        try:
            from src.quantum_hash import dirac, enhanced
            print_color("All required modules found.", Colors.GREEN)
            return True
        except ImportError as e:
            print_color(f"Cannot import quantum_hash modules: {e}", Colors.RED)
            print_color("Make sure you're running from the project root directory.", Colors.YELLOW)
            return False
    except ImportError as e:
        print_color(f"Cannot import standard modules: {e}", Colors.RED)
        return False

def setup_venv():
    """Create and setup virtual environment."""
    venv_dir = os.path.join(project_root, "venv")
    
    if not os.path.exists(venv_dir):
        print_color("Creating virtual environment...", Colors.YELLOW)
        try:
            venv.create(venv_dir, with_pip=True)
        except Exception as e:
            print_color(f"Failed to create virtual environment: {e}", Colors.RED)
            print_color("Please ensure you have the venv module installed:", Colors.RED)
            print_color("  - On Debian/Ubuntu: sudo apt-get install python3-venv", Colors.RED)
            print_color("  - On Arch Linux: pacman -S python-virtualenv", Colors.RED)
            return None
    
    # Determine the path to the Python executable in the virtual environment
    if platform.system() == "Windows":
        python_path = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_path = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        python_path = os.path.join(venv_dir, "bin", "python")
        pip_path = os.path.join(venv_dir, "bin", "pip")
    
    # Check if paths exist
    if not os.path.exists(python_path):
        print_color(f"Python executable not found: {python_path}", Colors.RED)
        return None
    
    if not os.path.exists(pip_path):
        print_color(f"Pip executable not found: {pip_path}", Colors.RED)
        return None
    
    # Install dependencies
    print_color("Installing dependencies...", Colors.YELLOW)
    try:
        subprocess.run(
            [pip_path, "install", "-q", "colorama", "tabulate"],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print_color(f"Failed to install dependencies: {e}", Colors.RED)
        return None
    
    # Install the package in development mode
    print_color("Installing quantum_hash package in development mode...", Colors.YELLOW)
    try:
        # Change to project root directory
        original_dir = os.getcwd()
        os.chdir(project_root)
        
        # Install in development mode
        subprocess.run(
            [pip_path, "install", "-e", "."],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Change back to original directory
        os.chdir(original_dir)
    except subprocess.CalledProcessError as e:
        print_color(f"Failed to install quantum_hash package: {e}", Colors.RED)
        return None
    
    return python_path

def run_unit_tests(python_path=sys.executable):
    """Run unit tests."""
    print_color("\nRunning unit tests...", Colors.YELLOW)
    if check_imports():
        test_file = os.path.join(project_root, "test", "test_suite.py")
        success, output = run_python_module(test_file, python_exe=python_path)
        if success:
            print_color("Unit tests passed successfully!", Colors.GREEN)
        else:
            print_color("Some unit tests failed.", Colors.RED)
            print(output)
        return success
    return False

def run_direct_unittest():
    """Run unit tests directly using unittest module."""
    print_color("\nRunning unit tests with unittest discovery...", Colors.YELLOW)
    try:
        # Create environment with PYTHONPATH
        env = os.environ.copy()
        if 'PYTHONPATH' in env:
            env['PYTHONPATH'] = f"{project_root}:{env['PYTHONPATH']}"
        else:
            env['PYTHONPATH'] = project_root
        
        cmd_args = [sys.executable, "-m", "unittest", "discover", "-s", os.path.join(project_root, 'test')]
        
        result = subprocess.run(
            cmd_args,
            check=True,
            capture_output=True,
            text=True,
            env=env
        )
        print_color("Unit tests passed successfully!", Colors.GREEN)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print_color("Some unit tests failed.", Colors.RED)
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False, str(e)

def run_performance_benchmarks(python_path=sys.executable):
    """Run performance benchmarks."""
    print_color("\nRunning performance benchmarks...", Colors.YELLOW)
    benchmark_file = os.path.join(project_root, "test", "performance_benchmark.py")
    success, output = run_python_module(
        benchmark_file, 
        "--data-types random --sizes Small Medium --format comparison",
        python_exe=python_path
    )
    print(output)
    return success

def run_nist_tests(python_path=sys.executable):
    """Run NIST STS tests."""
    print_color("\nRunning NIST STS tests...", Colors.YELLOW)
    nist_file = os.path.join(project_root, "test", "nist_sts_tester.py")
    
    # Run avalanche tests for each hash function
    for hash_func in ["dirac-standard", "dirac-improved", "quantum-enhanced", "sha256"]:
        print_color(f"\nTesting {hash_func}...", Colors.BLUE)
        success, output = run_python_module(
            nist_file,
            f"avalanche {hash_func} --num-tests 100",
            python_exe=python_path
        )
        print(output)
    
    return True

def run_all_tests(python_path=sys.executable):
    """Run all tests in sequence."""
    print_color("\n=== Running All Quantum Hash Framework Tests ===", Colors.BLUE)
    
    tests_passed = 0
    tests_failed = 0
    
    # Core Unit Tests
    print_color("\n[1/5] Running Core Unit Tests...", Colors.YELLOW)
    if check_imports():
        test_file = os.path.join(project_root, "test", "test_suite.py")
        success, output = run_python_module(test_file, python_exe=python_path)
        if success:
            print_color("Core unit tests passed successfully!", Colors.GREEN)
            tests_passed += 1
        else:
            print_color("Some core unit tests failed.", Colors.RED)
            print(output)
            tests_failed += 1
    else:
        print_color("Failed to run tests due to missing dependencies.", Colors.RED)
        tests_failed += 1
    
    # KEM Tests
    print_color("\n[2/5] Running KEM Tests...", Colors.YELLOW)
    if check_imports():
        test_file = os.path.join(project_root, "test", "test_kem.py")
        success, output = run_python_module(test_file, python_exe=python_path)
        if success:
            print_color("KEM tests passed successfully!", Colors.GREEN)
            tests_passed += 1
        else:
            print_color("Some KEM tests failed.", Colors.RED)
            print(output)
            tests_failed += 1
    else:
        print_color("Failed to run tests due to missing dependencies.", Colors.RED)
        tests_failed += 1
    
    # Signature Tests
    print_color("\n[3/5] Running Signature Tests...", Colors.YELLOW)
    if check_imports():
        test_file = os.path.join(project_root, "test", "test_signatures.py")
        success, output = run_python_module(test_file, python_exe=python_path)
        if success:
            print_color("Signature tests passed successfully!", Colors.GREEN)
            tests_passed += 1
        else:
            print_color("Some signature tests failed.", Colors.RED)
            print(output)
            tests_failed += 1
    else:
        print_color("Failed to run tests due to missing dependencies.", Colors.RED)
        tests_failed += 1
        
    # Performance benchmarks
    print_color("\n[4/5] Running Performance Benchmarks...", Colors.YELLOW)
    if check_imports():
        test_file = os.path.join(project_root, "test", "performance_benchmark.py")
        try:
            success, output = run_python_module(test_file, python_exe=python_path)
            if success:
                print_color("Performance benchmarks completed successfully!", Colors.GREEN)
                tests_passed += 1
            else:
                print_color("Some performance benchmarks failed.", Colors.RED)
                print(output)
                tests_failed += 1
        except Exception as e:
            print_color(f"Failed to run performance benchmarks: {e}", Colors.RED)
            tests_failed += 1
    else:
        print_color("Failed to run benchmarks due to missing dependencies.", Colors.RED)
        tests_failed += 1
    
    # NIST statistical tests
    print_color("\n[5/5] Running NIST Statistical Tests...", Colors.YELLOW)
    if check_imports():
        test_file = os.path.join(project_root, "test", "nist_sts_tester.py")
        try:
            success, output = run_python_module(test_file, python_exe=python_path)
            if success:
                print_color("NIST statistical tests passed successfully!", Colors.GREEN)
                tests_passed += 1
            else:
                print_color("Some NIST statistical tests failed.", Colors.RED)
                print(output)
                tests_failed += 1
        except Exception as e:
            print_color(f"Failed to run NIST statistical tests: {e}", Colors.RED)
            tests_failed += 1
    else:
        print_color("Failed to run NIST tests due to missing dependencies.", Colors.RED)
        tests_failed += 1
    
    # Summary
    print_color("\n=== Test Suite Summary ===", Colors.BLUE)
    print_color(f"Tests passed: {tests_passed}", Colors.GREEN)
    print_color(f"Tests failed: {tests_failed}", Colors.RED if tests_failed > 0 else Colors.GREEN)
    
    return tests_failed == 0

def main():
    """Main function."""
    print_color("====================================================", Colors.BLUE)
    print_color("Quantum Hash Test Suite", Colors.BLUE)
    print_color("====================================================", Colors.BLUE)
    
    # Basic import check - more reliable than venv for direct execution
    if not check_imports():
        print_color("Attempting to set up virtual environment...", Colors.YELLOW)
        python_path = setup_venv()
        if not python_path:
            print_color("Failed to set up environment. Please run from project root.", Colors.RED)
            sys.exit(1)
    else:
        python_path = sys.executable
    
    # Show menu of available tests
    print_color("\nAvailable Test Options:", Colors.BLUE)
    print_color("1. Run Unit Tests", Colors.GREEN)
    print("   Basic unit tests and validation of hash functions")
    print_color("2. Run Performance Benchmarks", Colors.GREEN)
    print("   Benchmark hash functions with various input sizes")
    print_color("3. Run NIST STS Tests", Colors.GREEN)
    print("   Statistical randomness tests compatible with NIST STS")
    print_color("4. Run All Tests", Colors.GREEN)
    print("   Run all test types in sequence")
    print_color("0. Exit", Colors.GREEN)
    
    # Get user choice
    try:
        choice = int(input("\nEnter your choice (0-4): "))
    except ValueError:
        print_color("Invalid choice. Exiting.", Colors.RED)
        sys.exit(1)
    
    # Execute based on choice
    if choice == 1:
        run_unit_tests(python_path)
    elif choice == 2:
        run_performance_benchmarks(python_path)
    elif choice == 3:
        run_nist_tests(python_path)
    elif choice == 4:
        run_all_tests(python_path)
    elif choice == 0:
        print_color("Exiting...", Colors.BLUE)
        sys.exit(0)
    else:
        print_color("Invalid choice. Exiting.", Colors.RED)
        sys.exit(1)
    
    print_color("\nTests completed!", Colors.GREEN)

if __name__ == "__main__":
    main() 
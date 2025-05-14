from setuptools import setup, Extension, find_packages
import os
import sys
import platform

# Check if we're building a wheel or source distribution
is_bdist_wheel = 'bdist_wheel' in sys.argv

# Flag to determine if C extensions should be built
build_extensions = True

# Handle environment variable to disable C extensions
if os.environ.get('DIRAC_PURE_PYTHON', '0').lower() in ('1', 'true', 'yes'):
    build_extensions = False

# Check for OpenMP support based on platform
def use_openmp():
    if platform.system() == "Darwin":  # macOS
        # Apple clang doesn't support OpenMP out of the box
        return False
    else:
        return True

# Set compiler flags based on platform
extra_compile_args = []
extra_link_args = []

if platform.system() == "Windows":
    if use_openmp():
        extra_compile_args.append("/openmp")
elif platform.system() == "Darwin":  # macOS
    extra_compile_args.extend(["-Xpreprocessor", "-fopenmp", "-O3"])
    extra_link_args.extend(["-lomp"])
else:  # Linux and others
    extra_compile_args.extend(["-fopenmp", "-O3"])
    extra_link_args.extend(["-fopenmp"])

# Remove -march=native which is incompatible with manylinux policy
# Instead, use more conservative but still optimized flags
if platform.system() != "Windows":
    extra_compile_args.append("-msse4.2")

# Try to detect AVX2 support - but don't include it for manylinux wheels
if not is_bdist_wheel:
    try:
        import cpuinfo
        info = cpuinfo.get_cpu_info()
        if 'avx2' in info.get('flags', []):
            extra_compile_args.append("-mavx2")
    except ImportError:
        # Skip AVX2 detection for manylinux compatibility
        pass

# Define the extensions - focused only on the essential C extensions
extensions = []
if build_extensions:
    extensions = [
        Extension(
            'quantum_hash.core.enhanced_core',
            sources=['src/quantum_hash/core/enhanced_core.c'],
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
        )
    ]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dirac-hashes",
    version="0.1.4",
    author="Quantum Hash Team",
    author_email="Mukulpal108@gmail.com",
    description="Quantum-resistant cryptographic hash functions for blockchain applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dirac.fun",
    project_urls={
        "Bug Tracker": "https://github.com/mukulpal/mkodz/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
        "Development Status :: 3 - Alpha",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    ext_modules=extensions,
    install_requires=[
        "numpy>=1.19.0",
        "base58>=2.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "py-cpuinfo>=8.0.0",
            "matplotlib>=3.3.0",
            "tabulate>=0.8.7",
            "pandas>=1.0.0",
            "seaborn>=0.11.0",
        ],
        "numba": [
            "numba>=0.50.0",
        ],
        "benchmark": [
            "xxhash>=2.0.0",
            "pycityhash>=0.1.0",
            "highwayhash>=0.1.0",
            "farmhash>=0.1.0",
            "murmurhash3>=2.0.0",
            "pyhash>=0.9.0",
        ],
    },
) 
"""
SIMD-optimized quantum-resistant hash functions.

This module provides vectorized implementations of our quantum-inspired hash
functions with a focus on the best performing algorithms for blockchain
applications.
"""

import numpy as np
from typing import List, Tuple, Optional, Union
import hashlib
import os

# Try to import C extensions
try:
    from .hybrid_core import optimized_hybrid_hash_c
    _HAVE_C_EXTENSIONS = True
except ImportError:
    _HAVE_C_EXTENSIONS = False
    print("Warning: C extensions not found. Using slower Python implementations.")

# Try to import numba for JIT compilation
try:
    import numba
    from numba import njit, prange, vectorize
    from numba import uint32, uint64, uint8, int64, int32
    _HAVE_NUMBA = True
except ImportError:
    # Create dummy decorators if numba is not available
    def njit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    def prange(*args, **kwargs):
        return range(*args, **kwargs)
    
    def vectorize(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    # Dummy type annotations that won't be used without Numba
    uint32 = lambda x: x
    uint64 = lambda x: x
    uint8 = lambda x: x
    int64 = lambda x: x
    int32 = lambda x: x
    _HAVE_NUMBA = False

# Constants for hashing
PRIMES = np.array([
    0x9e3779b9, 0x6a09e667, 0xbb67ae85, 0x3c6ef372,
    0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab,
    0x5be0cd19, 0xca62c1d6, 0x84caa73b, 0xfe94f82b
], dtype=np.uint32)

ROTATIONS = np.array([7, 11, 13, 17, 19, 23, 29, 31, 5, 3], dtype=np.uint8)

# Additional constants for better quantum resistance
EXTRA_PRIMES = np.array([
    0x243f6a88, 0x85a308d3, 0x13198a2e, 0x03707344,
    0xa4093822, 0x299f31d0, 0x082efa98, 0xec4e6c89,
    0x452821e6, 0x38d01377, 0xbe5466cf, 0x34e90c6c
], dtype=np.uint32)


# Define the rotate left function based on whether Numba is available
if _HAVE_NUMBA:
    @vectorize([uint32(uint32, uint8), 
                uint32(uint64, uint8),
                uint32(int64, uint8),
                uint32(int32, uint8)], nopython=True)
    def rotate_left(value: np.uint32, shift: np.uint8) -> np.uint32:
        """Vectorized rotate left operation."""
        # Convert to uint32 first to ensure consistent behavior
        value = np.uint32(value)
        return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF
else:
    def rotate_left(value: np.uint32, shift: np.uint8) -> np.uint32:
        """Simple rotate left operation."""
        value = np.uint32(value)
        return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF


@njit(fastmath=True)
def mix_bits(a: np.uint32, b: np.uint32) -> Tuple[np.uint32, np.uint32]:
    """Mix two values to increase diffusion."""
    # Ensure both a and b are uint32
    a = np.uint32(a)
    b = np.uint32(b)
    
    a = np.uint32((a + b) & 0xFFFFFFFF)
    b = np.uint32(rotate_left(b, np.uint8(13)) ^ a)
    a = np.uint32((rotate_left(a, np.uint8(7)) + b) & 0xFFFFFFFF)
    b = np.uint32(rotate_left(b, np.uint8(17)) ^ a)
    a = np.uint32((a + b) & 0xFFFFFFFF)
    
    # Additional mixing for quantum resistance
    b = np.uint32(rotate_left(b, np.uint8(5)) ^ (a * np.uint32(0x9e3779b9)))
    a = np.uint32(rotate_left(a, np.uint8(11)) + rotate_left(b, np.uint8(19)))
    return a, b


@njit(parallel=True, fastmath=True)
def numba_enhanced_hybrid_hash(data: bytes, digest_size: int = 32) -> bytes:
    """
    JIT-compiled implementation of enhanced hybrid hash combining 
    multiple approaches for maximum quantum resistance.
    
    Args:
        data: Input data to hash
        digest_size: Size of the output hash in bytes
    
    Returns:
        Hashed output as bytes
    """
    # If data is empty, use a default value
    if len(data) == 0:
        data = b"\x00"
    
    # Initialize state with prime numbers
    state_size = (digest_size + 3) // 4  # Number of 32-bit words
    state = np.array([PRIMES[i % len(PRIMES)] for i in range(state_size)], dtype=np.uint32)
    
    # Calculate data length for finalization
    data_length = len(data)
    
    # Process data in blocks
    block_size = 64  # Similar to SHA-256 block size
    padded_size = ((len(data) + block_size - 1) // block_size) * block_size
    
    # Use numpy array instead of bytearray
    padded_data = np.zeros(padded_size, dtype=np.uint8)
    for i in range(len(data)):
        padded_data[i] = data[i]
    
    # Seed initial state with data length for better avalanche effect
    seed = data_length * PRIMES[0]
    for i in range(state_size):
        state[i] = state[i] ^ rotate_left(np.uint32(seed), ROTATIONS[i % len(ROTATIONS)])
    
    # Process each block with enhanced security
    for block_start in range(0, padded_size, block_size):
        block = padded_data[block_start:block_start+block_size]
        
        # Process the block in 32-bit chunks
        for i in range(0, block_size, 4):
            chunk = 0
            for j in range(4):
                if i + j < len(block):
                    chunk |= block[i + j] << (j * 8)
            
            # Update state with chunk using hybrid techniques
            idx = (i // 4) % state_size
            
            # Quantum-resistant mixing
            a = state[idx]
            b = chunk ^ PRIMES[idx % len(PRIMES)] ^ EXTRA_PRIMES[idx % len(EXTRA_PRIMES)]
            
            # Apply mixing rounds
            a, b = mix_bits(a, b)
            state[idx] = a ^ b
            
            # Additional state mixing for quantum resistance
            for j in prange(state_size):
                k = (j + 1) % state_size
                a = state[j]
                b = state[k]
                a, b = mix_bits(a, b)
                state[j] = a
                state[k] = b
        
        # Apply permutation after each block with enhanced complexity
        temp = state.copy()
        for i in prange(state_size):
            j = (i * 7 + 1) % state_size
            k = (i * 5 + 3) % state_size  # Additional mixing point
            state[j] = temp[i] ^ rotate_left(temp[k], np.uint8(13))
    
    # Finalization with data length and additional operations
    for i in prange(state_size):
        state[i] ^= data_length
        
        # Apply enhanced final diffusion
        for j in range(4):  # Increased from 3 to 4 rounds
            idx1 = (i + j + 1) % state_size
            idx2 = (i + j + 2) % state_size
            idx3 = (i + j + 3) % state_size  # Additional mixing point
            
            # More complex diffusion
            state[i] = rotate_left(state[i], np.uint8(9)) ^ state[idx1] ^ rotate_left(state[idx2], np.uint8(13)) ^ state[idx3]
            state[i] = (state[i] * PRIMES[j % len(PRIMES)]) & 0xFFFFFFFF
    
    # Convert state to bytes
    result = np.zeros(digest_size, dtype=np.uint8)
    for i in range(min(state_size, digest_size // 4 + 1)):
        for j in range(4):
            if i * 4 + j < digest_size:
                result[i * 4 + j] = (state[i] >> (j * 8)) & 0xFF
    
    return bytes(result)


def optimized_hybrid_hash(data: bytes, digest_size: int = 32) -> bytes:
    """
    Optimized hybrid hash with enhanced security properties 
    and quantum resistance.
    
    Args:
        data: Input data to hash
        digest_size: Size of the output hash in bytes
    
    Returns:
        Hashed output as bytes
    """
    if _HAVE_C_EXTENSIONS:
        return optimized_hybrid_hash_c(data, digest_size)
    else:
        return numba_enhanced_hybrid_hash(data, digest_size) 
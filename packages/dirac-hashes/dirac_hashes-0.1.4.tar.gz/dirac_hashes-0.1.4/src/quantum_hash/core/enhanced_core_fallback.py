"""
Pure Python fallback implementation of enhanced_core.c for systems 
where C extensions are not available or not compiled.

This module provides the same functionality as enhanced_core.c but in
pure Python, which makes it more portable but less performant.
"""

import numpy as np
import struct
import hashlib
from typing import Union, List, Tuple

# Constants
BLOCK_SIZE = 64  # Same as used in SHA-256
WORD_SIZE = 4    # 32-bit words
ROUNDS = 64      # Number of mixing rounds

# Rotation constants (same as in enhanced_core.c)
ROT_CONSTANTS = [
    7, 9, 13, 16, 19, 21, 24, 27,
    3, 5, 11, 17, 23, 29, 31, 12
]

def rotate_left(value: int, shift: int) -> int:
    """Rotate left (circular left shift) by shift bits."""
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

def mix_block(state: List[int], block: bytes) -> None:
    """Mix a 64-byte block into the state."""
    # Convert block to 16 32-bit words
    words = struct.unpack('<16I', block)
    
    # Create a temporary state array
    temp_state = state.copy()
    
    # Mix in the block data
    for i in range(ROUNDS):
        # Choose indexes for mixing (similar to enhanced_core.c implementation)
        a_idx = i % 8
        b_idx = (i + 1) % 8
        c_idx = (i + 2) % 8
        d_idx = (i + 3) % 8
        
        # Choose word for this round
        word_idx = i % 16
        
        # Update state using a non-linear mixing function
        temp_state[a_idx] = rotate_left(
            (temp_state[a_idx] + temp_state[b_idx] + words[word_idx]) & 0xFFFFFFFF, 
            ROT_CONSTANTS[i % 16]
        )
        
        # Mixing operation
        if i % 4 == 0:
            temp_state[b_idx] ^= temp_state[a_idx]
        elif i % 4 == 1:
            temp_state[b_idx] = (temp_state[b_idx] + temp_state[a_idx]) & 0xFFFFFFFF
        elif i % 4 == 2:
            temp_state[b_idx] = rotate_left(temp_state[b_idx] ^ temp_state[a_idx], ROT_CONSTANTS[(i + 4) % 16])
        else:
            temp_state[b_idx] = (temp_state[b_idx] + (~temp_state[a_idx] & 0xFFFFFFFF)) & 0xFFFFFFFF
    
    # Update original state
    for i in range(8):
        state[i] = (state[i] + temp_state[i]) & 0xFFFFFFFF

def dirac_hash(data: Union[bytes, str], digest_size: int = 32) -> bytes:
    """
    Compute the DiracHash of the input data.
    
    Args:
        data: Input data as bytes or string
        digest_size: Size of the output digest in bytes (default: 32)
        
    Returns:
        Digest as bytes
    """
    # Convert string to bytes if needed
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Initialize the state (similar to SHA-256 but with quantum-resistant values)
    state = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]
    
    # Process all complete blocks
    data_len = len(data)
    for i in range(0, data_len - data_len % BLOCK_SIZE, BLOCK_SIZE):
        mix_block(state, data[i:i+BLOCK_SIZE])
    
    # Process the final block with padding
    remaining = data_len % BLOCK_SIZE
    final_block = bytearray(data[data_len - remaining:]) if remaining > 0 else bytearray()
    
    # Add padding (similar to SHA-256 padding)
    final_block.append(0x80)  # Append a 1 bit followed by zeros
    
    # Check if we need an additional block for the length
    if len(final_block) > BLOCK_SIZE - 8:
        # Pad the current block
        final_block.extend(b'\x00' * (BLOCK_SIZE - len(final_block)))
        mix_block(state, final_block)
        # Start a new block
        final_block = bytearray(b'\x00' * (BLOCK_SIZE - 8))
    else:
        # Pad the current block
        final_block.extend(b'\x00' * (BLOCK_SIZE - 8 - len(final_block)))
    
    # Append the length in bits (big-endian, 64 bits)
    bit_length = data_len * 8
    final_block.extend(struct.pack('>Q', bit_length))
    
    # Process the final block
    mix_block(state, final_block)
    
    # Output the digest
    raw_digest = struct.pack('<8I', *state)
    
    # If the requested digest size is smaller than 32 bytes, truncate
    # If larger, then extend using the same algorithm with the digest as input
    if digest_size <= 32:
        return raw_digest[:digest_size]
    else:
        # For larger digests, we use the digest as input for another round
        # and concatenate the results
        extended_digest = bytearray(raw_digest)
        remaining = digest_size - 32
        
        # Use the current digest as input for the next round
        counter = 0
        while remaining > 0:
            # Create a new input with the digest and a counter
            counter_bytes = struct.pack('<I', counter)
            next_input = raw_digest + counter_bytes
            
            # Compute the next digest block
            next_digest = dirac_hash(next_input)
            
            # Append to the extended digest
            size_to_append = min(32, remaining)
            extended_digest.extend(next_digest[:size_to_append])
            
            # Update the counter and remaining bytes
            counter += 1
            remaining -= size_to_append
        
        return bytes(extended_digest) 
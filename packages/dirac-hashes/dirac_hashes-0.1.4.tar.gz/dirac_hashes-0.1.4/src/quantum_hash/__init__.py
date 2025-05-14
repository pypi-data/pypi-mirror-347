"""
Quantum Hash: A lightweight quantum-resistant hash module.

This module provides hash functions designed to be resistant to
quantum computing attacks while maintaining good performance.
"""

from .dirac import DiracHash
from .enhanced import QuantumEnhancedHash

__version__ = "0.1.4"
__all__ = ['DiracHash', 'QuantumEnhancedHash']

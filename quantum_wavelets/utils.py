"""
Utility functions for quantum wavelet transforms.

This module contains internal helper functions that are
not part of the public API.
"""

import numpy as np


def is_power_of_two(n: int) -> bool:
    """
    Check whether an integer is a power of two.

    Args:
        n (int): Integer to check.

    Returns:
        bool: True if n is a power of two, False otherwise.
    """
    return n > 0 and (n & (n - 1)) == 0


def classical_haar_matrix(n: int) -> np.ndarray:
    """
    Construct the classical Haar matrix of size 2^n × 2^n.

    This function is intended for testing and verification only.

    Args:
        n (int): Number of qubits / levels.

    Returns:
        np.ndarray: Haar transform matrix.
    """
    if n == 1:
        return np.array([[1, 1], [1, -1]]) / np.sqrt(2)

    H_prev = classical_haar_matrix(n - 1)
    I = np.eye(2 ** (n - 1))

    top = np.kron(H_prev, [1, 1])
    bottom = np.kron(I, [1, -1])

    return np.vstack([top, bottom]) / np.sqrt(2)

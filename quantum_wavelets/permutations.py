# Copyright 2026
# Apache License 2.0
"""
Quantum permutation operators used in quantum wavelet transforms.

Implements:
- Perfect Shuffle permutation Π_{2^n}
- Bit-Reversal permutation P_{2^n}

These operators are fundamental building blocks for
quantum Haar and Daubechies wavelet transforms.
"""

import functools
import numpy as np

from pennylane import math
from pennylane.capture import enabled
from pennylane.control_flow import for_loop
from pennylane.decomposition import add_decomps, register_resources
from pennylane.operation import Operation
from pennylane.ops import SWAP
from pennylane.wires import Wires, WiresLike


# ============================================================
# Perfect Shuffle Π_{2^n}
# ============================================================

class PerfectShuffle(Operation):
    r"""
    PerfectShuffle(wires)

    Implements the perfect shuffle permutation Π_{2^n}:

        |a_{n-1} a_{n-2} ... a_1 a_0⟩ →
        |a_0 a_{n-1} a_{n-2} ... a_1⟩

    This corresponds to a left cyclic shift of qubits.
    """

    grad_method = None
    resource_keys = {"num_wires"}

    def __init__(self, wires: WiresLike, id=None):
        wires = Wires(wires)
        self.hyperparameters["n_wires"] = len(wires)
        super().__init__(wires=wires, id=id)

    def _flatten(self):
        return tuple(), (self.wires, tuple())

    @property
    def num_params(self):
        return 0

    def decomposition(self):
        return self.compute_decomposition(wires=self.wires)

    # --- Matrix (for verification only) ---
    @staticmethod
    @functools.lru_cache
    def compute_matrix(n_wires):
        N = 2**n_wires
        P = np.zeros((N, N))

        for i in range(N):
            bits = format(i, f"0{n_wires}b")
            j = int(bits[-1] + bits[:-1], 2)
            P[j, i] = 1

        return P

    # --- Gate decomposition ---
    @staticmethod
    def compute_decomposition(wires: WiresLike):
        wires = Wires(wires)
        ops = []

        for i in range(len(wires) - 1):
            ops.append(SWAP(wires=[wires[i], wires[i + 1]]))

        return ops

    # --- qfunc decomposition ---
    @staticmethod
    def compute_qfunc_decomposition(*wires, n_wires):
        wires = math.array(wires, like="jax")

        @for_loop(n_wires - 1)
        def swaps(i):
            SWAP(wires=[wires[i], wires[i + 1]])

        swaps()

    @property
    def resource_params(self):
        return {"num_wires": len(self.wires)}


# ============================================================
# Bit-Reversal P_{2^n}
# ============================================================

class BitReversal(Operation):
    r"""
    BitReversal(wires)

    Implements the bit-reversal permutation P_{2^n}:

        |a_{n-1} a_{n-2} ... a_1 a_0⟩ →
        |a_0 a_1 ... a_{n-2} a_{n-1}⟩

    This reverses the order of qubits.
    """

    grad_method = None
    resource_keys = {"num_wires"}

    def __init__(self, wires: WiresLike, id=None):
        wires = Wires(wires)
        self.hyperparameters["n_wires"] = len(wires)
        super().__init__(wires=wires, id=id)

    def _flatten(self):
        return tuple(), (self.wires, tuple())

    @property
    def num_params(self):
        return 0

    def decomposition(self):
        return self.compute_decomposition(wires=self.wires)

    # --- Matrix (for verification only) ---
    @staticmethod
    @functools.lru_cache
    def compute_matrix(n_wires):
        N = 2**n_wires
        P = np.zeros((N, N))

        for i in range(N):
            bits = format(i, f"0{n_wires}b")
            j = int(bits[::-1], 2)
            P[j, i] = 1

        return P

    # --- Gate decomposition ---
    @staticmethod
    def compute_decomposition(wires: WiresLike):
        wires = Wires(wires)
        ops = []

        n = len(wires)
        for i in range(n // 2):
            ops.append(SWAP(wires=[wires[i], wires[n - i - 1]]))

        return ops

    # --- qfunc decomposition ---
    @staticmethod
    def compute_qfunc_decomposition(*wires, n_wires):
        wires = math.array(wires, like="jax")

        @for_loop(n_wires // 2)
        def swaps(i):
            SWAP(wires=[wires[i], wires[n_wires - i - 1]])

        swaps()

    @property
    def resource_params(self):
        return {"num_wires": len(self.wires)}


# ============================================================
# Resource registration
# ============================================================

def _perfect_shuffle_resources(num_wires):
    return {SWAP: num_wires - 1}


def _bit_reversal_resources(num_wires):
    return {SWAP: num_wires // 2}


@register_resources(_perfect_shuffle_resources)
def _perfect_shuffle_decomp(wires: WiresLike, n_wires, **__):

    @for_loop(n_wires - 1)
    def swaps(i):
        SWAP(wires=[wires[i], wires[i + 1]])

    swaps()


@register_resources(_bit_reversal_resources)
def _bit_reversal_decomp(wires: WiresLike, n_wires, **__):

    @for_loop(n_wires // 2)
    def swaps(i):
        SWAP(wires=[wires[i], wires[n_wires - i - 1]])

    swaps()


add_decomps(PerfectShuffle, _perfect_shuffle_decomp)
add_decomps(BitReversal, _bit_reversal_decomp)

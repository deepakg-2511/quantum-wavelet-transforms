# Copyright 2026
# Apache License 2.0
"""
Quantum Haar Wavelet Transform (QHWT).

Implements the orthonormal Haar wavelet transform as a PennyLane Operation.
The circuit uses only Hadamard gates and Perfect Shuffle permutations,
following the factorization used in quantum wavelet literature.
"""

import functools
import numpy as np

from pennylane import math
from pennylane.capture import enabled
from pennylane.control_flow import for_loop
from pennylane.decomposition import add_decomps, register_resources
from pennylane.operation import Operation
from pennylane.ops import Hadamard
from pennylane.wires import Wires, WiresLike

from quantum_wavelets.permutations import PerfectShuffle


class HaarWavelet(Operation):
    r"""
    HaarWavelet(wires)

    Apply the quantum Haar wavelet transform (QHWT) on ``n = len(wires)`` qubits.

    The transform is implemented via a multiscale factorization:
    at each scale, Hadamards are applied to a subset of wires followed by
    a perfect shuffle permutation.
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

    # ------------------------------------------------------------------
    # Matrix (verification only)
    # ------------------------------------------------------------------
    @staticmethod
    @functools.lru_cache
    def compute_matrix(n_wires):
        """Return the exact Haar matrix of size 2^n × 2^n (for testing)."""
        N = 2**n_wires

        def haar_recursive(n):
            if n == 1:
                return np.array([[1, 1], [1, -1]]) / np.sqrt(2)

            H_prev = haar_recursive(n - 1)
            I = np.eye(2 ** (n - 1))

            top = np.kron(H_prev, [1, 1])
            bottom = np.kron(I, [1, -1])

            return np.vstack([top, bottom]) / np.sqrt(2)

        return haar_recursive(n_wires)

    # ------------------------------------------------------------------
    # Gate-level decomposition
    # ------------------------------------------------------------------
    @staticmethod
    def compute_decomposition(wires: WiresLike):
        """
        Decompose the Haar wavelet transform into Hadamards and PerfectShuffles.
        """
        wires = Wires(wires)
        n = len(wires)

        ops = []

        for level in range(n):
            # Apply Hadamard on the last (n - level) wires
            for w in wires[level:]:
                ops.append(Hadamard(w))

            # Apply perfect shuffle on all wires
            ops.append(PerfectShuffle(wires=wires))

        return ops

    # ------------------------------------------------------------------
    # qfunc decomposition (for JAX / capture)
    # ------------------------------------------------------------------
    @staticmethod
    def compute_qfunc_decomposition(*wires, n_wires):
        wires = math.array(wires, like="jax")

        @for_loop(n_wires)
        def outer(level):

            @for_loop(n_wires - level)
            def hadamards(i):
                Hadamard(wires[level + i])

            hadamards()

            PerfectShuffle(wires=wires)

        outer()

    @property
    def resource_params(self):
        return {"num_wires": len(self.wires)}


# ----------------------------------------------------------------------
# Resource counting
# ----------------------------------------------------------------------
def _haar_resources(num_wires):
    # At level k: (n-k) Hadamards, and one PerfectShuffle
    return {
        Hadamard: num_wires * (num_wires + 1) // 2,
        PerfectShuffle: num_wires,
    }


@register_resources(_haar_resources)
def _haar_decomposition(wires: WiresLike, n_wires, **__):

    @for_loop(n_wires)
    def outer(level):

        @for_loop(n_wires - level)
        def hadamards(i):
            Hadamard(wires[level + i])

        hadamards()

        PerfectShuffle(wires=wires)

    outer()


add_decomps(HaarWavelet, _haar_decomposition)

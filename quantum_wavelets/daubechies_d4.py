"""
Quantum Daubechies D4 Wavelet Transform.

Implements the Daubechies D4 quantum wavelet transform using
fixed local unitaries (C0, C1) and PerfectShuffle permutations.
"""

import functools
import numpy as np

from pennylane import math
from pennylane.capture import enabled
from pennylane.control_flow import for_loop
from pennylane.decomposition import add_decomps, register_resources
from pennylane.operation import Operation
from pennylane.ops import QubitUnitary
from pennylane.wires import Wires, WiresLike

from quantum_wavelets.permutations import PerfectShuffle


# ----------------------------------------------------------------------
# Fixed Daubechies D4 kernels
# ----------------------------------------------------------------------

_sqrt3 = np.sqrt(3)

_alpha = np.arccos((1 + _sqrt3) / 4)
_beta  = np.arccos((3 + _sqrt3) / 4)

C0 = np.array([
    [np.cos(_alpha),  np.sin(_alpha)],
    [np.sin(_alpha), -np.cos(_alpha)]
])

C1 = np.array([
    [np.cos(_beta),  np.sin(_beta)],
    [np.sin(_beta), -np.cos(_beta)]
])


class DaubechiesD4(Operation):
    r"""
    DaubechiesD4(wires)

    Apply the quantum Daubechies D4 wavelet transform on ``n`` qubits.

    The transform is constructed from:
    - fixed single-qubit unitaries C0 and C1,
    - applied in an alternating block-diagonal pattern,
    - interleaved with PerfectShuffle permutations.
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

    # ------------------------------------------------------------------
    # Decomposition entry point
    # ------------------------------------------------------------------
    def decomposition(self):
        return self.compute_decomposition(wires=self.wires)

    # ------------------------------------------------------------------
    # Matrix (verification only, small n)
    # ------------------------------------------------------------------
    @staticmethod
    @functools.lru_cache
    def compute_matrix(n_wires):
        """
        Construct the full Daubechies D4 matrix (for testing only).

        NOTE: This is exponential in size and should only be used
        for small n.
        """
        dim = 2**n_wires
        U = np.eye(dim)

        # Build matrix via circuit simulation
        import pennylane as qml
        dev = qml.device("default.qubit", wires=n_wires)

        @qml.qnode(dev)
        def circuit():
            DaubechiesD4(wires=range(n_wires))
            return qml.state()

        U = qml.matrix(circuit)()
        return U

    # ------------------------------------------------------------------
    # Gate-level decomposition
    # ------------------------------------------------------------------
    @staticmethod
    def compute_decomposition(wires: WiresLike):
        """
        Decompose the Daubechies D4 transform into C0/C1 unitaries
        and PerfectShuffle permutations.
        """
        wires = Wires(wires)
        n = len(wires)

        ops = []

        # Number of layers = n - 1
        for level in range(n - 1):

            # Active wires at this scale
            active = wires[level:]

            for idx, wire in enumerate(active):
                if idx % 2 == 0:
                    ops.append(QubitUnitary(C0, wires=[wire]))
                else:
                    ops.append(QubitUnitary(C1, wires=[wire]))

            # Shuffle all wires
            ops.append(PerfectShuffle(wires=wires))

        return ops

    # ------------------------------------------------------------------
    # qfunc decomposition (JAX / capture compatible)
    # ------------------------------------------------------------------
    @staticmethod
    def compute_qfunc_decomposition(*wires, n_wires):
        wires = math.array(wires, like="jax")

        @for_loop(n_wires - 1)
        def outer(level):

            @for_loop(n_wires - level)
            def inner(i):
                wire = wires[level + i]

                if i % 2 == 0:
                    QubitUnitary(C0, wires=[wire])
                else:
                    QubitUnitary(C1, wires=[wire])

            inner()
            PerfectShuffle(wires=wires)

        outer()

    @property
    def resource_params(self):
        return {"num_wires": len(self.wires)}


# ----------------------------------------------------------------------
# Resource counting (coarse)
# ----------------------------------------------------------------------
def _d4_resources(num_wires):
    return {
        QubitUnitary: num_wires * (num_wires - 1),
        PerfectShuffle: num_wires - 1,
    }


@register_resources(_d4_resources)
def _d4_decomposition(wires: WiresLike, n_wires, **__):

    @for_loop(n_wires - 1)
    def outer(level):

        @for_loop(n_wires - level)
        def inner(i):
            if i % 2 == 0:
                QubitUnitary(C0, wires=[wires[level + i]])
            else:
                QubitUnitary(C1, wires=[wires[level + i]])

        inner()
        PerfectShuffle(wires=wires)

    outer()


add_decomps(DaubechiesD4, _d4_decomposition)

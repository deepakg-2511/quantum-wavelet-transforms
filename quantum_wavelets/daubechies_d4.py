import numpy as np
import pennylane as qml
from pennylane.operation import Operation
from pennylane.wires import Wires

from quantum_wavelets.permutations import PerfectShuffle

# ============================================================
# Daubechies D4 2-qubit kernel (unitary, det = +1)
# ============================================================

SQRT2 = np.sqrt(2)
SQRT3 = np.sqrt(3)

h0 = (1 + SQRT3) / (4 * SQRT2)
h1 = (3 + SQRT3) / (4 * SQRT2)
h2 = (3 - SQRT3) / (4 * SQRT2)
h3 = (1 - SQRT3) / (4 * SQRT2)

UD4 = np.array(
    [
        [ h0,  h1,  h2,  h3],
        [ h3, -h2,  h1, -h0],
        [ h2,  h3, -h0, -h1],
        [ h1, -h0, -h3,  h2],
    ],
    dtype=complex,
)

# Sanity check (optional, safe to keep)
# assert np.allclose(UD4.conj().T @ UD4, np.eye(4))
# assert np.isclose(np.linalg.det(UD4), 1.0)


# ============================================================
# General Daubechies D4 Transform  D_{2^n}^4
# ============================================================

class DaubechiesD4(Operation):
    r"""
    General Daubechies D4 quantum wavelet transform :math:`D_{2^n}^4`.

    Implements the multiresolution construction of
    Fijany & Williams (1998) using:

    - local 2-qubit Daubechies D4 kernels
    - perfect-shuffle permutations
    - scale reduction by keeping low-frequency wires

    Works for any number of qubits n >= 2.
    """

    num_params = 0
    grad_method = None

    def __init__(self, wires, id=None):
        wires = Wires(wires)

        if len(wires) < 2:
            raise ValueError("DaubechiesD4 requires at least 2 qubits.")

        super().__init__(wires=wires, id=id)

    # --------------------------------------------------------
    # Decomposition (this is the ONLY thing PennyLane needs)
    # --------------------------------------------------------
    @staticmethod
    def compute_decomposition(*params, wires, **kwargs):
        """
        Multiscale Daubechies D4 decomposition.

        IMPORTANT:
        - Signature MUST accept *params and **kwargs
        - Do NOT introduce custom hyperparameters here
        """

        wires = Wires(wires)
        ops = []

        active_wires = list(wires)

        # Multiresolution stages
        while len(active_wires) >= 2:

            # 1. Apply D4 kernels on adjacent pairs
            for i in range(0, len(active_wires) - 1, 2):
                ops.append(
                    qml.QubitUnitary(
                        UD4,
                        wires=[active_wires[i], active_wires[i + 1]],
                    )
                )

            # 2. Perfect shuffle permutation
            ops.append(PerfectShuffle(wires=active_wires))

            # 3. Keep low-frequency half (even indices)
            active_wires = active_wires[::2]

        return ops

    # --------------------------------------------------------
    # Adjoint (inverse transform)
    # --------------------------------------------------------
    def adjoint(self):
        return qml.adjoint(DaubechiesD4)(wires=self.wires)

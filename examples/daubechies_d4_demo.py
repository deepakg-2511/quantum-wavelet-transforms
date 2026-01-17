"""
Daubechies D4 Quantum Wavelet Transform demo.

This example demonstrates:
1. Application of the Daubechies D4 QWT on n qubits
2. Verification of state normalization
3. Extraction and unitarity check of the full transform matrix
"""

import numpy as np
import pennylane as qml

from quantum_wavelets.daubechies_d4 import DaubechiesD4


def run_state_demo(n_wires=3):
    """Apply D4 wavelet transform to a basis state."""
    dev = qml.device("default.qubit", wires=n_wires)

    @qml.qnode(dev)
    def circuit():
        # Example basis state |010...0>
        basis = np.zeros(n_wires, dtype=int)
        basis[1] = 1
        qml.BasisState(basis, wires=range(n_wires))

        DaubechiesD4(wires=range(n_wires))
        return qml.state()

    state = circuit()

    print("=" * 60)
    print(f"Daubechies D4 QWT on {n_wires} qubits")
    print("Final statevector:")
    print(state)
    print("State norm:", np.linalg.norm(state))
    print("=" * 60)


def run_matrix_demo(n_wires=3):
    """Extract and verify the full D4 transform matrix."""
    dev = qml.device("default.qubit", wires=n_wires)

    @qml.qnode(dev)
    def circuit():
        DaubechiesD4(wires=range(n_wires))
        return qml.state()

    U = qml.matrix(circuit)()

    print("Full D4 transform matrix shape:", U.shape)
    print("Unitary check (U†U = I):",
          np.allclose(U.conj().T @ U, np.eye(2**n_wires)))


if __name__ == "__main__":
    run_state_demo(n_wires=3)
    run_matrix_demo(n_wires=3)

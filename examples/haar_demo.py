"""
Example: Quantum Haar Wavelet Transform

This script demonstrates how to apply the HaarWavelet operator
to a simple quantum state using PennyLane.
"""

import pennylane as qml
import numpy as np

from quantum_wavelets.haar import HaarWavelet


def main():
    n_wires = 3
    wires = list(range(n_wires))

    dev = qml.device("default.qubit", wires=n_wires)

    @qml.qnode(dev)
    def circuit():
        # Prepare a basis state |100>
        qml.BasisState(np.array([1, 0, 0]), wires=wires)

        # Apply the Quantum Haar Wavelet Transform
        HaarWavelet(wires=wires)

        return qml.state(), qml.probs(wires=wires)

    state, probs = circuit()

    print("Final statevector:")
    print(state)

    print("\nMeasurement probabilities:")
    print(probs)

    print("\nCircuit:")
    print(qml.draw(circuit)())


if __name__ == "__main__":
    main()

import numpy as np
import pennylane as qml
from quantum_wavelets.daubechies_d4 import DaubechiesD4


def test_d4_unitary_n2():
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit():
        DaubechiesD4(wires=[0, 1])
        return qml.state()

    U = qml.matrix(circuit)()
    assert np.allclose(U.conj().T @ U, np.eye(4))


def test_d4_unitary_n3():
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        DaubechiesD4(wires=[0, 1, 2])
        return qml.state()

    U = qml.matrix(circuit)()
    assert np.allclose(U.conj().T @ U, np.eye(8))


def test_d4_norm_preserved():
    dev = qml.device("default.qubit", wires=4)

    @qml.qnode(dev)
    def circuit():
        qml.BasisState(np.array([1, 0, 1, 0]), wires=[0, 1, 2, 3])
        DaubechiesD4(wires=[0, 1, 2, 3])
        return qml.state()

    state = circuit()
    assert np.isclose(np.linalg.norm(state), 1.0)

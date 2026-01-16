import numpy as np
import pennylane as qml

from quantum_wavelets.permutations import PerfectShuffle, BitReversal


def test_perfect_shuffle_unitary():
    """PerfectShuffle should be unitary."""
    n = 3
    wires = list(range(n))

    U = qml.matrix(PerfectShuffle(wires=wires))
    I = np.eye(2**n)

    assert np.allclose(U.conj().T @ U, I)


def test_bit_reversal_unitary():
    """BitReversal should be unitary."""
    n = 3
    wires = list(range(n))

    U = qml.matrix(BitReversal(wires=wires))
    I = np.eye(2**n)

    assert np.allclose(U.conj().T @ U, I)


def test_perfect_shuffle_action_on_basis():
    """
    Test PerfectShuffle action on a computational basis state.

    |100⟩ → |010⟩ under perfect shuffle.
    """
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        qml.BasisState(np.array([1, 0, 0]), wires=[0, 1, 2])
        PerfectShuffle(wires=[0, 1, 2])
        return qml.state()

    state = circuit()

    expected = np.zeros(8)
    expected[2] = 1.0  # |010⟩

    assert np.allclose(state, expected)


def test_bit_reversal_action_on_basis():
    """
    Test BitReversal action on a computational basis state.

    |100⟩ → |001⟩ under bit reversal.
    """
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        qml.BasisState(np.array([1, 0, 0]), wires=[0, 1, 2])
        BitReversal(wires=[0, 1, 2])
        return qml.state()

    state = circuit()

    expected = np.zeros(8)
    expected[1] = 1.0  # |001⟩

    assert np.allclose(state, expected)


def test_permutation_matrix_vs_circuit():
    """
    Compare matrix and circuit implementations for PerfectShuffle.
    """
    n = 3
    wires = list(range(n))

    dev = qml.device("default.qubit", wires=n)

    x = np.zeros(2**n)
    x[4] = 1.0  # |100⟩

    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(x, wires=wires)
        PerfectShuffle(wires=wires)
        return qml.state()

    state_circuit = circuit()
    U = PerfectShuffle.compute_matrix(n)
    state_matrix = U @ x

    assert np.allclose(state_circuit, state_matrix)

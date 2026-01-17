import numpy as np
import pennylane as qml

from quantum_wavelets.haar import HaarWavelet


def test_haar_unitary():
    """Test that HaarWavelet is unitary."""
    n = 3
    wires = list(range(n))

    U = qml.matrix(HaarWavelet(wires=wires))
    I = np.eye(2**n)

    assert np.allclose(U.conj().T @ U, I)


def test_haar_inverse_identity():
    """Test that Haar followed by its adjoint is identity."""
    n = 3
    wires = list(range(n))

    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.BasisState(np.array([1, 0, 0]), wires=wires)
        HaarWavelet(wires=wires)
        qml.adjoint(HaarWavelet)(wires=wires)
        return qml.state()

    state = circuit()
    expected = np.zeros(2**n)
    expected[4] = 1.0  # |100⟩

    assert np.allclose(state, expected)


def test_haar_matches_matrix_small_n():
    """Compare circuit output with explicit Haar matrix (n=2)."""
    n = 2
    wires = list(range(n))

    dev = qml.device("default.qubit", wires=n)

    x = np.array([1.0, 0.0, 0.0, 0.0])

    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(x, wires=wires)
        HaarWavelet(wires=wires)
        return qml.state()

    state_circuit = circuit()

    U = HaarWavelet.compute_matrix(n)
    state_matrix = U @ x

    assert np.allclose(state_circuit, state_matrix)

# Quantum Haar Wavelet Transform

The Haar wavelet is the simplest orthonormal wavelet and serves as the
foundation for more advanced wavelet families.

---

## 1. Classical Haar Transform

The classical Haar transform computes:
- Pairwise averages (low-frequency components)
- Pairwise differences (high-frequency components)

This process is applied recursively to achieve multiscale decomposition.

---

## 2. Haar Wavelet as a Quantum Operator

In the quantum setting, the Haar transform becomes a **unitary operator**
acting on a register of qubits.

For `n` qubits, the quantum Haar wavelet transform can be factorized as:

\[
H_{2^n}
=
\prod_{k=0}^{n-1}
\left(
(I_{2^k} \otimes H^{\otimes (n-k)})
\cdot \Pi_{2^n}
\right)
\]

where:
- \(H\) is the Hadamard gate
- \(\Pi_{2^n}\) is the perfect shuffle permutation

---

## 3. Circuit Interpretation

At each scale:
1. Hadamard gates mix amplitudes locally
2. Perfect shuffle reorders qubits to expose coarser scales

This alternation produces a multiresolution analysis entirely within
unitary quantum mechanics.

---

## 4. Implementation in This Repository

The Haar wavelet is implemented as a PennyLane `Operation`:

```python
from quantum_wavelets.haar import HaarWavelet
qml.HaarWavelet(wires=[0,1,2])

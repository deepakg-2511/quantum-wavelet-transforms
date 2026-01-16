# Quantum Permutation Operators

Permutation operators play a central role in quantum wavelet transforms.
Unlike classical algorithms, data movement in quantum circuits is costly
and must be carefully structured.

---

## 1. Perfect Shuffle (Π₂ⁿ)

The perfect shuffle permutation maps:

\[
|a_{n-1} a_{n-2} \dots a_0\rangle
\;\longrightarrow\;
|a_0 a_{n-1} a_{n-2} \dots a_1\rangle
\]

This corresponds to a cyclic left shift of qubits.

In circuits, Π₂ⁿ is implemented using a nearest-neighbor SWAP network.

---

## 2. Bit-Reversal (P₂ⁿ)

The bit-reversal permutation maps:

\[
|a_{n-1} a_{n-2} \dots a_0\rangle
\;\longrightarrow\;
|a_0 a_1 \dots a_{n-2} a_{n-1}\rangle
\]

Bit reversal appears in:
- Quantum Fourier Transform
- FFT-based wavelet constructions

---

## 3. Why Permutations Matter

The central result of Fijany & Williams is that:

> The computational complexity of quantum wavelet transforms is dominated
> by permutation operators, not by local unitaries.

Efficient quantum wavelet algorithms therefore depend on explicit,
gate-level constructions of these permutations.

---

## 4. Implementation in This Repository

This repository provides:
- `PerfectShuffle` as a PennyLane `Operation`
- `BitReversal` as a PennyLane `Operation`

Both:
- Are parameter-free
- Use only SWAP gates
- Have explicit resource accounting

---

## 5. Reference

- Fijany, A. and Williams, C. P., *Quantum Wavelet Transforms*, 1998
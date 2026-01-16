# Quantum Wavelet Transforms — Theory Overview

This repository implements **quantum wavelet transforms (QWTs)** as explicit
quantum circuits, following the seminal work:

> A. Fijany and C. P. Williams  
> *Quantum Wavelet Transforms: Fast Algorithms and Complete Circuits*, 1998.

Quantum wavelet transforms provide a multiscale alternative to the Quantum
Fourier Transform (QFT), enabling hierarchical representations of quantum data.

---

## 1. Motivation

The Quantum Fourier Transform is widely available in quantum software libraries,
yet many applications in signal processing, numerical analysis, and machine
learning rely on **wavelets**, not Fourier modes.

Wavelets provide:
- Locality in both scale and position
- Sparse representations for structured signals
- Multiresolution analysis

Quantum wavelet transforms aim to replicate these advantages within a
fully unitary, gate-based quantum framework.

---

## 2. Structure of Quantum Wavelet Transforms

A quantum wavelet transform has two essential components:

1. **Local unitary kernels**
   - Haar: Hadamard gates
   - Daubechies: small fixed unitaries (e.g., C₀, C₁)

2. **Permutation operators**
   - Perfect shuffle (Π₂ⁿ)
   - Bit-reversal (P₂ⁿ)
   - Cyclic down-shift (Q₂ⁿ)

The key insight of Fijany & Williams is that **permutations dominate the
quantum complexity**, not the local unitaries.

---

## 3. Haar vs Daubechies Wavelets

### Haar Wavelets
- Simplest orthonormal wavelet
- Compact support of length 2
- Quantum implementation uses:
  - Hadamard gates
  - Perfect shuffle permutations
- Efficient and fully recursive

### Daubechies Wavelets (D4)
- Higher-order wavelets with better smoothness
- Compact support of length 4
- Require:
  - Two fixed 2×2 unitaries
  - Nontrivial permutation operators
- Multiple quantum implementations exist:
  arithmetic-based, FFT-based, recursive

---

## 4. Quantum Implementability

A quantum wavelet transform must satisfy:
- Unitarity
- Polynomial gate complexity
- Efficient circuit depth

The paper demonstrates that both Haar and Daubechies D(4) wavelets meet
these requirements when properly factorized.

This repository implements these factorizations directly at the gate level.

---

## 5. Scope of This Repository

Currently implemented:
- Perfect shuffle and bit-reversal permutations
- Quantum Haar Wavelet Transform (QHWT)

Planned:
- Quantum Daubechies D(4) Wavelet Transform
- Multiple circuit constructions (FFT-based, recursive)

---

## 6. Reference

If you use this code in academic work, please cite:


# Quantum Wavelet Transforms

Quantum circuit implementations of **quantum wavelet transforms (QWTs)**,
with a focus on **explicit, gate-level constructions** suitable for modern
quantum software frameworks such as PennyLane.

This project is based on the seminal paper:

> **A. Fijany and C. P. Williams**  
> *Quantum Wavelet Transforms: Fast Algorithms and Complete Circuits*, 1998

---

## Motivation

The **Quantum Fourier Transform (QFT)** is a core primitive in quantum computing
and is widely available in quantum libraries. However, many applications in:

- signal processing  
- numerical analysis  
- multiscale PDE solvers  
- quantum machine learning  

rely more naturally on **wavelets** than on Fourier modes.

Wavelets provide:
- locality in both scale and position,
- multiresolution analysis,
- sparse representations for structured data.

Quantum wavelet transforms aim to bring these advantages into a **fully unitary,
quantum-circuit-based framework**.

---

## Key Idea

A quantum wavelet transform consists of two fundamentally different components:

1. **Local unitary kernels**
   - Haar: Hadamard gates
   - Daubechies: fixed small unitaries (e.g., C₀, C₁)

2. **Permutation operators**
   - Perfect shuffle (Π₂ⁿ)
   - Bit reversal (P₂ⁿ)
   - Cyclic down-shift (Q₂ⁿ)

A central result of Fijany & Williams is that:

> **The quantum complexity of wavelet transforms is dominated by permutation
> operators, not by the local unitaries.**

This repository explicitly implements these permutations as quantum circuits.

---

## Current Features

✔ Perfect Shuffle permutation (Π₂ⁿ)  
✔ Bit-Reversal permutation (P₂ⁿ)  
✔ Quantum Haar Wavelet Transform (QHWT)  
✔ PennyLane `Operation` implementations  
✔ Fully unitary, parameter-free operators  
✔ Automated tests and runnable examples  

---

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/deepakg-2511/quantum-wavelet-transforms.git
cd quantum-wavelet-transforms
pip install -e .


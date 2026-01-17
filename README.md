# Quantum Wavelet Transforms

Quantum circuit implementations of **quantum wavelet transforms (QWTs)**,
with a focus on **explicit, gate-level constructions** suitable for modern
quantum software frameworks such as **PennyLane**.

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

- locality in both **scale** and **position**  
- **multiresolution analysis**  
- sparse representations for structured data  

Quantum wavelet transforms aim to bring these advantages into a **fully unitary,
quantum-circuit-based framework**.

---

## Key Idea

A quantum wavelet transform consists of two fundamentally different components:

1. **Local unitary kernels**
   - Haar: Hadamard-based 2×2 unitaries
   - Daubechies D4: fixed 4×4 unitaries acting on qubit pairs

2. **Permutation operators**
   - Perfect shuffle (Π₂ⁿ)
   - Bit reversal (P₂ⁿ)
   - Cyclic down-shift (Q₂ⁿ)

A central result of Fijany & Williams is that:

> **The quantum complexity of wavelet transforms is dominated by permutation
> operators, not by the local unitaries.**

This repository explicitly implements these permutation operators and combines
them with local wavelet kernels to build **multiscale quantum wavelet circuits**.

---

## Current Features

✔ Perfect Shuffle permutation (Π₂ⁿ)  
✔ Bit-Reversal permutation (P₂ⁿ)  
✔ Quantum Haar Wavelet Transform (QHWT)  
✔ **Daubechies D4 Quantum Wavelet Transform (general n-qubit)**  
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
```

---

## Example Usage

### Haar Wavelet Transform

```python
import pennylane as qml
import numpy as np
from quantum_wavelets import HaarWavelet

dev = qml.device("default.qubit", wires=3)

@qml.qnode(dev)
def circuit():
    qml.BasisState(np.array([1, 0, 0]), wires=[0, 1, 2])
    HaarWavelet(wires=[0, 1, 2])
    return qml.state()

print(circuit())
```

---

### Daubechies D4 Wavelet Transform

```python
import pennylane as qml
from quantum_wavelets import DaubechiesD4

dev = qml.device("default.qubit", wires=4)

@qml.qnode(dev)
def circuit():
    DaubechiesD4(wires=[0, 1, 2, 3])
    return qml.state()

print(circuit())
```

The operator implements the full multiresolution transform  
\( D_{2^n}^4 \) using local D4 kernels and perfect-shuffle permutations.

---

## Project Structure

```text
quantum-wavelet-transforms/
│
├── quantum_wavelets/        # Core library
│   ├── haar.py              # Quantum Haar wavelet
│   ├── daubechies_d4.py     # Quantum Daubechies D4 wavelet
│   ├── permutations.py     # Π₂ⁿ, P₂ⁿ, Q₂ⁿ operators
│   ├── utils.py             # Internal helpers
│   └── __init__.py          # Public API
│
├── tests/                   # Unit tests
├── examples/                # Usage examples
├── docs/                    # Theory and documentation
└── references/              # Academic references
```

---

## Testing

Run all tests with:

```bash
python -m pytest
```

---

## Reference

```bibtex
@article{fijany1998quantum,
  title={Quantum Wavelet Transforms: Fast Algorithms and Complete Circuits},
  author={Fijany, Amir and Williams, Colin P.},
  year={1998}
}
```

---

## Roadmap

Planned and potential extensions include:

- Inverse quantum wavelet transforms  
- Higher-order Daubechies wavelets (D6, D8)  
- Wavelet packet transforms  
- Benchmarks against QFT-based approaches  
- Upstream contribution to PennyLane  

---

## License

Apache License 2.0

---

## After Saving

```bash
git add README.md
git commit -m "Update README with Daubechies D4 quantum wavelet transform"
git push
```


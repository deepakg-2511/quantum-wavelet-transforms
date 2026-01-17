# Daubechies D4 Quantum Wavelet Transform

This module implements the **Daubechies D4 quantum wavelet transform**
\( D_{2^n}^4 \) as a fully unitary quantum circuit.

## Theory

The Daubechies D4 wavelet is defined by four scaling coefficients:

\[
h_0 = \frac{1+\sqrt{3}}{4\sqrt{2}}, \quad
h_1 = \frac{3+\sqrt{3}}{4\sqrt{2}}, \quad
h_2 = \frac{3-\sqrt{3}}{4\sqrt{2}}, \quad
h_3 = \frac{1-\sqrt{3}}{4\sqrt{2}}
\]

These define a **2-qubit unitary kernel** \( U_{D4} \) acting locally.

## Quantum Construction

Following Fijany & Williams (1998):

1. Apply local D4 kernels to adjacent qubit pairs
2. Apply a perfect-shuffle permutation
3. Retain low-frequency components
4. Repeat recursively across scales

The quantum cost is dominated by permutations, not local unitaries.

## Reference

A. Fijany and C. P. Williams  
*Quantum Wavelet Transforms: Fast Algorithms and Complete Circuits*, 1998

# CRYPTOGRAPHIC COMMUNICATIONS SYSTEM AND METHOD

<!-- source: 02_math_heavy.pdf | kind: native | lang: en | pages: 1 -->

## Abstract

A cryptographic system based on the difficulty of factoring the product of two large primes. Public and private exponents are derived such that decryption inverts encryption modulo n.

## Description

Let p and q be distinct primes and let n = p·q. Define phi(n) = (p-1)(q-1). Choose e coprime to phi(n) and let d be the multiplicative inverse of e modulo phi(n): 

e · d ≡ 1 (mod φ(n)) 

Encryption of message m ∈ Z_n proceeds as c = m^e mod n, and decryption as m = c^d mod n. Correctness follows from Euler's theorem: 

m^(e·d) ≡ m^(1 + k·φ(n)) ≡ m (mod n)

## Claims

**1.** A communications method comprising: encoding a plaintext m as an integer in [0, n); computing c = m^e mod n; transmitting c; and recovering m = c^d mod n at a receiver, wherein n = p·q for distinct primes p, q and d ≡ e^(-1) mod (p-1)(q-1).

**2.** The method of claim 1, wherein |p| = |q| = 1024 bits.  *(depends on [1])*

**3.** The method of claim 1, wherein e = 65537.  *(depends on [1])*

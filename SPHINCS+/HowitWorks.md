# SPHINCS+ Components Overview

This document explains three key components of the SPHINCS+ signature scheme:
- **FORS**
- **SPX**
- **Haraka**

## 1. FORS

**FORS** stands for **Forest of Random Subsets**.

- **Purpose:**
  - Acts as a many-time (or few-time) signature scheme for signing a short message digest.
  - Compresses the message digest into a compact signature component.
  
- **How It Works:**
  - The message (or its hash) is split into several parts.
  - Each part is signed using a one-time signature mechanism on a small subset of the signature space.
  - The collection of these one-time signatures (forming a “forest”) produces an intermediate public key value.
  - This intermediate value is later embedded in a larger Merkle tree that provides overall stateless security.

- **Implementation:**
  - Functions like `fors_sign` and `fors_pk_from_sig` handle the generation of a FORS signature and the derivation of the corresponding public key from the signature.
  - Test executables (e.g., in `test/fors.c`) verify that the FORS component operates as expected.


## 2. SPX

**SPX** is the prefix used throughout the SPHINCS+ reference implementation and refers to the entire signature scheme.

- **What It Is:**
  - SPHINCS+ is constructed by combining several building blocks:
    - **FORS** for signing short message digests.
    - **WOTS+** (Winternitz One-Time Signature Plus) for chain signatures.
    - A hypertree structure (a multi-layered Merkle tree) that interlinks the above components.
    
- **Usage in the Implementation:**
  - Many constants and functions are prefixed with `SPX_` (e.g., `SPX_MLEN`, `SPX_BYTES`, `crypto_sign`).
  - The `test/spx` target builds an executable that tests the full signature generation and verification process.
  
- **Overall Role:**
  - SPX represents the complete stateless signature scheme.
  - It encompasses the entire process: key generation, signing (using the various components like FORS and WOTS+), and verification.


## 3. Haraka

**Haraka** is a lightweight cryptographic hash function family.

- **Design and Purpose:**
  - Haraka is designed for high efficiency, particularly on platforms that can exploit AES instructions.
  - It is optimized for short inputs, making it well suited for SPHINCS+ operations where small hash outputs are needed.
  
- **How It’s Used in SPHINCS+:**
  - SPHINCS+ supports multiple hash function options (e.g., SHA-2, SHAKE, and Haraka).
  - When the build parameter (e.g., `PARAMS = sphincs-haraka-128f`) specifies Haraka, the implementation links with files such as:
    - `haraka.c`
    - `hash_haraka.c`
    - `thash_haraka_robust.c`
  - This choice affects both the signing and verification processes.
  
- **Testing Haraka:**
  - The test executable (e.g., `test/haraka.c`) compares the output of the all-at-once function (`haraka_S`) with its incremental versions (`haraka_S_inc_*` functions).
  - The goal is to ensure that processing the input in chunks produces the same final hash as processing it all at once.


## Summary

- **FORS:**  
  A component that signs parts of a message digest using a forest of one-time signatures, compressing the digest into a compact value that is later integrated into a larger Merkle tree.

- **SPX:**  
  Refers to the overall SPHINCS+ signature scheme. It combines FORS, WOTS+, and a hypertree structure to provide a stateless, secure, and flexible signature mechanism.

- **Haraka:**  
  A high-speed, lightweight hash function that is used as one of the selectable hash functions within SPHINCS+. It is optimized for platforms that support fast AES-like operations and is particularly effective for short inputs.

This repository’s build system (as defined in the Makefile) allows you to compile and test these components individually (e.g., via `make test/fors.exec`, `make test/spx.exec`, and `make test/haraka`) as well as to run performance benchmarks. The Makefile conditionally includes the appropriate source files based on the chosen parameter set and hash function implementation.

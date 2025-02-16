# Explanation of Dilithium's `sign.c`

This document covers the major functions for key generation, signature creation, and verification, and explains how these functions interact to implement the signature scheme.

---

## 1. Key Pair Generation: `crypto_sign_keypair`

**Purpose:**
Generates a public/secret key pair for the Dilithium signature scheme.

**Steps:**

1. **Randomness and Seed Generation:**
   - A buffer `seedbuf` is filled with random bytes via `randombytes()`.
   - Two extra bytes are appended (set to constants `K` and `L`).
   - The `shake256` function hashes these bytes to produce a larger seed, which is then split into three parts:
     - **rho:** Used for expanding the public matrix.
     - **rhoprime:** Used as a seed for sampling short vectors.
     - **key:** Later incorporated into the secret key.

2. **Matrix Expansion:**
   - The function `polyvec_matrix_expand(mat, rho)` expands the matrix from the seed `rho`.
     This matrix is central to the lattice-based operations.

3. **Sampling Short Vectors:**
   - Two short vectors are sampled:
     - `s1` (a vector from the lattice’s first part) is generated via `polyvecl_uniform_eta`.
     - `s2`  (the error vector) is generated via `polyveck_uniform_eta`.
   - These vectors have “short” coefficients to ensure that the operations remain within the desired bounds.

4. **Matrix-Vector Multiplication and Rounding:**
   - `s1` is copied to `s1hat` and transformed into the NTT (Number Theoretic Transform) domain.
   - The product of the matrix `mat` and `s1hat` is computed using `polyvec_matrix_pointwise_montgomery` to produce `t1`.
   - After reducing and applying an inverse NTT, the error vector `s2` is added.
   - The vector `t1` is then:
     - Conditionally adjusted (`polyveck_caddq`),
     - Split into high and low bits via `polyveck_power2round`, where:
       - The high bits (stored in `t1`) are used in the public key.
       - The low bits (stored in `t0`) remain secret.

5. **Key Packing:**
   - The public key is created by packing `rho` and the high bits (`t1`) using `pack_pk`.
   - A hash `tr` is computed over the public key.
   - The secret key is packed (using `pack_sk`) with all necessary components: `rho`, `tr`, `key`, `t0`, `s1`, and `s2`.

---

## 2. Signature Generation

The signing process is split into two functions: an internal API and a wrapper.

### a. Internal API: `crypto_sign_signature_internal`

**Purpose:**
Computes a signature for a given message using the secret key.

**Key Operations:**

1. **Secret Key Unpacking:**
   - The secret key is unpacked to extract:
        - `rho`: A seed used to generate the public matrix.
        - `tr`: A hash derived from the public key, later used in computing the message hash.
        - `key`: An additional secret value that contributes to generating fresh randomness.
        - `t0`: The lower (rounded) part of an intermediate value, kept secret and used during verification.
        - `s1` and `s2`: Two short vectors with small coefficients that are central to the signature's security.

2. **Computing the Message Hash (`mu`):**
   - A hash `mu` is computed as
     `mu = CRH(tr || pre || m)`,
     where `pre` is a context prefix and `m` is the message.
   - This hash ties the message to the key.

3. **Deriving Fresh Randomness (`rhoprime`):**
   - A new seed `rhoprime` is computed via
     `rhoprime = CRH(key || rnd || mu)`,
     ensuring that each signature uses fresh randomness.

4. **NTT Transformations:**
   - The vectors `s1`, `s2`, and `t0` are transformed into the NTT domain for efficient arithmetic.

5. **Rejection Sampling Loop (Label `rej:`):**
   - An intermediate vector `y` is sampled from a prescribed distribution (`polyvecl_uniform_gamma1`) with a nonce that increments with each iteration.
   - **Matrix-Vector Multiplication:**
     - The sampled `y` is transformed (via NTT) and multiplied with the matrix `mat` to obtain `w1`.
     - After reduction and inverse NTT, `w1` is decomposed into:
       - A high part (kept secret) and
       - A low part `w0`.
   - **Challenge Computation:**
     - The high part of `w1` is packed and hashed (using SHAKE256) to produce a challenge polynomial `cp` via `poly_challenge`.
   - **Computing the Response (`z`):**
     - The response is computed as:
       `z = y + c * s1`
       (with `c` coming from the challenge).
     - The norm of `z` is checked; if it exceeds a threshold (`GAMMA1 - BETA`), the process restarts.
   - **Additional Checks and Hint Generation:**
     - The algorithm subtracts `c * s2` from `w0` and checks the norm.
     - Hints are generated from the low bits (and additional rounding of `t0`) and verified to ensure they do not exceed a threshold (`OMEGA`).
     - If any check fails, the sampling and computation are repeated.

6. **Signature Packing:**
   - Once all conditions are met, the signature is packed using `pack_sig`.
     The packed signature contains the response vector `z` and the hint vector `h`.
   - The signature length is set to `CRYPTO_BYTES`.

### b. External Signature API: `crypto_sign_signature`

- **Purpose:**
  This function wraps the internal signature function. It:
  - Prepares a prefix (`pre`) by encoding a context string.
  - Selects randomness: If `DILITHIUM_RANDOMIZED_SIGNING` is defined, it uses fresh random bytes; otherwise, it uses zeros.
  - Calls `crypto_sign_signature_internal` with the prepared inputs.

### c. Signed Message Construction: `crypto_sign`

- **Purpose:**
  Constructs a signed message by concatenating the signature and the original message.
- **Operation:**
  - The function reserves the first `CRYPTO_BYTES` bytes of the output for the signature.
  - It then appends the message.
  - The final length is updated to include both the signature and the message.

---

## 3. Signature Verification

Verification is also divided into internal and external functions.

### a. Internal Verification: `crypto_sign_verify_internal`

**Purpose:**
Verifies a signature by reconstructing and comparing the challenge.

**Steps:**

1. **Unpacking:**
   - The public key is unpacked to extract `rho` and the rounded vector `t1`.
   - The signature is unpacked to extract the challenge `c`, the response vector `z`, and the hint vector `h`.
   - The norm of `z` is checked to ensure it is within acceptable bounds.

2. **Recomputing the Message Hash (`mu`):**
   - A hash `mu` is computed as
     `mu = CRH(H(rho, t1) || pre || m)`,
     linking the public key with the message.

3. **Matrix-Vector Multiplication and Reconstruction:**
   - The matrix `mat` is re-expanded from `rho`.
   - The response vector `z` (transformed by NTT) is multiplied with `mat`.
   - The product of the challenge (transformed appropriately) with `t1` is subtracted from the above result.
   - The hint vector `h` is used to reconstruct the high part of the product (`w1`).

4. **Challenge Verification:**
   - A new challenge `c2` is computed by hashing `mu` and the packed form of the reconstructed `w1`.
   - The function compares `c2` with the challenge `c` from the signature. If they match, the signature is valid.

### b. External Verification: `crypto_sign_verify` and `crypto_sign_open`

- **`crypto_sign_verify`:**
  - Prepares the context prefix and calls the internal verification routine.
  - Returns 0 on success, or -1 if verification fails.

- **`crypto_sign_open`:**
  - Used for “signed messages” where the signature is concatenated with the message.
  - It separates the signature from the message, performs verification, and if successful, extracts the original message.
  - On failure, it zeros out the output message buffer and returns -1.

---

## 4. Summary

- **Key Generation:**
  - Uses random seeds and SHAKE256 to derive public parameters.
  - Expands a public matrix and samples short secret vectors.
  - Packs both the public key (with the high bits of a computed vector) and the secret key (containing additional secret information).

- **Signature Generation:**
  - Computes a hash (`mu`) that ties the message to the public key.
  - Derives fresh randomness (`rhoprime`) for each signature.
  - Uses the NTT for efficient polynomial arithmetic.
  - Employs rejection sampling to ensure the response vector (`z`) and hint vector (`h`) do not leak secret information.
  - Packs the final signature into a fixed-size byte array.

- **Signature Verification:**
  - Reconstructs intermediate values from the public key and signature.
  - Recomputes the challenge and checks it against the signature.
  - Provides both internal and external APIs for flexibility.

This implementation uses advanced techniques—including the Number Theoretic Transform (NTT), rejection sampling, and SHAKE256 hashing—to build a secure post-quantum digital signature scheme according to the Dilithium specification.

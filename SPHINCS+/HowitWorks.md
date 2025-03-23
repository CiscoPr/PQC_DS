# SPHINCS+

## Structure
The signature scheme combines these main components:
- **WOTS+ (Winternitz One-Time Signature Plus)**: each key pair signs exactly one message. The security relies on hash chains, wherein the public key consists of hash outputs from secret seeds. Signing involves revealing certain intermediate values of these chains, and verification reconstructs the hash chains to validate authenticity.
- **FORS (Forest of Random Subsets)**: splits the message into multiple indices, to select specific leaf nodes from several FORS trees. Each FORS tree provides one secret leaf and all selected leaves form the signature.
- **XMSS (eXtended Merkle Signature Scheme)**: uses binary Merkle trees to manage multiple WOTS+ public keys efficiently. Each leaf node is a WOTS+ public key. Authentication occurs through Merkle paths, leading from leaf nodes up to the root node. The root node serves as the public key for verification.
- **Hypertree (Multiple XMSS layers)**: structures multiple XMSS layers hierarchically. Each XMSS tree signs the root of the tree below.
- **Haraka (Cryptographic hash function for short-input hashing)**: specialized cryptographic hash function optimized for small input sizes (≤256 bits). Enhances the scheme's performance for message digest computations, node hashing in Merkle trees and hashing operations for WOTS+ and FORS

```
Hypertree structure:
Root (top-layer XMSS tree)
   ├── XMSS subtree 1 root
   │    ├── WOTS+ keys
   │    └── WOTS+ keys
   └── XMSS subtree 2 root
        ├── WOTS+ keys
        └── WOTS+ keys

The overall scheme with FORS:
Message → FORS Trees → FORS Public Key → WOTS+ → XMSS Trees → Hypertree → Public Key Root
```


## Operations
### Key Generation
  - Private Key:
    - `SK.seed`: used to generate private keys for WOTS+, FORS, and Merkle tree nodes.
    - `SK.prf`: pseudorandom function used to generate deterministic randomness for signing.

  - Public Key:
    - `PK.seed`: public seed to initialize hash functions and ensure domain separation.
    - `PK.root`: Merkle tree root for public key verification.

### Signing process:
  1. **Generate signature randomness (R)**: `R ← PRF_msg(SK.prf, OptRand, M)` -> PRF_msg is a pseudorandom function that uses the private seed SK.prf, optional randomness (OptRand), and the message (M) to generate a unique randomness (R) for each signature.
  2. **Derive the message digest and indices**: `(md || idx_tree || idx_leaf) ← H_msg(R, PK.seed, PK.root, M)` -> H_msg is a hash function combining the signature randomness (R), public seed (PK.seed), public root (PK.root), and the message (M). It outputs a message digest (md) used for FORS signing, and indices (idx_tree, idx_leaf) that identify the specific XMSS tree and leaf position within the hypertree structure.
  3. **Generate FORS signature based on the message digest**: `SIG_FORS ← fors_sign(md, SK.seed, PK.seed, ADRS)` -> FORS signing process uses the message digest (md) to select secret keys from multiple trees of the forest. Each selected key is combined into a signature (SIG_FORS), leveraging private seeds (SK.seed) and public seeds (PK.seed) along with address structures (ADRS) for domain separation.
  4. **Derive FORS public key**: `PK_FORS ← fors_pkFromSig(SIG_FORS, md, PK.seed, ADRS)` -> reconstructs the FORS public key (PK_FORS) from the previously generated FORS signature (SIG_FORS) and message digest (md). Correct reconstruction verifies that the signature authentically corresponds to the given digest.
  5. **Sign the FORS public key with XMSS hypertree**: `SIG_HT ← ht_sign(PK_FORS, SK.seed, PK.seed, idx_tree, idx_leaf)` -> PK_FORS is signed using the hypertree structure (ht_sign). The hypertree, composed of multiple XMSS layers, utilizes the XMSS scheme to authenticate this public key using secret seeds (SK.seed), public seeds (PK.seed), and derived indices (idx_tree, idx_leaf).
  6. **Concatenate the final signature**: `SIG = R || SIG_FORS || SIG_HT` -> The complete SPHINCS+ signature (SIG) comprises the initial randomness (R), the FORS signature (SIG_FORS), and the XMSS hypertree signature (SIG_HT). The verifier uses this combined signature to validate authenticity comprehensively.

### Signing Verification:
  1. **Recompute Message Digest and Indices**: `(md || idx_tree || idx_leaf) ← H_msg(R, PK.seed, PK.root, M)`:extracts the randomness (R) from the received signature (SIG), computing the message digest and indices using the hash function. Here, md is the message digest, idx_tree identifies the specific XMSS tree within the hypertree, and idx_leaf identifies the leaf node within the XMSS tree.
  2. **Recover FORS Public Key from the FORS Signature**: `PK_FORS ← fors_pkFromSig(SIG_FORS, md, PK.seed, ADRS)`: Using the recomputed message digest (md) and the provided FORS signature (SIG_FORS), reconstruct the corresponding FORS public key (PK_FORS). Correct reconstruction indicates that the signer had access to the secret keys corresponding to the FORS trees.
  3. **Validate the Hypertree Signature**: `XMSS_root ← hr_verify(SIG_HT, PK_FORS, PK.seed, idx_tree, idx_leaf)`: Verify the Hypertree signature (SIG_HT) using the reconstructed FORS public key (PK_FORS). Confirm that the final XMSS root matches the public key root (PK.root). Matching roots validate the authenticity of the signature, proving it was generated by the legitimate holder of the secret key.


```
SPHINCS+ Overall Scheme Diagram

 Message (M)
      │
      │
      └───┐
          ▼
┌───────────────────────┐
│ Generate randomness R │───┐
└───────────────────────┘   │
      │                     │
      ▼                     │
┌─────────────────────────────────────────────┐
│ Compute Digest and Indices                  │
│ md || idx_tree || idx_leaf = H_msg(...)     │
└─────────────────────────────────────────────┘
      │
      │ md
      ▼
┌───────────────────────────────────────┐
│ FORS (Forest of Random Subsets)       │
│                                       │
│ md → SIG_FORS → PK_FORS (FORS root)   │
│ ┌─ Tree 1 ──┐ ┌─ Tree 2 ──┐ ...       │
│ │  leaves   │ │  leaves   │           │
│ └───────────┘ └───────────┘           │
└───────────────────────────────────────┘
      │
      │ PK_FORS
      ▼
┌─────────────────────────────────────────────────┐
│ Hypertree (XMSS Layers)                         │
│ ┌───────────────────────────────────┐           │
│ │ Top-layer XMSS tree               │── PK.root │
│ └───────────┬───────────────────────┘           │
│             │                                   │
│             ▼                                   │
│ ┌──────────────────┐                            │
│ │ Intermediate XMSS│                            │
│ └─────────┬────────┘                            │
│           │                                     │
│           ▼                                     │
│ ┌───────────────────────┐                       │
│ │ WOTS+ Signs PK_FORS   │                       │
│ └───────────────────────┘                       │
└─────────────────────────────────────────────────┘
      │
      ▼
Final Signature:
SIG = [ R || SIG_FORS || SIG_HT ]

```

## Test folder:
- `benchmark.c`: Evaluates SPHINCS+ performance metrics.
- `fors.c`: Validates FORS signature and public-key derivation.
- `haraka.c`: Ensures correctness and measures incremental hashing operations.
- `spx.c`: Performs comprehensive tests for keypair generation, signing, and verification cycles.


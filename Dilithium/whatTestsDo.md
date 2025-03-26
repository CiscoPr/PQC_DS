## test_dilithium.c

- **Keypair gen**: generates a public and private key
- **Sig Creation and Verif**: signs a random message and verifies the signature is valid
- **Message Integrity check**: confirms that the recovered message matches the original
- **Forgery detection**: alterns one byte in the signature and verifies that the tampered signature is correctly rejected
- **Length Checks**: verifies that the signed message and original message lengths are as expected

## test_vectors.c

- **Iterative tetsing**: runs a large no. of iterations to exercise various internal operations
- **Diagnostic output**: prints intermediate values (e.g: message, public key hash, signature hash) to help debug and verify correct behavior
- **(Un)Packing Functions**: tests the correctness of functions for packing and unpacking polynomials (e.g: polyeta, polyz, polyt1, polyt0)
- **Norm and Consistency Checks**: verifies that polynomial norms and decompositions meet expected criteria
- **Matrix Expansion and NTT operations**: Validates that matrix expansion and the associated number-thoeretic transforms work correctly

## test_mul.c

- **Naive mult**: implements a straightforward, reference polynomial multiplication
- **NTT Consistency Test**: Uses the NTT and its inverse to ensure that transformations preserve the original polynomial when scaled and reversed
- **Optimized Multiplication verification**: compares the result of the optimized, Montogomery, based polynomial multiplication agains a naive multiplication result
- **Repetitive validation**: runs many iterations to verify the correctness of the arithmetic operations
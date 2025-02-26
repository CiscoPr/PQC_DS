# NIST Post-Quantum Cryptography Standardization Criteria

## Security
Security is the most critical evaluation criterion. The following aspects are considered:

- **Public-Key Cryptography Applications**: Compatibility with existing standards like TLS, SSH, and DNSSEC.
- **Security Definitions**: Ensuring encryption schemes meet IND-CCA2 security.
- **Resistance to Attacks**: Protection against classical and quantum attacks.
- **Malleability and Non-Repudiation**: Preventing unauthorized modifications and ensuring signature integrity.
- **Security Proofs**: Strong theoretical foundations with formal security proofs.

## Cost
Cost refers to the efficiency of an algorithm in terms of computational resources:

- **Size Efficiency**: Minimized sizes for public keys, ciphertexts, and signatures.
- **Computational Performance**: Efficient execution for encryption, decryption, and key generation.
- **Memory Usage**: Optimized RAM requirements for deployment in constrained environments.
- **Flexibility**: Ability to adapt to various security and performance trade-offs.

## Algorithm and Implementation Characteristics
These characteristics influence real-world usability and adoption:

- **Flexibility**: Supporting additional functionalities and seamless integration with existing protocols.
- **Simplicity**: Straightforward design to ease secure implementations.
- **Adoption Readiness**: Free and fair licensing to promote widespread use.

These criteria ensure that selected algorithms are secure, efficient, and practical for global adoption in post-quantum cryptographic standards.

For more info, go [here](https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization/evaluation-criteria).

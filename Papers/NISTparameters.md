# NIST Post-Quantum Cryptography Standardization Criteria

## Security
Security is the most critical evaluation criterion. The following aspects are considered:

- **Public-Key Cryptography Applications**: Compatibility with existing standards like TLS, SSH, and DNSSEC.
- **Security Definitions**: Ensuring encryption schemes meet IND-CCA2 security (indistiguishability under adaptive Chosen Ciphertext Attack ).
- **Resistance to Attacks**: Protection against classical and quantum attacks.
- **Malleability and Non-Repudiation**: Preventing unauthorized modifications and ensuring signature integrity.
- **Security Proofs**: Strong theoretical foundations with formal security proofs.

## Cost
Cost refers to the efficiency of an algorithm in terms of computational resources:

- **Size Efficiency**: Minimized sizes for public keys, ciphertexts, and signatures. ("The importance of public-key size may vary depending on the application; if applications can cache public keys, or otherwise avoid transmitting them frequently, the size of the public key may be of lesser importance. In contrast, applications that seek to obtain perfect forward secrecy by transmitting a new public key at the beginning of every session are likely to benefit greatly from algorithms that use relatively small public keys.")
- **Computational Performance**: Efficient execution for encryption, decryption, and key generation.
- **Memory Usage**: Optimized RAM requirements for deployment in constrained environments.
- **Flexibility**: Ability to adapt to various security and performance trade-offs.

## Algorithm and Implementation Characteristics
These characteristics influence real-world usability and adoption:

- **Flexibility**: Supporting additional functionalities and seamless integration with existing protocols. ("Some examples of “flexibility” may include (but are not limited to) the following:
The scheme can be modified to provide additional functionalities that extend beyond the minimum requirements of public-key encryption, KEM, or digital signature (e.g., asynchronous or implicitly authenticated key exchange, etc.).
It is straightforward to customize the scheme’s parameters to meet a range of security targets and performance goals.
The algorithms can be implemented securely and efficiently on a wide variety of platforms, including constrained environments, such as smart cards.
Implementations of the algorithms can be parallelized to achieve higher performance.
The scheme can be incorporated into existing protocols and applications, requiring as few changes as possible.")
- **Simplicity**: Straightforward design to ease secure implementations.
- **Adoption Readiness**: Free and fair licensing to promote widespread use.

These criteria ensure that selected algorithms are secure, efficient, and practical for global adoption in post-quantum cryptographic standards.

For more info, go [here](https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization/evaluation-criteria).

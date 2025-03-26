# Dockerized Crystals-Dilithium Build and Test

This project provides a Docker container that automatically clones, builds, and tests the [Crystals-Dilithium](https://github.com/pq-crystals/dilithium) repository (a post-quantum digital signature implementation) without requiring you to clone the repo locally.

## Features

- **Automated Cloning:** The Dockerfile clones the official Crystals-Dilithium repository during the image build.
- **Dependency Installation:** Installs necessary build tools and OpenSSL development libraries.
- **Build Process:** Compiles the reference implementation (located in the `ref/` directory) using the provided Makefile.
- **Test Execution:** Runs a test executable (default: `test/test_dilithium2`) to verify the build.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system.

## Usage

### 1. Build the Docker Image

Open a terminal in the directory containing the `Dockerfile` and run:

```bash
docker build -t dilithium .
```

This command:

- Pulls the Ubuntu 22.04 base image.
- Installs required packages (git, build-essential, make, and libssl-dev).
- Clones the Crystals-Dilithium repository from GitHub.
- Navigates to the ref/ directory and compiles the project using make.

### 2. Run the Docker container

After the image is built, run the container:

```bash
docker run --rm dilithium
```

By default, this command executes the **./test/test_dilithium2** test program. When the test completes, the container exits and is removed.

### 3. Customization

- **Running a Different Test**: To run a different executable (for example, test/test_vectors2), override the default command:

```bash
docker run --rm dilithium ./test/test_vectors2
```

- **Using a Different Implementation**: If you want to build and test the AVX2 implementation instead of the reference (ref/), modify the Dockerfile by changing the working directory (e.g., to /dilithium/avx2) and adjust the commands accordingly.

- **Custom Compiler Flags**: If you need to set custom compiler flags (e.g., for nonstandard OpenSSL installation paths), modify the Dockerfile to export the required environment variables (CFLAGS, NISTFLAGS, LDFLAGS) before running make.


# Error Override Files for Test_dilithium

The Dilithium test harness (`test_dilithium.c`) runs several checks on key generation, signing, and verification. To ensure that our error‐detection mechanisms are working correctly, we have created several override files that deliberately force specific error conditions. **Only one override file should be compiled at a time** (to avoid multiple definition conflicts). Below is a description of each error file and how to compile it with the test program.

## Error Files and Their Purposes

### 1. `messages_dont_match.c`
- **Purpose:**
  Overrides `crypto_sign_open` so that after recovering the message from the signed message, it deliberately flips one bit (using XOR) in the first byte of the recovered message.
- **Error Triggered:**
  When test_dilithium compares the recovered message with the original message, they will differ and the test prints: `Messages don't match`


### 2. `open_message_length_wrong.c`
- **Purpose:**
Overrides `crypto_sign_open` to compute the correct message length (i.e. `smlen - CRYPTO_BYTES`) for verification but then deliberately returns a message length that is one byte too short.
- **Error Triggered:**
The test checks if the recovered message length equals `MLEN` (e.g., 59) and, if not, prints: `Message lengths wrong`


### 3. `signed_message_length_wrong.c`
- **Purpose:**
Overrides `crypto_sign` to produce a valid signature and copy the message into the output buffer, then deliberately increases the signed message length (`smlen`) by one extra byte.
- **Error Triggered:**
The test verifies that the signed message length equals `MLEN + CRYPTO_BYTES` and, if it doesn't, prints: `Signed message lengths wrong`


### 4. `trivial_forgery_possible.c`
- **Purpose:**
Overrides `crypto_sign_verify_internal` so that it always returns success (0), even if the signature has been tampered with. It simulates a scenario where the verification function would accept forged signatures.
- **Error Triggered:**
After intentionally corrupting a signature in the test (by modifying a random byte), the test expects verification to fail. If it instead returns success, the test prints: `Trivial forgeries possible`


### 5. `verification_failure.c`
- **Purpose:**
Overrides `crypto_sign_verify_internal` by computing the challenge from the message, context, and public key, then deliberately corrupts the computed challenge (by flipping its first byte). As a result, even a valid signature will not match the expected challenge.
- **Error Triggered:**
When the test calls `crypto_sign_open` on a valid signature, it will now fail verification and the test prints: `Verification failed`


## Compiling with test_dilithium.c

Each override file is compiled together with `test_dilithium.c` (and any required support files such as `randombytes.c`) to create a separate executable that forces the corresponding error condition.
- Ensure that only one override file is included in each build command to avoid multiple definitions.
- The include paths (-I. -I./ref -I./avx2) and library linking (-L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref) must match the build environment.

## Running the test
After building the container, create an interactive shell within it by running
```bash
docker run -it --entrypoint /bin/bash dilithium
```
Right after that, before running the tests, make sure to set the library path so that the dynamic linker can find the shared libraries. For example, run export LD_LIBRARY_PATH=. to include the current directory in the search path.
Then just run each test individually.
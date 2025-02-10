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

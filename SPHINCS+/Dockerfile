# Use a base image with a recent Ubuntu release
FROM ubuntu:20.04

# Install essential build tools and git
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      build-essential \
      git \
      ca-certificates \
      make \
      libssl-dev \
      && rm -rf /var/lib/apt/lists/*

# Set working directory and clone the SPHINCS+ repository
WORKDIR /sphincsplus
RUN git clone https://github.com/sphincs/sphincsplus.git

# Change to the repository directory (preserving layout)
WORKDIR /sphincsplus/sphincsplus/ref


# Build the project normally (this builds the tests as well).
RUN make

# --- Build a shared library for SPHINCS+ ---
# Include the Haraka-related sources because PARAMS is sphincs-haraka-128f.
RUN gcc -shared -fPIC -O3 -std=c99 -DPARAMS=sphincs-haraka-128f -I. \
    -o libsphincs.so address.c randombytes.c merkle.c wots.c wotsx1.c utils.c utilsx1.c fors.c sign.c haraka.c hash_haraka.c thash_haraka_robust.c -lcrypto

# --- Copy in our custom override (failure) source files ---
# (These files must be present in your build context.)
COPY fors_fail.c ./fail_tests/fors_fail.c
COPY spx_fail_keypair.c ./fail_tests/spx_fail_keypair.c
COPY spx_fail_verification.c ./fail_tests/spx_fail_verification.c
COPY spx_fail_inplace.c ./fail_tests/spx_fail_inplace.c
COPY spx_fail_flip.c ./fail_tests/spx_fail_flip.c

# --- Compile custom test executables for each failing case ---

# 1. Compile a failing FORS test executable.
#    Links test/fors.c with fors_fail.c.
RUN gcc -O2 -DPARAMS=sphincs-haraka-128f -o test_fail_fors test/fors.c fail_tests/fors_fail.c -I. -L. -lsphincs -lcrypto -ldl

# 2. Compile a failing keypair test executable.
#    Links test/spx.c with spx_fail_keypair.c.
RUN gcc -O2 -DPARAMS=sphincs-haraka-128f -o test_fail_keypair test/spx.c fail_tests/spx_fail_keypair.c -I. -L. -lsphincs -lcrypto -ldl

# 3. Compile a failing signature verification test executable.
#    Links test/spx.c with spx_fail_verification.c.
RUN gcc -O2 -DPARAMS=sphincs-haraka-128f -o test_fail_verification test/spx.c fail_tests/spx_fail_verification.c -I. -L. -lsphincs -lcrypto -ldl

# 4. Compile a failing in-place verification test executable.
#    Links test/spx.c with spx_fail_inplace.c.
RUN gcc -O2 -DPARAMS=sphincs-haraka-128f -o test_fail_inplace test/spx.c fail_tests/spx_fail_inplace.c -I. -L. -lsphincs -lcrypto -ldl

# 5. Compile a failing flip test executable.
#    Links test/spx.c with spx_fail_flip.c.
RUN gcc -O2 -DPARAMS=sphincs-haraka-128f -o test_fail_flip test/spx.c fail_tests/spx_fail_flip.c -I. -L. -lsphincs -lcrypto -ldl

# Ensure the shared library is found at runtime.
ENV LD_LIBRARY_PATH=/sphincsplus/sphincsplus/ref

# By default, run all custom test executables sequentially.
# "set +e" ensures the shell does not exit if one test fails.
CMD /bin/sh -c "set +e; \
echo '======================================='; \
echo 'Running failing FORS test:'; \
echo '======================================='; \
./test_fail_fors; \
echo; echo '======================================='; \
echo 'Running failing keypair test:'; \
echo '======================================='; \
./test_fail_keypair; \
echo; echo '======================================='; \
echo 'Running failing verification test:'; \
echo '======================================='; \
./test_fail_verification; \
echo; echo '======================================='; \
echo 'Running failing in-place test:'; \
echo '======================================='; \
./test_fail_inplace; \
echo; echo '======================================='; \
echo 'Running failing flip test:'; \
echo '======================================='; \
./test_fail_flip; \
"
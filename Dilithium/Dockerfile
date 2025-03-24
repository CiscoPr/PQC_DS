# Use a base image with a recent Ubuntu release
FROM ubuntu:20.04

# Install required packages: git, build-essential, make, libssl-dev, and ca-certificates
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      git \
      build-essential \
      make \
      libssl-dev \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set working directory and clone the Dilithium repository
WORKDIR /dilithium
RUN git clone https://github.com/pq-crystals/dilithium.git .

# Change to the reference implementation directory and build the shared library
WORKDIR /dilithium/ref
RUN make shared

# Copy in custom test source files (ensure these files are in the build context)
COPY messages_dont_match.c open_message_length_wrong.c signed_message_length_wrong.c trivial_forgery_possible.c verification_failure.c ./

# Compile custom test executables linking against the shared library
RUN gcc -O2 -DDILITHIUM_MODE=2 -o test_messages test/test_dilithium.c messages_dont_match.c randombytes.c \
    -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref
RUN gcc -O2 -DDILITHIUM_MODE=2 -o test_mess_len_open test/test_dilithium.c open_message_length_wrong.c randombytes.c \
    -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref
RUN gcc -O2 -DDILITHIUM_MODE=2 -o test_mess_len test/test_dilithium.c signed_message_length_wrong.c randombytes.c \
    -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref
RUN gcc -O2 -DDILITHIUM_MODE=2 -o test_forge test/test_dilithium.c trivial_forgery_possible.c randombytes.c \
    -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref
RUN gcc -O2 -DDILITHIUM_MODE=2 -o test_ver test/test_dilithium.c verification_failure.c randombytes.c \
    -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref

# Set runtime library path so the shared library is found
ENV LD_LIBRARY_PATH=/dilithium/ref

# By default, run each test sequentially with clear output headers.
CMD ["/bin/sh", "-c", "set +e; \
echo '======================================='; \
echo 'Running test_messages:'; \
echo '======================================='; \
./test_messages; \
echo; \
echo '======================================='; \
echo 'Running test_mess_len_open:'; \
echo '======================================='; \
./test_mess_len_open; \
echo; \
echo '======================================='; \
echo 'Running test_mess_len:'; \
echo '======================================='; \
./test_mess_len; \
echo; \
echo '======================================='; \
echo 'Running test_forge:'; \
echo '======================================='; \
./test_forge; \
echo; \
echo '======================================='; \
echo 'Running test_ver:'; \
echo '======================================='; \
./test_ver"]

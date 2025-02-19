# Use an official Ubuntu image as the base.
FROM ubuntu:22.04

# Install required packages: git, build-essential (for gcc, make, etc.), and libssl-dev for OpenSSL.
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    make \
    libssl-dev \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container.
WORKDIR /dilithium

# Clone the Dilithium repository directly into the container.
RUN git clone https://github.com/pq-crystals/dilithium.git .

# Change to the reference implementation directory.
WORKDIR /dilithium/ref

# Build the shared libraries first.
RUN make shared

# Copy the local files force_corruption.c and force_error.c into the container.
COPY force_corruption.c force_error.c ./

# Now compile your custom test programs, linking against the shared library.
RUN gcc -O2 -DDILITHIUM_MODE=2 -o force_error force_error.c randombytes.c -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref
RUN gcc -O2 -DDILITHIUM_MODE=2 -o force_corruption force_corruption.c randombytes.c -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref

RUN export LD_LIBRARY_PATH=. && ./force_error
RUN export LD_LIBRARY_PATH=. && ./force_corruption


# Build the remaining tests.
# RUN make

# By default, run one of the test programs (for parameter set 2).
# CMD ["./test/test_dilithium2"]

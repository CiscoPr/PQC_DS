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

# Change to the reference implementation directory and build it.
WORKDIR /dilithium/avx2
RUN make

# By default, run one of the test programs (for parameter set 2).
CMD ["./test/test_dilithium2"]

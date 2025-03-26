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
      python3 \
      python3-pip \
    && python3 -m pip install pandas matplotlib \
    && rm -rf /var/lib/apt/lists/*

# Set working directory and clone the Dilithium repository
WORKDIR /dilithium
RUN git clone https://github.com/pq-crystals/dilithium.git .

# Change to the reference implementation directory and build the shared library
WORKDIR /dilithium/ref
RUN make shared

# Copy in custom test source files (ensure these files are in the build context)
COPY messages_dont_match.c open_message_length_wrong.c signed_message_length_wrong.c trivial_forgery_possible.c verification_failure.c test_timing.c generate_graph.py ./

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

RUN gcc -O2 -DDILITHIUM_MODE=2 -o test_timing_2 \
    test_timing.c \
    sign.c randombytes.c fips202.c poly.c polyvec.c packing.c rounding.c symmetric-shake.c ntt.c \
    -I. \
    -L. \
    -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref

RUN gcc -O2 -DDILITHIUM_MODE=3 -o test_timing_3 \
    test_timing.c \
    sign.c randombytes.c fips202.c poly.c polyvec.c packing.c rounding.c symmetric-shake.c ntt.c \
    -I. \
    -L. \
    -lpqcrystals_dilithium3_ref -lpqcrystals_fips202_ref

RUN gcc -O2 -DDILITHIUM_MODE=5 -o test_timing_5 \
    test_timing.c \
    sign.c randombytes.c fips202.c poly.c polyvec.c packing.c rounding.c symmetric-shake.c ntt.c \
    -I. \
    -L. \
    -lpqcrystals_dilithium5_ref -lpqcrystals_fips202_ref


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
./test_forge"]


# Final CMD: run each test 10 times for each mode and update CSV/graph.
CMD ["/bin/sh", "-c", "\
mkdir -p /results && \
for mode in 2 3 5; do \
  for i in $(seq 1 10); do \
    if [ \"$mode\" -eq 2 ]; then \
      output=$(./test_timing_2); \
    elif [ \"$mode\" -eq 3 ]; then \
      output=$(./test_timing_3); \
    elif [ \"$mode\" -eq 5 ]; then \
      output=$(./test_timing_5); \
    fi; \
    echo \"Mode $mode, iteration $i output:\"; \
    echo \"$output\"; \
    keygen=$(echo \"$output\" | grep 'Average key generation time:' | awk '{print $5}'); \
    sign=$(echo \"$output\" | grep 'Average signing time:' | awk '{print $4}'); \
    verify=$(echo \"$output\" | grep 'Average verification time:' | awk '{print $4}'); \
    if [ -z \"$keygen\" ]; then keygen=\"0.00\"; fi; \
    if [ -z \"$sign\" ]; then sign=\"0.00\"; fi; \
    if [ -z \"$verify\" ]; then verify=\"0.00\"; fi; \
    echo \"Appending: Mode $mode, keygen=$keygen, sign=$sign, verify=$verify\"; \
    python3 generate_graph.py \"$mode\" \"$keygen\" \"$sign\" \"$verify\"; \
  done; \
done; \
echo 'Timing tests complete. Check /results for CSV and graphs.'"]
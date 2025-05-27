# Base image
FROM ubuntu:20.04

# Install required packages
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

# Clone Dilithium repository
WORKDIR /dilithium
RUN git clone https://github.com/pq-crystals/dilithium.git .

# Build Dilithium shared libraries
WORKDIR /dilithium/ref

RUN make shared

# Copy custom C source files
COPY instrumental_sign.c test_timing.c generate_graph.py ./

# Compile tests
RUN gcc -O2 -DDILITHIUM_MODE=2 -o test_timing_2 test_timing.c instrumental_sign.c randombytes.c \
    -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref

RUN gcc -O2 -DDILITHIUM_MODE=3 -o test_timing_3 test_timing.c instrumental_sign.c randombytes.c \
    -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium3_ref -lpqcrystals_fips202_ref

RUN gcc -O2 -DDILITHIUM_MODE=5 -o test_timing_5 test_timing.c instrumental_sign.c randombytes.c  \
    -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium5_ref -lpqcrystals_fips202_ref


#gcc -O2 -DDILITHIUM_MODE=2 -o test_messages test/test_dilithium.c messages_dont_match.c randombytes.c \
#    -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref && \
#    gcc -O2 -DDILITHIUM_MODE=2 -o test_mess_len_open test/test_dilithium.c open_message_length_wrong.c randombytes.c \
#    -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref && \
#    gcc -O2 -DDILITHIUM_MODE=2 -o test_mess_len test/test_dilithium.c signed_message_length_wrong.c randombytes.c \
#    -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref && \
#    gcc -O2 -DDILITHIUM_MODE=2 -o test_forge test/test_dilithium.c trivial_forgery_possible.c randombytes.c \
#    -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref && \
#    gcc -O2 -DDILITHIUM_MODE=2 -o test_ver test/test_dilithium.c verification_failure.c randombytes.c \
#    -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref && \


# Set runtime library path
ENV LD_LIBRARY_PATH=/dilithium/ref

# Default command (Run extensive timing tests for each mode)
CMD ["/bin/sh", "-c", "\
mkdir -p /results && \
for mode in 2 3 5; do \
  for i in $(seq 1 100); do \
    output=$(./test_timing_${mode}); \
    echo \"Mode $mode, iteration $i output:\"; \
    echo \"$output\"; \
    keygen=$(echo \"$output\" | grep 'Average key generation time:' | awk '{print $5}'); \
    sign=$(echo \"$output\" | grep 'Average signing time:' | awk '{print $4}'); \
    verify=$(echo \"$output\" | grep 'Average verification time:' | awk '{print $4}'); \
    slow_rej=$(echo \"$output\" | grep 'Number of rejections:' | awk '{print $4}'); \
    fast_rej=$(echo \"$output\" | grep 'Number of rejections:' | awk '{print $7}'); \
    [ -z \"$keygen\" ] && keygen=\"0.00\"; \
    [ -z \"$sign\" ] && sign=\"0.00\"; \
    [ -z \"$verify\" ] && verify=\"0.00\"; \
    [ -z \"$slow_rej\" ] && slow_rej=\"0\"; \
    [ -z \"$fast_rej\" ] && fast_rej=\"0\"; \
    python3 generate_graph.py \"$mode\" \"$keygen\" \"$sign\" \"$verify\" \"$slow_rej\" \"$fast_rej\"; \
  done; \
  cp /results/rejection_timings.csv /results/rejection_log_mode${mode}.csv; \
done; \
echo 'Timing tests complete. Check /results for CSV and graphs.'"]


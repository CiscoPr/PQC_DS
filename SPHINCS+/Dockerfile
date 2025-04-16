# Use a base image with a recent Ubuntu release
FROM ubuntu:20.04

# Install essential build tools, git, Python, and required packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      build-essential \
      git \
      ca-certificates \
      make \
      libssl-dev \
      python3 \
      python3-pip && \
    python3 -m pip install pandas matplotlib && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory and clone the SPHINCS+ repository
WORKDIR /sphincsplus
RUN git clone https://github.com/sphincs/sphincsplus.git

# Change to the repository's reference implementation directory
WORKDIR /sphincsplus/sphincsplus/ref

# Build the project normally (this builds tests as well)
RUN make

# (Optional) Build a shared library if required by your tests.
# Example: Build one using the "sphincs-haraka-128f" parameter set (you can remove or adapt this block as needed)
RUN gcc -shared -fPIC -O3 -std=c99 -DPARAMS=sphincs-haraka-128f -I. \
    -o libsphincs.so address.c randombytes.c merkle.c wots.c wotsx1.c utils.c utilsx1.c fors.c sign.c haraka.c hash_haraka.c thash_haraka_robust.c -lcrypto

# Copy benchmark-related source files and the graph generator script into the container
COPY test_timing.c .
COPY generate_graph.py .

# Create a directory for storing results
RUN mkdir -p /results

# Default command: compile and run the timing benchmark for each SHA-256 parameter set.
# The parameter set names here are based on the official repo names (e.g., "sha2-128s")
# For SHA-256 instantiations, the additional source files are: sha2.c, hash_sha2.c, thash_sha2_robust.c.
CMD ["/bin/sh", "-c", "\
echo 'Starting SPHINCS+ benchmark loop...'; \
mkdir -p /results; \
for param in sha2-128s sha2-128f sha2-192s sha2-192f sha2-256s sha2-256f; do \
  echo \"Testing parameter set $param...\"; \
  HASH_SRC='sha2.c hash_sha2.c thash_sha2_robust.c'; \
  gcc -O2 -DPARAMS=$param -o test_timing test_timing.c sign.c address.c randombytes.c fors.c merkle.c wots.c wotsx1.c utils.c utilsx1.c $HASH_SRC -I. -lcrypto || exit 1; \
  for i in $(seq 1 100); do \
    output=$(./test_timing); \
    echo \"$output\"; \
    keygen=$(echo \"$output\" | grep 'Average key generation time:' | awk '{print $5}'); \
    sign=$(echo \"$output\" | grep 'Average signing time:' | awk '{print $4}'); \
    verify=$(echo \"$output\" | grep 'Average verification time:' | awk '{print $4}'); \
    # For SPHINCS+ no rejections occur, so we pass \"0\" as a placeholder \
    python3 generate_graph.py \"$param\" \"$keygen\" \"$sign\" \"$verify\" \"0\"; \
  done; \
done; \
echo 'Benchmark loop complete. Listing /results directory:'; ls -l /results; \
echo 'Done.'"]

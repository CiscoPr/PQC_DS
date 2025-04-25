# 1) Base image + packages
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
      build-essential \
      git \
      ca-certificates \
      make \
      libssl-dev \
      python3 \
      python3-pip && \
    python3 -m pip install pandas matplotlib && \
    rm -rf /var/lib/apt/lists/*

# 2) Clone SPHINCS+
WORKDIR /sphincsplus
RUN git clone https://github.com/sphincs/sphincsplus.git .

# 3) Bring in your harness + graph script
WORKDIR /sphincsplus/ref
COPY test_timing.c generate_graph.py ./

# 4) Build the “ref” lib
RUN make clean && make

# 7) Run timing tests for all THASH + HASH + parameter sets and save output
CMD ["/bin/sh", "-c", "\
mkdir -p /results && \
for HASH in haraka shake sha2; do \
  for THASH in robust simple; do \
    for VAR in 128s 128f 192s 192f 256s 256f; do \
      echo; echo \"=== Building sphincs-$HASH-$VAR ($THASH) ===\"; \
      # Select proper sources for each HASH type \
      if [ \"$HASH\" = \"haraka\" ]; then \
        HASH_C=\"haraka.c hash_haraka.c\"; THASH_C=\"thash_haraka_${THASH}.c\"; \
      elif [ \"$HASH\" = \"shake\" ]; then \
        HASH_C=\"fips202.c hash_shake.c\"; THASH_C=\"thash_shake_${THASH}.c\"; \
      elif [ \"$HASH\" = \"sha2\" ]; then \
        HASH_C=\"sha2.c hash_sha2.c\"; THASH_C=\"thash_sha2_${THASH}.c\"; \
      fi; \
      gcc -mavx2 -march=haswell \
          -Wall -Wextra -Wpedantic -O3 -std=c99 \
          -Wconversion -Wmissing-prototypes \
          -DPARAMS=sphincs-$HASH-$VAR -DTHASH=$THASH \
          -I. \
          test_timing.c \
            address.c randombytes.c merkle.c wots.c wotsx1.c \
            utils.c utilsx1.c fors.c sign.c \
            $HASH_C $THASH_C \
          -lcrypto -lrt \
          -o test_timing-$HASH-$VAR-$THASH; \
      mkdir -p /results/$HASH/$THASH/sphincs-$HASH-$VAR; \
      for ITER in $(seq 1 100); do \
        echo \"--- Iteration $ITER for $HASH-$VAR ($THASH) ---\"; \
        ./test_timing-$HASH-$VAR-$THASH | tee out; \
        kg=$(grep 'Average key generation time:' out | awk '{print $5}'); \
        sg=$(grep 'Average signing time:'        out | awk '{print $4}'); \
        vg=$(grep 'Average verification time:'   out | awk '{print $4}'); \
        [ -z \"$kg\" ] && kg=0; [ -z \"$sg\" ] && sg=0; [ -z \"$vg\" ] && vg=0; \
        python3 generate_graph.py $HASH $THASH $VAR \"$kg\" \"$sg\" \"$vg\" 0; \
      done; \
    done; \
  done; \
done; \
echo 'All done — see /results/<hash>/<thash>/sphincs-*/ for outputs.'"]


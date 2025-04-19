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

# 3) Drop into the ref/ directory and bring in your harness + graph script
WORKDIR /sphincsplus/ref
COPY test_timing.c generate_graph.py ./

# 4) Build the “ref” lib
RUN make clean && make

# 5) Compile the timing harness; we’ll overwrite this for each variant in the CMD loop
RUN gcc -mavx2 -march=haswell \
    -Wall -Wextra -Wpedantic -O3 -std=c99 \
    -Wconversion -Wmissing-prototypes \
    -DPARAMS=sphincs-haraka-128f -DTHASH=robust \
    -I. \
    test_timing.c \
      address.c randombytes.c merkle.c wots.c wotsx1.c \
      utils.c utilsx1.c fors.c sign.c \
      haraka.c hash_haraka.c thash_haraka_robust.c \
    -lcrypto -lrt \
    -o test_timing

# 6) Prepare results dir
RUN mkdir -p /results

# 7) For each Haraka‑128s/128f/192s/192f/256s/256f, rebuild, retest and re‑graph
CMD ["bash","-lc", "\
for VAR in 128s 128f 192s 192f 256s 256f; do \
  echo; echo \"=== Building & testing sphincs-haraka-$VAR ===\"; \
  gcc -mavx2 -march=haswell \
      -Wall -Wextra -Wpedantic -O3 -std=c99 \
      -Wconversion -Wmissing-prototypes \
      -DPARAMS=\"sphincs-haraka-$VAR\" -DTHASH=robust \
      -I. \
      test_timing.c \
        address.c randombytes.c merkle.c wots.c wotsx1.c \
        utils.c utilsx1.c fors.c sign.c \
        haraka.c hash_haraka.c thash_haraka_robust.c \
      -lcrypto -lrt \
      -o test_timing-$VAR; \
  mkdir -p /results/haraka-$VAR; \
  for i in $(seq 1 100); do \
    echo; echo \"--- run #$i for sphincs-haraka-$VAR ---\"; \
    ./test_timing-$VAR | tee out; \
    kg=$(grep 'Average key generation time:' out | awk '{print $5}'); \
    sg=$(grep 'Average signing time:'        out | awk '{print $4}'); \
    vg=$(grep 'Average verification time:'  out | awk '{print $4}'); \
    [ -z \"$kg\" ] && kg=0; [ -z \"$sg\" ] && sg=0; [ -z \"$vg\" ] && vg=0; \
    python3 generate_graph.py haraka-$VAR \"$kg\" \"$sg\" \"$vg\" 0; \
    # now move the fresh CSV + PNG into our subfolder
    mv /results/haraka-$VAR.* /results/haraka-$VAR/; \
  done; \
done; \
echo 'All done — subdirectories under /results each contain their own CSV + plot.' \
"]
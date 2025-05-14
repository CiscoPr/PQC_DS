FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    make \
    libssl-dev \
    unzip \
    curl \
    python3 \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install pandas matplotlib

WORKDIR /falcon
RUN curl -L -o falcon.zip https://falcon-sign.info/falcon-round3.zip
RUN unzip falcon.zip && rm falcon.zip

# Copy source files to both Falcon-512 and Falcon-1024 folders
WORKDIR /falcon/falcon-round3/Reference_Implementation

COPY test_timing.c ./test_timing.c
COPY ../KAT/generator/katrng.c ./katrng.c
COPY ../KAT/generator/katrng.h ./katrng.h
COPY generate_graph.py /generate_graph.py

# Build Falcon-512
WORKDIR /falcon/falcon-round3/Reference_Implementation/falcon512/falcon512int
RUN make clean && make
RUN gcc -O2 -DFALCON_MODE=512 -o test_timing_512 ../../test_timing.c ../../katrng.c rng.c sign.c vrfy.c keygen.c codec.c common.c fft.c fpr.c shake.c nist.c -I. -I../../

# Build Falcon-1024
WORKDIR /falcon/falcon-round3/Reference_Implementation/falcon1024/falcon1024int
RUN make clean && make
RUN gcc -O2 -DFALCON_MODE=1024 -o test_timing_1024 ../../test_timing.c ../../katrng.c rng.c sign.c vrfy.c keygen.c codec.c common.c fft.c fpr.c shake.c nist.c -I. -I../../

# Prepare results folder
RUN mkdir -p /results/512 /results/1024

# Entry point script
# Entry point script
RUN printf '#!/bin/bash\n\
for MODE in 512 1024; do\n\
  echo "Running $MODE..."\n\
  EXE="/falcon/falcon-round3/Reference_Implementation/falcon${MODE}/falcon${MODE}int/test_timing_${MODE}"\n\
  for i in {1..100}; do\n\
    echo "Run $i for Falcon-$MODE..."\n\
    $EXE > out\n\
    kg=$(grep "Average key generation time:" out | awk "{print \\$5}")\n\
    sg=$(grep "Average signing time:"        out | awk "{print \\$4}")\n\
    vg=$(grep "Average verification time:"   out | awk "{print \\$4}")\n\
    python3 /generate_graph.py "${MODE}" "$kg" "$sg" "$vg"\n\
  done\n\
done\n' > /run_timing.sh && chmod +x /run_timing.sh



CMD ["/run_timing.sh"]

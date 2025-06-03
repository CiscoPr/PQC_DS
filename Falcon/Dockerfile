# ─────────────────────────────────────────────────────────────────────────────
# Dockerfile to build Falcon‐round3 (512 and 1024), compile test_timing.c,
# and then run a shell command that loops over both modes and calls
# generate_graph.py. We include katrng.c so that randombytes() is defined.
# ─────────────────────────────────────────────────────────────────────────────
FROM ubuntu:22.04

# 1) Install OS‐level dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      build-essential \
      gcc \
      make \
      git \
      curl \
      unzip \
      libssl-dev \
      python3 \
      python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 2) Install Python packages needed by generate_graph.py
RUN python3 -m pip install --no-cache-dir pandas matplotlib

# 3) Set /opt as our workspace
WORKDIR /opt

# 4) Download and unzip the official "falcon-round3" reference archive
#    (this will create /opt/falcon-round3)
RUN curl -L -o falcon-round3.zip https://falcon-sign.info/falcon-round3.zip && \
    unzip falcon-round3.zip && \
    rm falcon-round3.zip

# 5) Build the 512‐bit reference implementation
WORKDIR /opt/falcon-round3/Reference_Implementation/falcon512/falcon512int
RUN make clean && make

# 6) Build the 1024‐bit reference implementation
WORKDIR /opt/falcon-round3/Reference_Implementation/falcon1024/falcon1024int
RUN make clean && make

# 7) Copy your test_timing.c and generate_graph.py into /opt
#    (Assumes you have test_timing.c and generate_graph.py next to this Dockerfile)
COPY test_timing.c     /opt/test_timing.c
COPY generate_graph.py /opt/generate_graph.py

# 8) Compile two executables: test_timing_512 and test_timing_1024
#    We add the KAT generator path (-I../../../../KAT/generator) so that katrng.h is found,
#    and link katrng.c from /opt/falcon-round3/KAT/generator/ so that randombytes() is defined.

# Build Falcon‐512 timing binary
WORKDIR /opt/falcon-round3/Reference_Implementation/falcon512/falcon512int
RUN gcc -O2 -Wall -DFALCON_MODE=512 \
    /opt/test_timing.c \
    codec.c common.c fft.c fpr.c keygen.c nist.c rng.c shake.c sign.c vrfy.c \
    /opt/falcon-round3/KAT/generator/katrng.c \
    -I. \
    -I/opt/falcon-round3/KAT/generator \
    -o /opt/test_timing_512

# Build Falcon‐1024 timing binary
WORKDIR /opt/falcon-round3/Reference_Implementation/falcon1024/falcon1024int
RUN gcc -O2 -Wall -DFALCON_MODE=1024 \
    /opt/test_timing.c \
    codec.c common.c fft.c fpr.c keygen.c nist.c rng.c shake.c sign.c vrfy.c \
    /opt/falcon-round3/KAT/generator/katrng.c \
    -I. \
    -I/opt/falcon-round3/KAT/generator \
    -o /opt/test_timing_1024

# 9) Make directories for results
RUN mkdir -p /opt/results/512 /opt/results/1024

# 10) Expose the working directory for container runtime
WORKDIR /opt

# 11) Use CMD ["sh", "-c", "..."] to run a one‐liner with an embedded loop when the container starts.
#     This loops over MODE in {512,1024}, runs the corresponding binary 10 times each,
#     greps out the three reported times, and calls generate_graph.py accordingly.
#
CMD [ "sh", "-c", "\
  for MODE in 512 1024; do \
    BIN=\"/opt/test_timing_${MODE}\"; \
    if [ ! -x \"$BIN\" ]; then \
      echo \"*** ERROR: timing binary not found: $BIN\" >&2; exit 1; \
    fi; \
    echo \"---- Running Falcon-$MODE timing loop ----\"; \
    for i in $(seq 1 100); do \
      echo \"Run #$i for Falcon-$MODE...\"; \
      OUTFILE=\"/opt/out.txt\"; \
      $BIN > \"$OUTFILE\" 2>&1; \
      KG=$(grep \"Average key generation time:\"   \"$OUTFILE\" | awk '{print $5}'); \
      SG=$(grep \"Average signing time:\"          \"$OUTFILE\" | awk '{print $4}'); \
      VG=$(grep \"Average verification time:\"     \"$OUTFILE\" | awk '{print $4}'); \
      echo \"Falcon-${MODE}, iteration ${i}, keygen=${KG}, sign=${SG}, verify=${VG}\"; \
      python3 /opt/generate_graph.py \"$MODE\" \"$KG\" \"$SG\" \"$VG\"; \
    done; \
  done\n" ]

# ─────────────────────────────────────────────────────────────────────────────

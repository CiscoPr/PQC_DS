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

# 5) Overwrite sign.c in the Falcon-512 folder with our patched version
COPY ./Reference_Implementation/falcon512/falcon512int/sign.c /opt/falcon-round3/Reference_Implementation/falcon512/falcon512int/sign.c
COPY ./Reference_Implementation/falcon512/falcon512int/keygen.c /opt/falcon-round3/Reference_Implementation/falcon512/falcon512int/keygen.c

# 6) Build the 512‐bit reference implementation
WORKDIR /opt/falcon-round3/Reference_Implementation/falcon512/falcon512int
RUN make clean && make

# 7) Overwrite sign.c in the Falcon-1024 folder with our patched version
COPY ./Reference_Implementation/falcon1024/falcon1024int/sign.c /opt/falcon-round3/Reference_Implementation/falcon1024/falcon1024int/sign.c
COPY ./Reference_Implementation/falcon1024/falcon1024int/keygen.c /opt/falcon-round3/Reference_Implementation/falcon1024/falcon1024int/keygen.c

# 8) Build the 1024‐bit reference implementation
WORKDIR /opt/falcon-round3/Reference_Implementation/falcon1024/falcon1024int
RUN make clean && make

# 9) Copy your test_timing.c and generate_graph.py into /opt
COPY test_timing.c     /opt/test_timing.c
COPY generate_graph.py /opt/generate_graph.py

# 10) Compile two executables: test_timing_512 and test_timing_1024
#     We add the KAT generator path so that katrng.h is found,
#     and link katrng.c from /opt/falcon-round3/KAT/generator/ so that randombytes() is defined.

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

# 11) Make directories for results
RUN mkdir -p /opt/results/512 /opt/results/1024

# 12) Expose the working directory for container runtime
WORKDIR /opt

# 13) Use CMD ["sh", "-c", "..."] to run a one‐liner with an embedded loop when the container starts.
CMD ["sh", "-c", "\
  for MODE in 512 1024; do \
    BIN=\"/opt/test_timing_${MODE}\"; \
    if [ ! -x \"$BIN\" ]; then echo \"*** ERROR: timing binary not found: $BIN\" >&2; exit 1; fi; \
    echo \"---- Running Falcon-$MODE timing loop ----\"; \
    for i in $(seq 1 25); do \
      echo \"Run #$i for Falcon-$MODE...\"; \
      OUTFILE=\"/opt/out.txt\"; \
      $BIN > \"$OUTFILE\" 2>&1; \
      KG=$(grep \"Average key generation time:\"   \"$OUTFILE\" | awk '{print $5}'); \
      SG=$(grep \"Average signing time:\"          \"$OUTFILE\" | awk '{print $4}'); \
      VG=$(grep \"Average verification time:\"     \"$OUTFILE\" | awk '{print $4}'); \
      REJ=$(grep \"Average rejections per sign:\" \"$OUTFILE\" | awk '{print $5}'); \
      NTRU=$(grep \"Average NTRU solving time:\" \"$OUTFILE\" | awk '{print $5}'); \
      GAUSS=$(grep \"Average Gaussian sampling time:\" \"$OUTFILE\" | awk '{print $5}'); \
      FFT=$(grep \"Average FFT time:\" \"$OUTFILE\" | awk '{print $4}'); \
      echo \"Falcon-${MODE}, iteration ${i}, keygen=${KG}, sign=${SG}, verify=${VG}, rejections=${REJ}, ntru_timing=${NTRU}, gauss_timing=${GAUSS}, fft_timing=${FFT}\"; \
      python3 /opt/generate_graph.py \"$MODE\" \"$KG\" \"$SG\" \"$VG\" \"$REJ\" \"$NTRU\" \"$GAUSS\" \"$FFT\"; \
    done; \
  done\
"]

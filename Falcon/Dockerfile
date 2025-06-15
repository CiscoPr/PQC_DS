# ─────────────────────────────────────────────────────────────────────────────
# Dockerfile to clone Falcon-round3, build the Extra/C harness (test_falcon.c),
# compile your 11 focused drivers, and run each to hit exactly one stderr error.
# ─────────────────────────────────────────────────────────────────────────────
FROM ubuntu:20.04

# 1) Install build deps
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      build-essential \
      clang \
      make \
      git \
      curl \
      unzip \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2) Fetch Falcon-round3
WORKDIR /falcon
RUN curl -L -o falcon3.zip https://falcon-sign.info/falcon-round3.zip && \
    unzip falcon3.zip && \
    rm falcon3.zip

# 3) Build the reference C in Extra/c
WORKDIR /falcon/falcon-round3/Extra/c
RUN make


# 4) Remove static + rename main properly
RUN sed -E 's/^[[:space:]]*static[[:space:]]+//g' -i test_falcon.c && \
    perl -0777 -i -pe 's/int\s+main\s*\((.*?)\)/void test_falcon_harness(\1)/s' test_falcon.c && \
    gcc -O2 -fPIC -I. -c test_falcon.c -o harness.o



# 5) Copy in your 11 error-drivers (keygen_failed.c, makepub_failed.c, …, wrong_pub_enc_length.c)
COPY tests/*.c ./tests/

# 6) Compile each driver into its own executable under /falcon/testsbin
WORKDIR /falcon/falcon-round3/Extra/c
# 6) Compile each test driver into /falcon/testsbin/
RUN mkdir -p /falcon/testsbin && \
    for src in tests/*.c; do \
      name=$(basename "$src" .c); \
      gcc -O2 -fPIC -no-pie -I. \
        harness.o codec.o common.o falcon.o fft.o fpr.o keygen.o \
        rng.o shake.o sign.o vrfy.o \
        "$src" -o /falcon/testsbin/"$name"; \
    done

# 7) Run every test (including full test_falcon harness)
CMD ["sh","-c","\
  set +e; \
  for exe in /falcon/testsbin/*; do \
    echo; echo '======================================='; \
    echo \"Running $(basename \"$exe\"):\"; \
    echo '======================================='; \
    \"$exe\"; \
  done"]

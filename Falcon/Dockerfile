FROM ubuntu:20.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    git \
    curl \
    unzip \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Create workdir and fetch Falcon
WORKDIR /falcon
RUN curl -L -o falcon3.zip https://falcon-sign.info/falcon-round3.zip && \
    unzip falcon3.zip && rm falcon3.zip

# Move to Reference Implementation path
WORKDIR /falcon/falcon-round3

# Copy your override files into the container
COPY tests/keypair_error.c ./tests/
COPY tests/open_error.c ./tests/
COPY tests/open_bad_m.c ./tests/
COPY tests/open_bad_mlen.c ./tests/
COPY tests/sign_error.c ./tests/

# Now compile everything properly
RUN gcc -O2 \
    -I Reference_Implementation/falcon512/falcon512int \
    -I KAT/generator \
    KAT/generator/PQCgenKAT_sign.c \
    KAT/generator/katrng.c \
    Reference_Implementation/falcon512/falcon512int/codec.c \
    Reference_Implementation/falcon512/falcon512int/common.c \
    Reference_Implementation/falcon512/falcon512int/fft.c \
    Reference_Implementation/falcon512/falcon512int/fpr.c \
    Reference_Implementation/falcon512/falcon512int/keygen.c \
    Reference_Implementation/falcon512/falcon512int/rng.c \
    Reference_Implementation/falcon512/falcon512int/shake.c \
    Reference_Implementation/falcon512/falcon512int/vrfy.c \
    tests/keypair_error.c \
    -o test_keypair

RUN gcc -O2 \
    -I Reference_Implementation/falcon512/falcon512int \
    -I KAT/generator \
    KAT/generator/PQCgenKAT_sign.c \
    KAT/generator/katrng.c \
    Reference_Implementation/falcon512/falcon512int/codec.c \
    Reference_Implementation/falcon512/falcon512int/common.c \
    Reference_Implementation/falcon512/falcon512int/fft.c \
    Reference_Implementation/falcon512/falcon512int/fpr.c \
    Reference_Implementation/falcon512/falcon512int/keygen.c \
    Reference_Implementation/falcon512/falcon512int/rng.c \
    Reference_Implementation/falcon512/falcon512int/shake.c \
    Reference_Implementation/falcon512/falcon512int/vrfy.c \
    tests/sign_error.c \
    -o test_sign

RUN gcc -O2 \
    -I Reference_Implementation/falcon512/falcon512int \
    -I KAT/generator \
    KAT/generator/PQCgenKAT_sign.c \
    KAT/generator/katrng.c \
    Reference_Implementation/falcon512/falcon512int/codec.c \
    Reference_Implementation/falcon512/falcon512int/common.c \
    Reference_Implementation/falcon512/falcon512int/fft.c \
    Reference_Implementation/falcon512/falcon512int/fpr.c \
    Reference_Implementation/falcon512/falcon512int/keygen.c \
    Reference_Implementation/falcon512/falcon512int/rng.c \
    Reference_Implementation/falcon512/falcon512int/shake.c \
    Reference_Implementation/falcon512/falcon512int/vrfy.c \
    tests/open_error.c \
    -o test_ver_open_err

RUN gcc -O2 \
    -I Reference_Implementation/falcon512/falcon512int \
    -I KAT/generator \
    KAT/generator/PQCgenKAT_sign.c \
    KAT/generator/katrng.c \
    Reference_Implementation/falcon512/falcon512int/codec.c \
    Reference_Implementation/falcon512/falcon512int/common.c \
    Reference_Implementation/falcon512/falcon512int/fft.c \
    Reference_Implementation/falcon512/falcon512int/fpr.c \
    Reference_Implementation/falcon512/falcon512int/keygen.c \
    Reference_Implementation/falcon512/falcon512int/rng.c \
    Reference_Implementation/falcon512/falcon512int/shake.c \
    Reference_Implementation/falcon512/falcon512int/vrfy.c \
    tests/open_bad_mlen.c \
    -o test_ver_mlen

RUN gcc -O2 \
    -I Reference_Implementation/falcon512/falcon512int \
    -I KAT/generator \
    KAT/generator/PQCgenKAT_sign.c \
    KAT/generator/katrng.c \
    Reference_Implementation/falcon512/falcon512int/codec.c \
    Reference_Implementation/falcon512/falcon512int/common.c \
    Reference_Implementation/falcon512/falcon512int/fft.c \
    Reference_Implementation/falcon512/falcon512int/fpr.c \
    Reference_Implementation/falcon512/falcon512int/keygen.c \
    Reference_Implementation/falcon512/falcon512int/rng.c \
    Reference_Implementation/falcon512/falcon512int/shake.c \
    Reference_Implementation/falcon512/falcon512int/vrfy.c \
    tests/open_bad_m.c \
    -o test_ver_msg



# Default run command to execute all tests
CMD /bin/sh -c "set +e; \
echo '== keypair error =='; ./test_keypair || true; echo; \
echo '== signing error =='; ./test_sign || true; echo; \
echo '== open error =='; ./test_ver_open_err || true; echo; \
echo '== bad mlen =='; ./test_ver_mlen || true; echo; \
echo '== bad message content =='; ./test_ver_msg || true"

#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include <string.h>
#include "sign.h"
#include "randombytes.h"

#define MLEN 32
#define CTXLEN 14
#define NUM_RUNS 10

// Helper function to return current time in seconds as a double.
static inline double get_time(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}

int main(void) {
    uint8_t pk[CRYPTO_PUBLICKEYBYTES];
    uint8_t sk[CRYPTO_SECRETKEYBYTES];
    uint8_t m[MLEN];
    uint8_t sm[MLEN + CRYPTO_BYTES];
    uint8_t m2[MLEN];
    size_t smlen, mlen;
    uint8_t ctx[CTXLEN];

    // Use a fixed context for testing.
    snprintf((char*)ctx, CTXLEN, "timing_test");

    double total_keygen_time = 0.0;
    double total_sign_time   = 0.0;
    double total_verify_time = 0.0;

    for (int i = 0; i < NUM_RUNS; i++) {
        // Generate a random message.
        randombytes(m, MLEN);
        // Measure key generation time.
        double start = get_time();
        crypto_sign_keypair(pk, sk);
        double end = get_time();
        total_keygen_time += (end - start);

        // Measure signing time.
        start = get_time();
        if (crypto_sign(sm, &smlen, m, MLEN, ctx, CTXLEN, sk)) {
            fprintf(stderr, "Signing failed in iteration %d\n", i);
            return -1;
        }

        end = get_time();
        total_sign_time += (end - start);

        // Measure verification time.
        start = get_time();
        int ret = crypto_sign_open(m2, &mlen, sm, smlen, ctx, CTXLEN, pk);
        end = get_time();
        total_verify_time += (end - start);

        if (ret != 0) {
            fprintf(stderr, "Verification failed in iteration %d\n", i);
            return -1;
        }
    }

    printf("Average key generation time: %.3f ms\n", (total_keygen_time / NUM_RUNS) * 1000.0);
    printf("Average signing time: %.3f ms\n", (total_sign_time / NUM_RUNS) * 1000.0);
    printf("Average verification time: %.3f ms\n", (total_verify_time / NUM_RUNS) * 1000.0);


    return 0;
}

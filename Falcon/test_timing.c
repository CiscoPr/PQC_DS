#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include <string.h>
#include "api.h"

#ifndef FALCON_MODE
#define FALCON_MODE 512
#endif

#define MLEN 32
#define NUM_RUNS 10

int randombytes(unsigned char *x, unsigned long long xlen);  // forward declaration
extern unsigned long high_level_rejection_count;   // from sign.c
extern unsigned long low_level_rejection_count;    // from sign.c

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
    uint8_t m2[MLEN + CRYPTO_BYTES];
    unsigned long long smlen, mlen;

    double total_keygen_time = 0.0;
    double total_sign_time   = 0.0;
    double total_verify_time = 0.0;
    unsigned long total_high_level_rejections = 0;
    unsigned long total_low_level_rejections = 0;

    for (int i = 0; i < NUM_RUNS; i++) {
        randombytes(m, MLEN);

        // Reset counters before each iteration
        high_level_rejection_count = 0;
        low_level_rejection_count = 0;

        // Measure key generation time
        double start = get_time();
        if (crypto_sign_keypair(pk, sk)) {
            fprintf(stderr, "Key generation failed in iteration %d\n", i);
            return -1;
        }
        double end = get_time();
        total_keygen_time += (end - start);

        // Measure signing time
        start = get_time();
        if (crypto_sign(sm, &smlen, m, MLEN, sk)) {
            fprintf(stderr, "Signing failed in iteration %d\n", i);
            return -1;
        }
        end = get_time();
        total_sign_time += (end - start);

        // Measure verification time
        start = get_time();
        if (crypto_sign_open(m2, &mlen, sm, smlen, pk)) {
            fprintf(stderr, "Verification failed in iteration %d\n", i);
            return -1;
        }
        end = get_time();
        total_verify_time += (end - start);

        // Accumulate total rejection counts
        total_high_level_rejections += high_level_rejection_count;
        total_low_level_rejections += low_level_rejection_count;
    }

    double avg_keygen_ms = (total_keygen_time / NUM_RUNS) * 1000.0;
    double avg_sign_ms   = (total_sign_time   / NUM_RUNS) * 1000.0;
    double avg_verify_ms = (total_verify_time / NUM_RUNS) * 1000.0;
    double avg_high_level_rejections = (double)total_high_level_rejections / (double)NUM_RUNS;
    double avg_low_level_rejections = (double)total_low_level_rejections / (double)NUM_RUNS;

    printf("Average key generation time:          %.3f ms\n", avg_keygen_ms);
    printf("Average signing time:                 %.3f ms\n", avg_sign_ms);
    printf("Average verification time:            %.3f ms\n", avg_verify_ms);
    printf("Average high-level rejections:        %.4f\n", avg_high_level_rejections);
    printf("Average low-level rejections:         %.4f\n", avg_low_level_rejections);

    return 0;
}

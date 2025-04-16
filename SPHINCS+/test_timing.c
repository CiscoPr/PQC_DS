#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include "params.h"
#include "api.h"

#define NUM_RUNS 1000
#define MSG_LEN 32

// Helper function to get current time (in seconds)
static inline double get_time(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}

int main(void) {
    uint8_t pk[CRYPTO_PUBLICKEYBYTES];
    uint8_t sk[CRYPTO_SECRETKEYBYTES];
    uint8_t m[MSG_LEN] = {0};
    uint8_t sm[MSG_LEN + CRYPTO_BYTES];
    uint8_t m2[MSG_LEN];
    size_t smlen, mlen;

    double total_keygen = 0, total_sign = 0, total_verify = 0;

    for (int i = 0; i < NUM_RUNS; i++) {
        double start, end;

        // Measure key pair generation time
        start = get_time();
        crypto_sign_keypair(pk, sk);
        end = get_time();
        total_keygen += (end - start);

        // Measure signing time
        start = get_time();
        crypto_sign(sm, &smlen, m, MSG_LEN, sk);
        end = get_time();
        total_sign += (end - start);

        // Measure verification time
        start = get_time();
        if (crypto_sign_open(m2, &mlen, sm, smlen, pk) != 0) {
            printf("Verification failed at iteration %d\n", i);
            return -1;
        }
        end = get_time();
        total_verify += (end - start);
    }

    printf("Average key generation time: %.3f ms\n", (total_keygen / NUM_RUNS) * 1000.0);
    printf("Average signing time: %.3f ms\n", (total_sign / NUM_RUNS) * 1000.0);
    printf("Average verification time: %.3f ms\n", (total_verify / NUM_RUNS) * 1000.0);

    return 0;
}

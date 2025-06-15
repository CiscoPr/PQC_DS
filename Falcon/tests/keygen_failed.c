/* tests/keygen_failed.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "inner.h"
#include "falcon.h"

int main(void) {
    shake256_context rng;
    shake256_init_prng_from_seed(&rng, "test", 4);

    int r = falcon_keygen_make(&rng, 9,
        NULL, 0,
        malloc(FALCON_PUBKEY_SIZE(9)), FALCON_PUBKEY_SIZE(9),
        NULL, 0);

    fprintf(stderr, "keygen failed: %d\n", r);
    return EXIT_FAILURE;
}
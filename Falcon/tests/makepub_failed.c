/* tests/makepub_failed.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "inner.h"
#include "falcon.h"

int main(void) {
    inner_shake256_context rng;
    inner_shake256_init(&rng);
    size_t priv_len = FALCON_PRIVKEY_SIZE(9);
    void *priv = malloc(priv_len);
    memset(priv,0,priv_len);
    /* provoke makepub failure by zero‐length pubkey output */
    int r = falcon_make_public(NULL, 0, priv, priv_len, NULL, 0);
    fprintf(stderr, "makepub failed: %d\n", r);
    return EXIT_FAILURE;
}
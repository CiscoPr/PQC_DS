#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include "api.h"
#include "params.h"

/*
 * Override crypto_sign_verify:
 * Call the original function and if it returns success (0), force a failure by returning 1.
 */
int crypto_sign_verify(const uint8_t *sig, size_t siglen,
                       const uint8_t *m, size_t mlen, const uint8_t *pk) {
    typedef int (*orig_crypto_sign_verify_t)(const uint8_t *, size_t, const uint8_t *, size_t, const uint8_t *);
    orig_crypto_sign_verify_t orig = (orig_crypto_sign_verify_t)dlsym(RTLD_NEXT, "crypto_sign_verify");
    if (!orig) {
        fprintf(stderr, "Error: could not find original crypto_sign_verify\n");
        exit(1);
    }
    int ret = orig(sig, siglen, m, mlen, pk);
    if (ret == 0)
        ret = 1;  // Force failure.
    return ret;
}

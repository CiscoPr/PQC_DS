#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "api.h"
#include "params.h"

/*
 * Override crypto_sign_open:
 * Call the original function; if m (the output) equals sm (the input), then corrupt m and force failure.
 */
int crypto_sign_open(unsigned char *m, unsigned long long *mlen,
                     const unsigned char *sm, unsigned long long smlen,
                     const unsigned char *pk) {
    typedef int (*orig_crypto_sign_open_t)(unsigned char *, unsigned long long *, const unsigned char *, unsigned long long, const unsigned char *);
    orig_crypto_sign_open_t orig = (orig_crypto_sign_open_t)dlsym(RTLD_NEXT, "crypto_sign_open");
    if (!orig) {
        fprintf(stderr, "Error: could not find original crypto_sign_open\n");
        exit(1);
    }
    int ret = orig(m, mlen, sm, smlen, pk);
    if (m == sm) { // in-place verification
        if (mlen && *mlen > 0)
            m[0] ^= 0x0F;  // corrupt the recovered message.
        ret = -1;
    }
    return ret;
}

#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include "api.h"
#include "params.h"

/*
 * Override crypto_sign_keypair:
 * Call the original routine (using RTLD_NEXT) and then tweak the generated public key.
 */
int crypto_sign_keypair(unsigned char *pk, unsigned char *sk) {
    typedef int (*orig_crypto_sign_keypair_t)(unsigned char *, unsigned char *);
    orig_crypto_sign_keypair_t orig = (orig_crypto_sign_keypair_t)dlsym(RTLD_NEXT, "crypto_sign_keypair");
    if (!orig) {
        fprintf(stderr, "Error: could not find original crypto_sign_keypair\n");
        exit(1);
    }
    int ret = orig(pk, sk);
    /* Tweak the public key in a nontrivial way */
    pk[0] ^= 0x0F;
    pk[3] ^= 0xF0;
    return ret;
}

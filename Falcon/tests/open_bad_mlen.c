// tests/open_bad_mlen.c
#include "api.h"

/*
  Return success but lie about the recovered message length.
  smlen is the signature+message length, so smlen-CRYPTO_BYTES == original mlen.
*/
int crypto_sign_open(unsigned char *m1,
                     unsigned long long *mlen1,
                     const unsigned char *sm,
                     unsigned long long smlen,
                     const unsigned char *pk)
{
    (void)m1; (void)pk;
    unsigned long long orig = smlen - CRYPTO_BYTES;
    *mlen1 = orig + 1;      /* off by one */
    return 0;                /* success */
}

/* dummy stubs so linker doesn't complain */
int crypto_sign(unsigned char *sm, unsigned long long *smlen,
                const unsigned char *m, unsigned long long mlen,
                const unsigned char *sk) {
    (void)sm; (void)smlen; (void)m; (void)mlen; (void)sk;
    return 0;
}

/* force keypair to fail */
int crypto_sign_keypair(unsigned char *pk, unsigned char *sk) {
    (void)pk; (void)sk;
    return 0;
}
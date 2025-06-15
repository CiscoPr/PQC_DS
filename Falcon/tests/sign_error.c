// tests/sign_error.c
#include "api.h"

/* force signing to fail */
int crypto_sign(unsigned char *sm,
                unsigned long long *smlen,
                const unsigned char *m,
                unsigned long long mlen,
                const unsigned char *sk)
{
    (void)sm; (void)smlen;
    (void)m; (void)mlen; (void)sk;
    return -1;
}

int crypto_sign_open(unsigned char *m1, unsigned long long *mlen1,
                     const unsigned char *sm, unsigned long long smlen,
                     const unsigned char *pk) {
    (void)m1; (void)mlen1; (void)sm; (void)smlen; (void)pk;
    return 0;
}

/* force keypair to fail */
int crypto_sign_keypair(unsigned char *pk, unsigned char *sk) {
    (void)pk; (void)sk;
    return 0;
}

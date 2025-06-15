// tests/open_bad_m.c
#include "api.h"
#include <string.h>

/*
  Return success and correct length, but do *not* copy the real message into m1
  (calloc in PQCgenKAT_sign gives you all-zero m1, so memcmp will fail).
*/
int crypto_sign_open(unsigned char *m1,
                     unsigned long long *mlen1,
                     const unsigned char *sm,
                     unsigned long long smlen,
                     const unsigned char *pk)
{
    (void)sm; (void)pk;
    unsigned long long orig = smlen - CRYPTO_BYTES;
    *mlen1 = orig;          /* correct length */
    /* leave m1 zeroed (it was calloc’d by the test harness) */
    return 0;
}

/* force keypair to fail */
int crypto_sign_keypair(unsigned char *pk, unsigned char *sk) {
    (void)pk; (void)sk;
    return 0;
}

/* dummy stubs so linker doesn't complain */
int crypto_sign(unsigned char *sm, unsigned long long *smlen,
                const unsigned char *m, unsigned long long mlen,
                const unsigned char *sk) {
    (void)sm; (void)smlen; (void)m; (void)mlen; (void)sk;
    return 0;
}
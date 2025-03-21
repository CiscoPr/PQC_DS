#define _GNU_SOURCE
#include <dlfcn.h>
#include <string.h>
#include "fors.h"     // For fors_pk_from_sig prototype.
#include "params.h"

/* Override fors_pk_from_sig:
   We call the original implementation (retrieved via dlsym from RTLD_DEFAULT)
   then flip a bit in the computed public key so that test/fors.c’s memcmp fails.
*/
void fors_pk_from_sig(unsigned char *pk, const unsigned char *sig, const unsigned char *m,
                      const spx_ctx* ctx, const uint32_t fors_addr[8]) {
    typedef void (*orig_fors_pk_from_sig_t)(unsigned char *, const unsigned char *, const unsigned char *, const spx_ctx*, const uint32_t *);
    orig_fors_pk_from_sig_t orig = (orig_fors_pk_from_sig_t)dlsym(RTLD_DEFAULT, "fors_pk_from_sig");
    if (orig)
        orig(pk, sig, m, ctx, fors_addr);
    /* Force failure: flip the least significant bit of the first byte */
    pk[0] ^= 0x01;
}


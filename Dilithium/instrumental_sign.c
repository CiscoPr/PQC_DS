#include <stdio.h>
#include <stdint.h>
#include "params.h"
#include "sign.h"
#include "packing.h"
#include "polyvec.h"
#include "poly.h"
#include "randombytes.h"
#include "symmetric.h"
#include "fips202.h"


static int last_rejection_count = 0;
int get_last_rejection_count(void) {
    return last_rejection_count;
}


int crypto_sign_signature_internal(uint8_t *sig,
                                   size_t *siglen,
                                   const uint8_t *m,
                                   size_t mlen,
                                   const uint8_t *pre,
                                   size_t prelen,
                                   const uint8_t rnd[RNDBYTES],
                                   const uint8_t *sk)
{
    unsigned int n;
    uint8_t seedbuf[2 * SEEDBYTES + TRBYTES + 2 * CRHBYTES];
    uint8_t *rho, *tr, *key, *mu, *rhoprime;
    uint16_t nonce = 0;
    polyvecl mat[K], s1, y, z;
    polyveck t0, s2, w1, w0, h;
    poly cp;
    keccak_state state;
    int rejection_count = 0; // Initialize rejection counter

    rho = seedbuf;
    tr = rho + SEEDBYTES;
    key = tr + TRBYTES;
    mu = key + SEEDBYTES;
    rhoprime = mu + CRHBYTES;
    unpack_sk(rho, tr, key, &t0, &s1, &s2, sk);

    /* Compute mu = CRH(tr, pre, msg) */
    shake256_init(&state);
    shake256_absorb(&state, tr, TRBYTES);
    shake256_absorb(&state, pre, prelen);
    shake256_absorb(&state, m, mlen);
    shake256_finalize(&state);
    shake256_squeeze(mu, CRHBYTES, &state);

    /* Compute rhoprime = CRH(key, rnd, mu) */
    shake256_init(&state);
    shake256_absorb(&state, key, SEEDBYTES);
    shake256_absorb(&state, rnd, RNDBYTES);
    shake256_absorb(&state, mu, CRHBYTES);
    shake256_finalize(&state);
    shake256_squeeze(rhoprime, CRHBYTES, &state);

    /* Expand matrix and transform vectors */
    polyvec_matrix_expand(mat, rho);
    polyvecl_ntt(&s1);
    polyveck_ntt(&s2);
    polyveck_ntt(&t0);

rej:
    rejection_count++; // Increment every time we retry

    /* Sample intermediate vector y */
    polyvecl_uniform_gamma1(&y, rhoprime, nonce++);

    /* Matrix-vector multiplication */
    z = y;
    polyvecl_ntt(&z);
    polyvec_matrix_pointwise_montgomery(&w1, mat, &z);
    polyveck_reduce(&w1);
    polyveck_invntt_tomont(&w1);

    /* Decompose w and call the random oracle */
    polyveck_caddq(&w1);
    polyveck_decompose(&w1, &w0, &w1);
    polyveck_pack_w1(sig, &w1);

    shake256_init(&state);
    shake256_absorb(&state, mu, CRHBYTES);
    shake256_absorb(&state, sig, K * POLYW1_PACKEDBYTES);
    shake256_finalize(&state);
    shake256_squeeze(sig, CTILDEBYTES, &state);
    poly_challenge(&cp, sig);
    poly_ntt(&cp);

    /* Compute z, reject if it reveals secret */
    polyvecl_pointwise_poly_montgomery(&z, &cp, &s1);
    polyvecl_invntt_tomont(&z);
    polyvecl_add(&z, &z, &y);
    polyvecl_reduce(&z);
    if (polyvecl_chknorm(&z, GAMMA1 - BETA))
        goto rej;

    /* Check that subtracting cs2 does not change high bits of w and low bits
     * do not reveal secret information */
    polyveck_pointwise_poly_montgomery(&h, &cp, &s2);
    polyveck_invntt_tomont(&h);
    polyveck_sub(&w0, &w0, &h);
    polyveck_reduce(&w0);
    if (polyveck_chknorm(&w0, GAMMA2 - BETA))
        goto rej;

    /* Compute hints for w1 */
    polyveck_pointwise_poly_montgomery(&h, &cp, &t0);
    polyveck_invntt_tomont(&h);
    polyveck_reduce(&h);
    if (polyveck_chknorm(&h, GAMMA2))
        goto rej;

    polyveck_add(&w0, &w0, &h);
    n = polyveck_make_hint(&h, &w0, &w1);
    if (n > OMEGA)
        goto rej;

    /* Write signature */
    pack_sig(sig, sig, &z, &h);
    *siglen = CRYPTO_BYTES;

    last_rejection_count = rejection_count;


    return 0;
}


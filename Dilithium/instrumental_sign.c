#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include "params.h"
#include "sign.h"
#include "packing.h"
#include "polyvec.h"
#include "poly.h"
#include "randombytes.h"
#include "symmetric.h"
#include "fips202.h"

// Add near other global counters
static uint64_t total_z_overhead = 0, z_overhead_count = 0;
static uint64_t total_lowbits_overhead = 0, lowbits_overhead_count = 0;
static uint64_t total_hintnorm_overhead = 0, hintnorm_overhead_count = 0;
static uint64_t total_hintcount_overhead = 0, hintcount_overhead_count = 0;


static int last_znorm_rejection_count = 0;
static int last_lowbits_rejection_count = 0;
static int last_hitnorm_rejection_count = 0;
static int last_hitcount_rejection_count = 0;

static uint64_t total_z_time = 0, z_count = 0;
static uint64_t total_lowbits_time = 0, lowbits_count = 0;
static uint64_t total_hintnorm_time = 0, hintnorm_count = 0;
static uint64_t total_hintcount_time = 0, hintcount_count = 0;

int get_last_znorm_rejection_count(void) {
    return last_znorm_rejection_count;
}

int get_last_lowbits_rejection_count(void) {
    return last_lowbits_rejection_count;
}

int get_last_hitnorm_rejection_count(void) {
    return last_hitnorm_rejection_count;
}

int get_last_hitcount_rejection_count(void) {
    return last_hitcount_rejection_count;
}

static inline uint64_t get_time_us() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ((uint64_t)ts.tv_sec * 1000000ULL) + (ts.tv_nsec / 1000ULL);
}

static void log_rejection_time(const char* label, uint64_t duration_us) {
    FILE* f = fopen("/tmp/rejection_log.csv", "a");
    if (f) {
        fprintf(f, "%s,%llu\n", label, (unsigned long long)duration_us);
        fclose(f);
    }
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
    int znorm_rejection_count = 0; // Initialize znorm rejection counter
    int lowbits_rejection_count = 0; // Initialize lowbits rejection counter
    int hitnorm_rejection_count = 0; // Initialize hitnorm rejection counter
    int hitcount_rejection_count = 0; // Initialize hitcount rejection counter

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

    uint64_t loop_start_time = get_time_us();
rej:
    loop_start_time = get_time_us();  // Reset at start of each attempt


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
    // ZNORM
    uint64_t t_rej = get_time_us();
    if (polyvecl_chknorm(&z, GAMMA1 - BETA)){
        znorm_rejection_count++;
        total_z_time += (get_time_us() - t_rej);
        z_count++;
        total_z_overhead += (get_time_us() - loop_start_time);
        z_overhead_count++;
        goto rej;
    }

    /* Check that subtracting cs2 does not change high bits of w and low bits
     * do not reveal secret information */
    polyveck_pointwise_poly_montgomery(&h, &cp, &s2);
    polyveck_invntt_tomont(&h);
    polyveck_sub(&w0, &w0, &h);
    polyveck_reduce(&w0);
    //LOWBITS
    t_rej = get_time_us();
    if (polyveck_chknorm(&w0, GAMMA2 - BETA)){
        total_lowbits_time += (get_time_us() - t_rej);
        lowbits_count++;
        total_lowbits_overhead += (get_time_us() - loop_start_time);
        lowbits_overhead_count++;
        lowbits_rejection_count++;
        goto rej;
    }

    /* Compute hints for w1 */
    polyveck_pointwise_poly_montgomery(&h, &cp, &t0);
    polyveck_invntt_tomont(&h);
    polyveck_reduce(&h);
    t_rej = get_time_us();
    // HITNORM
    if (polyveck_chknorm(&h, GAMMA2)){
        hitnorm_rejection_count++;
        total_hintnorm_time += (get_time_us() - t_rej);
        hintnorm_count++;
        total_hintnorm_overhead += (get_time_us() - loop_start_time);
        hintnorm_overhead_count++;
        goto rej;
    }

    polyveck_add(&w0, &w0, &h);
    n = polyveck_make_hint(&h, &w0, &w1);
    t_rej = get_time_us();
    //HITCOUNT
    if (n > OMEGA){
        total_hintcount_time += (get_time_us() - t_rej);
        hintcount_count++;
        total_hintcount_overhead += (get_time_us() - loop_start_time);
        hintcount_overhead_count++;
        hitcount_rejection_count++;
        goto rej;
    }

    /* Write signature */
    pack_sig(sig, sig, &z, &h);
    *siglen = CRYPTO_BYTES;

    last_znorm_rejection_count = znorm_rejection_count;
    last_lowbits_rejection_count = lowbits_rejection_count;

    last_hitnorm_rejection_count = hitnorm_rejection_count;
    last_hitcount_rejection_count = hitcount_rejection_count;

    FILE *f = fopen("/results/rejection_timings.csv", "w");
    if (f) {
        fprintf(f, "rejection_label,avg_time_us\n");

        if (z_count)
            fprintf(f, "z_norm,%.5f\n", (double)total_z_time/z_count);
        if (z_overhead_count)
            fprintf(f, "z_norm_overhead,%.5f\n", (double)total_z_overhead/z_overhead_count);
        
        if (lowbits_count)
            fprintf(f, "lowbits,%.5f\n", (double)total_lowbits_time/lowbits_count);
        if (lowbits_overhead_count)
            fprintf(f, "lowbits_overhead,%.5f\n", (double)total_lowbits_overhead/lowbits_overhead_count);
        
        if (hintnorm_count)
            fprintf(f, "hint_norm,%.5f\n", (double)total_hintnorm_time/hintnorm_count);
        if (hintnorm_overhead_count)
            fprintf(f, "hint_norm_overhead,%.5f\n", (double)total_hintnorm_overhead/hintnorm_overhead_count);
        
        if (hintcount_count)
            fprintf(f, "hint_count,%.5f\n", (double)total_hintcount_time/hintcount_count);
        if (hintcount_overhead_count)
            fprintf(f, "hint_count_overhead,%.5f\n", (double)total_hintcount_overhead/hintcount_overhead_count);
        
        fclose(f);
    }

    return 0;
}


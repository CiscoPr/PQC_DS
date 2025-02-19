#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "params.h"
#include "sign.h"
#include "packing.h"
#include "polyvec.h"
#include "poly.h"
#include "symmetric.h"
#include "fips202.h"

// Override crypto_sign_verify_internal to force verification failure
int crypto_sign_verify_internal(const uint8_t *sig,
                                size_t siglen,
                                const uint8_t *m,
                                size_t mlen,
                                const uint8_t *pre,
                                size_t prelen,
                                const uint8_t *pk)
{
  // This simplified version computes a hash from (pk, pre, m)
  // and then deliberately corrupts the computed challenge.
  uint8_t mu[CRHBYTES];
  keccak_state state;
  uint8_t computed_challenge[CTILDEBYTES];
  uint8_t corrupted_challenge[CTILDEBYTES];

  // Compute a dummy mu (normally it would be CRH(H(rho,t1) || pre || m))
  shake256(mu, CRHBYTES, pk, CRYPTO_PUBLICKEYBYTES);

  // Simulate challenge computation from mu, pre, and m
  shake256_init(&state);
  shake256_absorb(&state, mu, CRHBYTES);
  shake256_absorb(&state, pre, prelen);
  shake256_absorb(&state, m, mlen);
  shake256_finalize(&state);
  shake256_squeeze(computed_challenge, CTILDEBYTES, &state);

  // Force error: flip the first bit of the computed challenge
  memcpy(corrupted_challenge, computed_challenge, CTILDEBYTES);
  corrupted_challenge[0] ^= 0xFF;

  // Compare the (corrupted) computed challenge with the challenge from sig.
  // Since they differ, we force verification to fail.
  for (size_t i = 0; i < CTILDEBYTES; i++) {
    if (sig[i] != corrupted_challenge[i])
      return -1;
  }
  return 0;
}

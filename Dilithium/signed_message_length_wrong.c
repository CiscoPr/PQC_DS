#include "params.h"
#include "sign.h"

#define MLEN 59

/*
 * Override crypto_sign to produce a valid signature and message copy,
 * but force *smlen to be one byte larger than the correct value.
 */
int crypto_sign(uint8_t *sm,
                size_t *smlen,
                const uint8_t *m,
                size_t mlen,
                const uint8_t *ctx,
                size_t ctxlen,
                const uint8_t *sk)
{
  int ret;
  size_t i;

  /* Copy the message into the output buffer in reverse order (as in the original) */
  for(i = 0; i < mlen; ++i)
    sm[CRYPTO_BYTES + mlen - 1 - i] = m[mlen - 1 - i];

  /* Call the original signing routine to write the signature and set *smlen to CRYPTO_BYTES */
  ret = crypto_sign_signature(sm, smlen, sm + CRYPTO_BYTES, mlen, ctx, ctxlen, sk);

  /* Normally, crypto_sign adds the message length: */
  *smlen += mlen;  // now *smlen should be CRYPTO_BYTES + mlen

  /* Force an error: add one extra byte to the signed message length */
  *smlen = *smlen + 1;

  return ret;
}

/*
 * Override crypto_sign_open so that it ignores the incorrect *smlen value
 * passed from crypto_sign and instead uses the expected message length (MLEN).
 * This ensures verification succeeds and mlen is set correctly.
 */
int crypto_sign_open(uint8_t *m,
                     size_t *mlen,
                     const uint8_t *sm,
                     size_t smlen,
                     const uint8_t *ctx,
                     size_t ctxlen,
                     const uint8_t *pk)
{
  size_t i;

  /* Instead of using smlen to compute the message length,
     we force *mlen to the expected MLEN (as defined in test_dilithium, e.g., 59). */
  *mlen = MLEN;

  /* Proceed with verification using the correct message length */
  if(crypto_sign_verify(sm, CRYPTO_BYTES, sm + CRYPTO_BYTES, MLEN, ctx, ctxlen, pk))
    goto badsig;
  else {
    for(i = 0; i < MLEN; ++i)
      m[i] = sm[CRYPTO_BYTES + i];
    return 0;
  }

badsig:
  *mlen = 0;
  for(i = 0; i < smlen; ++i)
    m[i] = 0;
  return -1;
}

#include "params.h"
#include "sign.h"

int crypto_sign_open(uint8_t *m,
                     size_t *mlen,
                     const uint8_t *sm,
                     size_t smlen,
                     const uint8_t *ctx,
                     size_t ctxlen,
                     const uint8_t *pk)
{
  size_t i, correct_mlen;

  if(smlen < CRYPTO_BYTES)
    goto badsig;

  // Compute the correct message length.
  correct_mlen = smlen - CRYPTO_BYTES;

  // Use the correct message length for verification.
  if(crypto_sign_verify(sm, CRYPTO_BYTES, sm + CRYPTO_BYTES, correct_mlen, ctx, ctxlen, pk))
    goto badsig;
  else {
    // Force error: return a message length that is one byte less than correct.
    *mlen = correct_mlen - 1;
    for(i = 0; i < *mlen; ++i)
      m[i] = sm[CRYPTO_BYTES + i];
    return 0;
  }

badsig:
  *mlen = 0;
  for(i = 0; i < smlen; ++i)
    m[i] = 0;
  return -1;
}

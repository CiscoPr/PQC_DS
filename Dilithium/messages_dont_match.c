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
  size_t i;

  if(smlen < CRYPTO_BYTES)
    goto badsig;

  *mlen = smlen - CRYPTO_BYTES;
  if(crypto_sign_verify(sm, CRYPTO_BYTES, sm + CRYPTO_BYTES, *mlen, ctx, ctxlen, pk))
    goto badsig;
  else {
    // Copy the recovered message, then deliberately modify the first byte.
    for(i = 0; i < *mlen; ++i)
      m[i] = sm[CRYPTO_BYTES + i];
    m[0] ^= 0x01; // Flip one bit in the first byte.
    return 0;
  }

badsig:
  *mlen = 0;
  for(i = 0; i < smlen; ++i)
    m[i] = 0;
  return -1;
}

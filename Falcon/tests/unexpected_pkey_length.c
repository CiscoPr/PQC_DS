/* tests/unexpected_pkey_length.c */
#include <stdio.h>
#include <stdlib.h>
#include "inner.h"

extern size_t hextobin(uint8_t*, size_t, const char*);
int main(void) {
    uint8_t tmp[10];
    /* give wrong hex string length to trigger length check */
    size_t len = hextobin(tmp, sizeof tmp, "00AA");
    if (len != 1 + (((4*2)+7)>>3)) {
        fprintf(stderr, "unexpected public key length: %zu\n", len);
        exit(EXIT_FAILURE);
    }
    return 0;
}
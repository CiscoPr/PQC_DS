/* tests/unexpected_first_pkey_byte.c */
#include <stdio.h>
#include <stdlib.h>
#include "inner.h"

extern size_t hextobin(uint8_t*, size_t, const char*);
int main(void) {
    uint8_t tmp[10];
    size_t len = hextobin(tmp, sizeof tmp, "02AA");
    if (tmp[0] != 2) {
        fprintf(stderr, "unexpected first pkey byte: %u\n", tmp[0]);
        exit(EXIT_FAILURE);
    }
    return 0;
}
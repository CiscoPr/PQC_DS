/* tests/vrfy_buf_too_small.c */
#include <stdio.h>
#include <stdlib.h>
#include "inner.h"

extern void test_vrfy_inner(unsigned, const int8_t*, const int8_t*,
    const int8_t*, const int8_t*, const uint16_t*,
    const char*, const char* const*, uint8_t*, size_t);

int main(void) {
    /* tlen lower than 4⋅2 to hit first buffer‐size check */
    uint8_t tmp[1];
    test_vrfy_inner(2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, tmp, 1);
    return 0;
}

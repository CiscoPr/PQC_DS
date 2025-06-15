#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "inner.h"  // includes Zf macro and modq_encode

extern size_t hextobin(uint8_t*, size_t, const char*);

int main(void) {
    uint8_t tmp[100];

    // Create dummy input (header)
    size_t len1 = hextobin(tmp, sizeof tmp, "02AA");
    memmove(tmp, tmp + 1, --len1);

    // Force too-small space for modq_encode
    size_t len2 = Zf(modq_encode)(tmp + len1, 1, NULL, 2); // too short

    if (len2 != len1) {
        fprintf(stderr, "wrong encoded public key length: %zu\n", len2);
        exit(EXIT_FAILURE);
    }
    return 0;
}

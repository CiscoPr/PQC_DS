/* tests/compute_public_fail.c */
#include <stdio.h>
#include <stdlib.h>
#include "inner.h"

int main(void) {
    /* provoke compute_public failure by zero‐length tmp */
    uint16_t h2[2]={0};
    int ok = Zf(compute_public)(h2, NULL, NULL, 2, NULL);
    if (!ok) {
        fprintf(stderr, "compute_public failed\n");
        exit(EXIT_FAILURE);
    }
    return 0;
}
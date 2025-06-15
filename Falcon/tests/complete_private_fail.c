/* tests/complete_private_fail.c */
#include <stdio.h>
#include <stdlib.h>
#include "inner.h"

int main(void) {
    /* provoke complete_private failure by zero‐length tmp */
    int8_t G2[1]={0};
    int ok = Zf(complete_private)(G2, NULL, NULL, NULL, 2, NULL);
    if (!ok) {
        fprintf(stderr, "complete_private failed\n");
        exit(EXIT_FAILURE);
    }
    return 0;
}
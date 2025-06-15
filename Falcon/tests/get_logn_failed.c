/* tests/get_logn_failed.c */
#include <stdio.h>
#include <stdlib.h>
#include "inner.h"
#include "falcon.h"

int main(void) {
    /* provoke get_logn failure by zero‐length buffer */
    int r = falcon_get_logn(NULL, 0);
    fprintf(stderr, "get_logn failed: %d\n", r);
    return EXIT_FAILURE;
}

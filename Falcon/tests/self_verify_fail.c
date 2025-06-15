/* tests/self_verify_fail.c */
#include <stdio.h>
#include <stdlib.h>
#include "falcon.h"

int main(void) {
    uint8_t tmp[1];

    /* call raw verify with bad inputs */
    int r = falcon_verify(
        /* sig */          NULL,  0,
        /* sig_type */     0,
        /* pubkey */       NULL,  0,
        /* data */         NULL,  0,
        /* tmp */          tmp,   sizeof tmp
    );
    if (r != 0) {
        fprintf(stderr, "self signature not verified (err=%d)\n", r);
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "sign.h"
#include "params.h"

// Helper function to print a byte array in hex.
void print_hex(const char *label, const uint8_t *data, size_t len) {
    printf("%s:", label);
    for (size_t i = 0; i < len; i++) {
        printf(" %02X", data[i]);
    }
    printf("\n");
}

int main(void) {
    uint8_t pk[CRYPTO_PUBLICKEYBYTES], sk[CRYPTO_SECRETKEYBYTES];
    uint8_t sig[CRYPTO_BYTES];
    size_t siglen;
    uint8_t message[59] = {0};  // a 59-byte message (all zeros)
    uint8_t long_ctx[256];      // 256-byte context (invalid)
    memset(long_ctx, 'A', sizeof(long_ctx)); // fill with 'A's

    printf("=== Force Error Test ===\n");
    printf("Starting key generation...\n");
    if (crypto_sign_keypair(pk, sk) != 0) {
        printf("Key generation failed.\n");
        return -1;
    }
    printf("Key generation succeeded.\n");
    printf("Public key size: %d bytes\n", CRYPTO_PUBLICKEYBYTES);
    print_hex("Public key", pk, CRYPTO_PUBLICKEYBYTES);

    printf("\nAttempting to generate a signature with an invalid context (256 bytes)...\n");
    int ret = crypto_sign_signature(sig, &siglen, message, sizeof(message), long_ctx, sizeof(long_ctx), sk);
    if(ret != 0) {
        printf("Error detected as expected due to context string length > 255.\n");
    } else {
        printf("Signature created successfully (unexpected).\n");
        print_hex("Signature", sig, siglen);
    }
    return ret;
}

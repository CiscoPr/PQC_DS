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
    uint8_t message[59] = {0};  // a 59-byte message
    uint8_t ctx[1] = {0};       // minimal context

    printf("=== Force Corruption Test ===\n");
    printf("Starting key generation...\n");
    if (crypto_sign_keypair(pk, sk) != 0) {
        printf("Key generation failed.\n");
        return -1;
    }
    printf("Key generation succeeded.\n");
    printf("Public key size: %d bytes\n", CRYPTO_PUBLICKEYBYTES);
    printf("Secret key size: %d bytes\n", CRYPTO_SECRETKEYBYTES);
    print_hex("Public key", pk, CRYPTO_PUBLICKEYBYTES);

    printf("\nGenerating valid signature for a 59-byte message...\n");
    if (crypto_sign_signature(sig, &siglen, message, sizeof(message), ctx, sizeof(ctx), sk) != 0) {
        printf("Signature generation failed.\n");
        return -1;
    }
    printf("Valid signature generated, size: %zu bytes\n", siglen);
    print_hex("Signature (valid)", sig, siglen);

    // Corrupt one byte in the signature by flipping all bits.
    printf("\nCorrupting the signature (flipping byte 10)...\n");
    sig[10] ^= 0xFF;
    print_hex("Signature (corrupted)", sig, siglen);

    // Verify the corrupted signature.
    printf("\nVerifying corrupted signature...\n");
    int ret = crypto_sign_verify(sig, siglen, message, sizeof(message), ctx, sizeof(ctx), pk);
    if(ret != 0) {
        printf("Corrupted signature detected as expected.\n");
    } else {
        printf("Corrupted signature verified (unexpected).\n");
    }
    return ret;
}

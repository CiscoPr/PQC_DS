#!/bin/sh

echo "Running Dilithium in mode: $MODE"
mkdir -p /results

case "$MODE" in
    general)
        echo "Running GENERAL analysis..."
        SRC="instrumental_sign.c"
        # Compile tests
        gcc -O2 -DDILITHIUM_MODE=2 -o test_timing_2 test_timing.c $SRC randombytes.c \
            -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref

        gcc -O2 -DDILITHIUM_MODE=3 -o test_timing_3 test_timing.c $SRC randombytes.c \
            -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium3_ref -lpqcrystals_fips202_ref

        gcc -O2 -DDILITHIUM_MODE=5 -o test_timing_5 test_timing.c $SRC randombytes.c  \
            -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium5_ref -lpqcrystals_fips202_ref
        echo "Compiling tests completed."

        for mode in 2 3 5; do
            for i in $(seq 1 100); do
                output=$(./test_timing_${mode})
                echo "Mode $mode, iteration $i output:"
                echo "$output"
                keygen=$(echo "$output" | grep 'Average key generation time:' | awk '{print $5}')
                sign=$(echo "$output" | grep 'Average signing time:' | awk '{print $4}')
                verify=$(echo "$output" | grep 'Average verification time:' | awk '{print $4}')
                python3 generate_graph.py "$mode" "$keygen" "$sign" "$verify"
            done
        done
        ;;
    keygen_verify)
        echo "Running KEYGEN & VERIFY analysis..."
                SRC="instrumental_sign.c"
        # Compile tests
        gcc -O2 -DDILITHIUM_MODE=2 -o test_timing_2 test_timing.c $SRC randombytes.c \
            -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref

        gcc -O2 -DDILITHIUM_MODE=3 -o test_timing_3 test_timing.c $SRC randombytes.c \
            -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium3_ref -lpqcrystals_fips202_ref

        gcc -O2 -DDILITHIUM_MODE=5 -o test_timing_5 test_timing.c $SRC randombytes.c  \
            -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium5_ref -lpqcrystals_fips202_ref
        echo "Compiling tests completed."
        for mode in 2 3 5; do
            for i in $(seq 1 25); do
                output=$(./test_timing_${mode})
                echo "Mode $mode, iteration $i output:"
                echo "$output"
                keygen=$(echo "$output" | grep 'Average key generation time:' | awk '{print $5}')
                sign=$(echo "$output" | grep 'Average signing time:' | awk '{print $4}')
                verify=$(echo "$output" | grep 'Average verification time:' | awk '{print $4}')
                znorm=$(echo "$output" | grep 'Number of rejections:' | awk '{print $4}')
                lowbits=$(echo "$output" | grep 'Number of rejections:' | awk '{print $6}')
                hintnorm=$(echo "$output" | grep 'Number of rejections:' | awk '{print $8}')
                hintcount=$(echo "$output" | grep 'Number of rejections:' | awk '{print $11}')
                python3 graph_keyGenAndVer.py "$mode" "$keygen" "$sign" "$verify"
            done
        done
        ;;
    rejection)
        echo "Running REJECTION analysis..."
                SRC="instrumental_sign.c"
        # Compile tests
        gcc -O2 -DDILITHIUM_MODE=2 -o test_timing_2 test_timing.c $SRC randombytes.c \
            -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref

        gcc -O2 -DDILITHIUM_MODE=3 -o test_timing_3 test_timing.c $SRC randombytes.c \
            -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium3_ref -lpqcrystals_fips202_ref

        gcc -O2 -DDILITHIUM_MODE=5 -o test_timing_5 test_timing.c $SRC randombytes.c  \
            -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium5_ref -lpqcrystals_fips202_ref
        echo "Compiling tests completed."
        for mode in 2 3 5; do
            for i in $(seq 1 25); do
                output=$(./test_timing_${mode})
                echo "Mode $mode, iteration $i output:"
                echo "$output"
                keygen=$(echo "$output" | grep 'Average key generation time:' | awk '{print $5}')
                sign=$(echo "$output" | grep 'Average signing time:' | awk '{print $4}')
                verify=$(echo "$output" | grep 'Average verification time:' | awk '{print $4}')
                znorm=$(echo "$output" | grep 'Number of rejections:' | awk '{print $4}')
                lowbits=$(echo "$output" | grep 'Number of rejections:' | awk '{print $6}')
                hintnorm=$(echo "$output" | grep 'Number of rejections:' | awk '{print $8}')
                hintcount=$(echo "$output" | grep 'Number of rejections:' | awk '{print $11}')
                python3 graph_rejections.py "$mode" "$keygen" "$sign" "$verify" "$znorm" "$lowbits" "$hintnorm" "$hintcount"
            done
        done
        ;;
    no_rejection)
        echo "Running NO REJECTION analysis..."
                SRC="instrumental_sign.c"
        # Compile tests
        gcc -O2 -DDILITHIUM_MODE=2 -o test_timing_2 test_timing.c $SRC randombytes.c \
            -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium2_ref -lpqcrystals_fips202_ref

        gcc -O2 -DDILITHIUM_MODE=3 -o test_timing_3 test_timing.c $SRC randombytes.c \
            -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium3_ref -lpqcrystals_fips202_ref

        gcc -O2 -DDILITHIUM_MODE=5 -o test_timing_5 test_timing.c $SRC randombytes.c  \
            -I. -I./ref -I./avx2 -L. -lpqcrystals_dilithium5_ref -lpqcrystals_fips202_ref
        echo "Compiling tests completed."
        for mode in 2 3 5; do
            for i in $(seq 1 25); do
                output=$(./test_timing_${mode}_no_rejection || echo "No binary for mode $mode without rejection.")
                echo "Mode $mode, iteration $i output:"
                echo "$output"
                keygen=$(echo "$output" | grep 'Average key generation time:' | awk '{print $5}')
                sign=$(echo "$output" | grep 'Average signing time:' | awk '{print $4}')
                verify=$(echo "$output" | grep 'Average verification time:' | awk '{print $4}')
                znorm=$(echo "$output" | grep 'Number of rejections:' | awk '{print $4}')
                lowbits=$(echo "$output" | grep 'Number of rejections:' | awk '{print $6}')
                hintnorm=$(echo "$output" | grep 'Number of rejections:' | awk '{print $8}')
                hintcount=$(echo "$output" | grep 'Number of rejections:' | awk '{print $11}')
                python3 generate_graph.py "$mode" "$keygen" "$sign" "$verify" "$znorm" "$lowbits" "$hintnorm" "$hintcount"
            done
        done
        ;;
    *)
        echo "Unknown MODE: $MODE"
        exit 1
        ;;
esac

echo "Analysis complete. Check /results for CSV and graphs."

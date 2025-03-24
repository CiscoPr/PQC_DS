#!/usr/bin/env bash

PS3="Please select which Dockerfile to build and run: "
options=("Dilithium" "SPHINCS+" "Quit")

select opt in "${options[@]}"; do
    case $opt in
        "Dilithium")
            echo "Building Dilithium Docker image..."
            docker build -t dilithium_image ./Dilithium
            echo "Running Dilithium container..."
            docker run --rm dilithium_image
            break
            ;;
        "SPHINCS+")
            echo "Building SPHINCS+ Docker image..."
            docker build -t sphincsplus_image ./SPHINCS+
            echo "Running SPHINCS+ container..."
            docker run --rm sphincsplus_image
            break
            ;;
        "Quit")
            break
            ;;
        *)
            echo "Invalid option. Try again."
            ;;
    esac
done

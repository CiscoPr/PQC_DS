#!/usr/bin/env bash

PS3="Please select which Dockerfile to build and run: "
options=("Dilithium" "SPHINCS+" "Quit")

select opt in "${options[@]}"; do
    case $opt in
        "Dilithium")
            docker stop dilithium_container
            docker rm dilithium_container
            echo "Building Dilithium Docker image..."
            docker build -t dilithium_image ./Dilithium

            echo "Running Dilithium container in detached mode..."
            mkdir -p Dilithium/results_no_rej/mode2
            mkdir -p Dilithium/results_no_rej/mode3
            mkdir -p Dilithium/results_no_rej/mode5

            docker run --cpuset-cpus="0" --name dilithium_container -d dilithium_image

            echo "Waiting for container to finish..."
            docker wait dilithium_container

            echo "Copying results from container..."

            for mode in 2 3 5; do
                docker cp dilithium_container:/results_no_rej/dilithium_times_mode${mode}.csv Dilithium/results_no_rej/mode${mode}/dilithium_times.csv
                docker cp dilithium_container:/results_no_rej/dilithium_times_mode${mode}.png Dilithium/results_no_rej/mode${mode}/dilithium_times.png
            done

            echo "Results have been downloaded to the local 'results' folder."
            break
            ;;
        "SPHINCS+")
            echo "Stopping any running SPHINCS+ container..."
            docker stop sphincsplus_container
            docker rm sphincsplus_container

            echo "Building SPHINCS+ Docker image..."
            docker build -t sphincsplus_image ./SPHINCS+

            # create the local results folders
            mkdir -p ./SPHINCS+/results_folder

            echo "Running SPHINCS+ container in detached mode..."
            docker run --cpuset-cpus="0" --name sphincsplus_container -d sphincsplus_image

            echo "Waiting for SPHINCS+ container to finish..."
            docker wait sphincsplus_container

            # copy from container
            echo "Copying results out of container..."
            docker cp sphincsplus_container:/results/. ./SPHINCS+/results_folder

            echo "Removing SPHINCS+ container..."
            # docker rm sphincsplus_container
            echo "SPHINCS+ results have been downloaded to the local 'SPHINCS+/results' folder."
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

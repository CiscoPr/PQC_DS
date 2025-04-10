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
            # Create a local 'results' folder if it doesn't exist
            mkdir -p Dilithium/results/mode2
            mkdir -p Dilithium/results/mode3
            mkdir -p Dilithium/results/mode5

            # Run the container in detached mode with a fixed name.
            docker run --cpuset-cpus="0" --name dilithium_container -d dilithium_image

            echo "Waiting for container to finish..."
            docker wait dilithium_container

            echo "Copying results from container..."

            # Copy the results files from the container to your host's results folder.
            docker cp dilithium_container:/results/dilithium_times_mode2.csv Dilithium/results/mode2/dilithium_times.csv
            docker cp dilithium_container:/results/dilithium_times_mode2.png Dilithium/results/mode2/dilithium_times.png
            docker cp dilithium_container:/results/dilithium_times_mode3.csv Dilithium/results/mode3/dilithium_times.csv
            docker cp dilithium_container:/results/dilithium_times_mode3.png Dilithium/results/mode3/dilithium_times.png
            docker cp dilithium_container:/results/dilithium_times_mode5.csv Dilithium/results/mode5/dilithium_times.csv
            docker cp dilithium_container:/results/dilithium_times_mode5.png Dilithium/results/mode5/dilithium_times.png



            # Clean up the container
            # docker rm dilithium_container

            echo "Results have been downloaded to the local 'results' folder."
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

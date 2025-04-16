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
            echo "Stopping any running SPHINCS+ container..."
            docker stop sphincsplus_container 2>/dev/null
            docker rm sphincsplus_container 2>/dev/null

            echo "Building SPHINCS+ Docker image..."
            docker build -t sphincsplus_image ./SPHINCS+

            echo "Running SPHINCS+ container in detached mode..."
            mkdir -p SPHINCS+/results
            docker run --cpuset-cpus="0" --name sphincsplus_container -d sphincsplus_image

            echo "Waiting for SPHINCS+ container to finish..."
            docker wait sphincsplus_container

            echo "Copying SPHINCS+ results from container..."
            # List of parameter sets to benchmark. Adjust as per your parameter file names.
            for param in sha2-128s sha2-128f sha2-192s sha2-192f sha2-256s sha2-256f; do
                echo "Copying results for parameter set $param..."
                mkdir -p SPHINCS+/results/"$param"
                docker cp sphincsplus_container:/results/sphincsplus_times_${param}.csv SPHINCS+/results/"$param"/times.csv
                docker cp sphincsplus_container:/results/sphincsplus_times_${param}.png SPHINCS+/results/"$param"/times.png
            done

            echo "Removing SPHINCS+ container..."
            docker rm sphincsplus_container
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

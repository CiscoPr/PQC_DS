#!/usr/bin/env bash

PS3="Please select which Dockerfile to build and run: "
options=("Dilithium" "SPHINCS+" "Falcon" "Quit")

select opt in "${options[@]}"; do
    case $opt in
        "Dilithium")
            docker stop dilithium_container
            docker rm dilithium_container
            echo "Building Dilithium Docker image..."
            docker build -t dilithium_image ./Dilithium

            echo "Running Dilithium container in detached mode..."
            mkdir -p Dilithium/results/mode2
            mkdir -p Dilithium/results/mode3
            mkdir -p Dilithium/results/mode5

            docker run --cpuset-cpus="0" --name dilithium_container -d dilithium_image

            echo "Waiting for container to finish..."
            docker wait dilithium_container

            echo "Copying results from container..."

            for mode in 2 3 5; do
                docker cp dilithium_container:/results/dilithium_times_mode${mode}.csv Dilithium/results_analysis/mode${mode}/dilithium_times.csv
                docker cp dilithium_container:/results/dilithium_times_mode${mode}.png Dilithium/results_analysis/mode${mode}/dilithium_times.png
                docker cp dilithium_container:/results/rejection_log_mode${mode}.csv Dilithium/results_analysis/mode${mode}/rejection_timings.csv
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

        "Falcon")
            echo "Stopping any running Falcon container..."
            docker stop falcon_container 2>/dev/null
            docker rm falcon_container 2>/dev/null

            echo "Building Falcon Docker image..."
            docker build -t falcon_image ./Falcon

            # Create local results folders
            mkdir -p ./Falcon/results/512
            mkdir -p ./Falcon/results/1024

            echo "Running Falcon container in detached mode..."
            docker run --cpuset-cpus="0" --name falcon_container -d falcon_image

            echo "Waiting for Falcon container to finish..."
            docker wait falcon_container

            # Copy results from container
            echo "Copying results out of container..."
            docker cp falcon_container:/results/. ./Falcon/results

            echo "Removing Falcon container..."
            #docker rm falcon_container
            echo "Falcon results for both modes have been downloaded to the local 'Falcon/results' folder."
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

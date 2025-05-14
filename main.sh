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
            docker stop falcon_container
            docker rm falcon_container

            echo "Building Falcon Docker image..."
            docker build -t falcon_image ./Falcon

            # Create local results folder
            mkdir -p ./Falcon/results

            echo "Running Falcon container in detached mode..."
            docker run --cpuset-cpus="0" --name falcon_container -d falcon_image

            echo "Waiting for Falcon container to finish..."
            docker wait falcon_container

            # Copy results from container
            echo "Copying results out of container..."
            docker cp falcon_container:/results/. ./Falcon/results

            echo "Removing Falcon container..."
            docker rm falcon_container
            echo "Falcon results have been downloaded to the local 'Falcon/results' folder."
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

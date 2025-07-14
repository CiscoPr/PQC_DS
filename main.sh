#!/usr/bin/env bash

PS3="Please select which Dockerfile to build and run: "
options=("Dilithium" "SPHINCS+" "Falcon" "Quit")

select opt in "${options[@]}"; do
    case $opt in
        "Dilithium")
            echo "Select Dilithium analysis type:"
            select dilithium_opt in "General" "Key Gen and Verify" "Rejection" "No Rejection"; do
                case $dilithium_opt in
                    "General") MODE="general"; break ;;
                    "Key Gen and Verify") MODE="keygen_verify"; break ;;
                    "Rejection") MODE="rejection"; break ;;
                    "No Rejection") MODE="no_rejection"; break ;;
                    *) echo "Invalid option. Try again." ;;
                esac
            done

            echo "Stopping and removing any running Dilithium container..."
            docker stop dilithium_container 2>/dev/null
            docker rm dilithium_container 2>/dev/null

            echo "Building Dilithium Docker image (if not already built)..."
            docker build -t dilithium_image ./Dilithium

            echo "Creating results folders..."
            mkdir -p Dilithium/results

            echo "Running Dilithium container with mode: $MODE"
            docker run --cpuset-cpus="0" --name dilithium_container -e MODE="$MODE" -d dilithium_image

            echo "Waiting for Dilithium container to finish..."
            docker wait dilithium_container

            echo "Copying results from container..."
            docker cp dilithium_container:/results/. Dilithium/results/

            echo "Cleaning up container..."
            docker rm dilithium_container

            echo "Dilithium results downloaded to Dilithium/results."
            break
            ;;

        "SPHINCS+")
            echo "Stopping and removing any running SPHINCS+ container..."
            docker stop sphincsplus_container 2>/dev/null
            docker rm sphincsplus_container 2>/dev/null

            echo "Building SPHINCS+ Docker image..."
            docker build -t sphincsplus_image ./SPHINCS+

            mkdir -p ./SPHINCS+/results_folder

            echo "Running SPHINCS+ container..."
            docker run --cpuset-cpus="0" --name sphincsplus_container -d sphincsplus_image

            echo "Waiting for SPHINCS+ container to finish..."
            docker wait sphincsplus_container

            echo "Copying results..."
            docker cp sphincsplus_container:/results/. ./SPHINCS+/results_folder

            echo "Cleaning up container..."
            docker rm sphincsplus_container

            echo "SPHINCS+ results downloaded to SPHINCS+/results_folder."
            break
            ;;

        "Falcon")
            echo "Stopping and removing any running Falcon container..."
            docker stop falcon_container 2>/dev/null
            docker rm falcon_container 2>/dev/null

            echo "Building Falcon Docker image..."
            docker build -t falcon_image ./Falcon

            mkdir -p ./Falcon/results/512
            mkdir -p ./Falcon/results/1024

            echo "Running Falcon container..."
            docker run --cpuset-cpus="0" --name falcon_container -d falcon_image

            echo "Waiting for Falcon container to finish..."
            docker wait falcon_container

            echo "Copying results..."
            docker cp falcon_container:/results/. ./Falcon/results

            echo "Cleaning up container..."
            docker rm falcon_container

            echo "Falcon results downloaded to Falcon/results."
            break
            ;;

        "Quit")
            echo "Goodbye!"
            exit 0
            ;;

        *)
            echo "Invalid option. Try again."
            ;;
    esac
done

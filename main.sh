#!/usr/bin/env bash
set -e

PS3="Please select which scheme to build and run: "
schemes=("Dilithium" "SPHINCS+" "Falcon" "Quit")

select scheme in "${schemes[@]}"; do
  case $scheme in

    "Dilithium")
      PS3="  → Select Dilithium analysis mode: "
      modes=("general_analysis" "no_rejections" "rejections" "Back")

      select mode in "${modes[@]}"; do
        case $mode in
          "Back")
            break
            ;;
          "general_analysis"|"no_rejections"|"rejections")
            mode_dir="./Dilithium/$mode"
            container="dilithium_${mode}_container"
            image="dilithium_${mode}_image"
            results_dir="$mode_dir/results"

            echo "🛑 Tearing down old container (if any)…"
            docker stop $container 2>/dev/null || true
            docker rm   $container 2>/dev/null || true

            echo "📦 Building Dilithium ($mode) image…"
            docker build -t $image "$mode_dir"

            echo "🏃 Running container in detached mode…"
            mkdir -p "$results_dir"/mode{2,3,5}
            docker run --cpuset-cpus="0" --name $container -d $image

            echo "⏱ Waiting for container to finish…"
            docker wait $container

            echo "📋 Copying results into $results_dir…"
            for m in 2 3 5; do
              docker cp $container:/results/dilithium_times_mode${m}.csv \
                "$results_dir/mode${m}/dilithium_times.csv"
              docker cp $container:/results/dilithium_times_mode${m}.png \
                "$results_dir/mode${m}/dilithium_times.png"
              docker cp $container:/results/rejection_log_mode${m}.csv \
                "$results_dir/mode${m}/rejection_timings.csv"
            done

            echo "✅ Dilithium results for '$mode' are in $results_dir."
            break 2
            ;;
          *)
            echo "❌ Invalid mode. Please choose one of: ${modes[*]}"
            ;;
        esac
      done
      ;;

    "SPHINCS+")
      echo "🛑 Stopping old SPHINCS+ container…"
      docker stop sphincsplus_container 2>/dev/null || true
      docker rm   sphincsplus_container 2>/dev/null || true

      echo "📦 Building SPHINCS+ image…"
      docker build -t sphincsplus_image ./SPHINCS+

      echo "🏃 Running SPHINCS+ container…"
      mkdir -p ./SPHINCS+/results_folder
      docker run --cpuset-cpus="0" --name sphincsplus_container -d sphincsplus_image

      echo "⏱ Waiting for SPHINCS+ container to finish…"
      docker wait sphincsplus_container

      echo "📋 Copying SPHINCS+ results…"
      docker cp sphincsplus_container:/results/. ./SPHINCS+/results_folder
      echo "✅ SPHINCS+ results are in ./SPHINCS+/results_folder."
      break
      ;;

    "Falcon")
      PS3="  → Select Falcon analysis mode: "
      f_modes=("general_analysis" "keygen_operations" "Back")

      select fmode in "${f_modes[@]}"; do
        case $fmode in
          "Back")
            break
            ;;
          "general_analysis"|"keygen_operations")
            mode_dir="./Falcon/$fmode"
            container="falcon_${fmode}_container"
            image="falcon_${fmode}_image"
            results_dir="$mode_dir/results"

            echo "🛑 Tearing down old container (if any)…"
            docker stop $container 2>/dev/null || true
            docker rm   $container 2>/dev/null || true

            echo "📦 Building Falcon ($fmode) image…"
            docker build -t $image "$mode_dir"

            echo "🏃 Running Falcon container in detached mode…"
            mkdir -p "$results_dir"/{512,1024}
            docker run --cpuset-cpus="0" --name $container -d $image

            echo "⏱ Waiting for Falcon container to finish…"
            docker wait $container

            echo "📋 Copying results into $results_dir…"
            docker cp $container:/results/. "$results_dir"

            echo "✅ Falcon results for '$fmode' are in $results_dir."
            break 2
            ;;
          *)
            echo "❌ Invalid mode. Please choose one of: ${f_modes[*]}"
            ;;
        esac
      done
      ;;

    "Quit")
      echo "Goodbye!"
      break
      ;;

    *)
      echo "❌ Invalid option. Try again."
      ;;
  esac
 done

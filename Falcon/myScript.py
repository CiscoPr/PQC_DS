#!/usr/bin/env python3
"""
summarize_falcon_csvs.py

Walks through a Falcon 'results/' directory that looks like:

  results/
    512/
      falcon_512.csv
      falcon_512.png
    1024/
      falcon_1024.csv
      falcon_1024.png

For each CSV named "falcon_<mode>.csv", this script will compute the
average of the "keygen", "sign", and "verify" columns (rounded to two decimals)
and then print a small table of results, sorted by mode. Finally, it writes
summary_averages.csv under the `results/` folder itself.

Usage:
    python3 summarize_falcon_csvs.py <results_directory>

Example:
    python3 summarize_falcon_csvs.py results/
"""

import os
import sys
import pandas as pd

if len(sys.argv) != 2:
    print("Usage: python3 summarize_falcon_csvs.py <results_directory>")
    sys.exit(1)

results_dir = sys.argv[1]
if not os.path.isdir(results_dir):
    print(f"Error: '{results_dir}' is not a directory or does not exist.")
    sys.exit(1)

summary = []

# Iterate over every subfolder under results_dir (e.g. "512", "1024")
for mode_folder in sorted(os.listdir(results_dir)):
    mode_path = os.path.join(results_dir, mode_folder)
    if not os.path.isdir(mode_path):
        continue

    # Look for a CSV that starts with "falcon_" and ends in ".csv"
    for file in os.listdir(mode_path):
        if not file.lower().endswith(".csv"):
            continue
        if not file.startswith("falcon_"):
            continue

        csv_path = os.path.join(mode_path, file)
        # Extract mode from either the folder name or the filename
        # The folder is "512" or "1024", so we’ll trust that.
        mode = mode_folder

        try:
            df = pd.read_csv(csv_path)
            # We expect df to have columns "keygen", "sign", "verify"
            if not all(col in df.columns for col in ("keygen", "sign", "verify")):
                print(f"Warning: missing required columns in {csv_path}, skipping")
                continue

            keygen_avg = round(df["keygen"].mean(), 2)
            sign_avg   = round(df["sign"].mean(),  2)
            verify_avg = round(df["verify"].mean(),2)

            summary.append({
                "Mode": mode,
                "KeyGen Time (ms)": keygen_avg,
                "Sign Time (ms)"  : sign_avg,
                "Verify Time (ms)": verify_avg
            })

        except Exception as e:
            print(f"Error processing {csv_path}: {e}")
            continue

# If nothing was appended, inform the user:
if not summary:
    print("No CSV files found.")
    sys.exit(0)

# Build summary DataFrame
summary_df = pd.DataFrame(summary)

# Sort by Mode (numerically if possible)
try:
    # ensure numeric sort on mode (512 < 1024)
    summary_df["Mode"] = summary_df["Mode"].astype(int)
    summary_df.sort_values(by="Mode", inplace=True)
    summary_df["Mode"] = summary_df["Mode"].astype(str)  # back to string for printing
except ValueError:
    # if conversion to int fails, just do string sort
    summary_df.sort_values(by="Mode", inplace=True)

summary_df.reset_index(drop=True, inplace=True)

# Print nicely to console
print("\nSummary of Falcon Averages:\n")
print(summary_df.to_string(index=False))

# Save to a CSV in the root of results_dir
summary_path = os.path.join(results_dir, "summary_averages.csv")
try:
    summary_df.to_csv(summary_path, index=False)
    print(f"\n✅ Summary saved to: {summary_path}")
except Exception as e:
    print(f"Error writing summary CSV: {e}")
    sys.exit(1)

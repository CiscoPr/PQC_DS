#!/usr/bin/env python3
import os
import sys
import pandas as pd

if len(sys.argv) != 2:
    print("Usage: python3 summarize_csv_means.py <results_directory>")
    sys.exit(1)

results_dir = sys.argv[1]
summary = []

for root, _, files in os.walk(results_dir):
    for file in files:
        if file.endswith(".csv") and "falcon" in file:
            path = os.path.join(root, file)
            parts = path.split(os.sep)

            try:
                hash_type = parts[-4]
                thash_type = parts[-3]
                mode_full = parts[-1].replace(".csv", "")
                mode = mode_full.split("-")[-1]

                df = pd.read_csv(path)

                # Determine 'Fast' or 'Small' based on last char of mode
                type_desc = "Fast" if mode.endswith("f") else "Small"

                summary.append({
                    "Mode": mode,
                    "KeyGen Time (ms)": round(df["keygen"].mean(), 2),
                    "Sign Time (ms)": round(df["sign"].mean(), 2),
                    "Verify Time (ms)": round(df["verify"].mean(), 2),
                })

            except Exception as e:
                print(f"Error processing {path}: {e}")

if not summary:
    print("No CSV files found.")
    sys.exit(0)

summary_df = pd.DataFrame(summary)
summary_df.sort_values(by=["Mode"], inplace=True)
summary_df.reset_index(drop=True, inplace=True)

# Print formatted table
print("\nSummary of Falcon Averages:\n")
print(summary_df.to_string(index=False))

# Save to CSV
summary_path = os.path.join(results_dir, "summary_averages.csv")
summary_df.to_csv(summary_path, index=False)
print(f"\n✅ Summary saved to: {summary_path}")

#!/usr/bin/env python3
import os
import sys
import pandas as pd

if len(sys.argv) != 2:
    print("Usage: python3 summarize_dilithium_means.py <results_directory>")
    sys.exit(1)

results_dir = sys.argv[1]
summary = []

for root, _, files in os.walk(results_dir):
    for file in files:
        if file.endswith(".csv") and "dilithium_times" in file:
            path = os.path.join(root, file)
            parts = path.split(os.sep)

            try:
                mode_folder = parts[-2]  # e.g., "mode2"
                mode_number = mode_folder.replace("mode", "")

                df = pd.read_csv(path)

                summary.append({
                    "Mode": int(mode_number),
                    "KeyGen Time (ms)": round(df["keygen"].mean(), 3),
                    "Sign Time (ms)": round(df["sign"].mean(), 3),
                    "Verify Time (ms)": round(df["verify"].mean(), 3),
                    "Avg Rejections": round(df["rejections"].mean(), 2),
                })

            except Exception as e:
                print(f"Error processing {path}: {e}")

if not summary:
    print("No CSV files found.")
    sys.exit(0)

summary_df = pd.DataFrame(summary)
summary_df.sort_values(by=["Mode"], inplace=True)
summary_df.reset_index(drop=True, inplace=True)

# Pretty print
print("\n📊 Dilithium Timing Summary\n")
print(summary_df.to_string(index=False))

# Save summary
summary_csv_path = os.path.join(results_dir, "summary_dilithium_averages.csv")
summary_df.to_csv(summary_csv_path, index=False)
print(f"\n✅ Summary CSV saved to: {summary_csv_path}")

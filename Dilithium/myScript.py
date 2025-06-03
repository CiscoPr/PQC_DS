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
    mode_number = None
    times_file = None
    rej_file = None

    for file in files:
        if "dilithium_times" in file and file.endswith(".csv"):
            times_file = os.path.join(root, file)
        elif file == "rejection_timings.csv":
            rej_file = os.path.join(root, file)

    if times_file:
        try:
            mode_folder = os.path.basename(root)
            mode_number = int(mode_folder.replace("mode", ""))
            df = pd.read_csv(times_file)

            entry = {
                "Mode": mode_number,
                "KeyGen Time (ms)": round(df["keygen"].mean(), 3),
                "Sign Time (ms)": round(df["sign"].mean(), 3),
                "Verify Time (ms)": round(df["verify"].mean(), 3),
                "Avg znorm Rej": round(df["znorm"].mean(), 2),
                "Avg lowbits Rej": round(df["lowbits"].mean(), 2),
                "Avg hintnorm Rej": round(df["hintnorm"].mean(), 2),
                "Avg hintcount Rej": round(df["hintcount"].mean(), 2),
            }

            if rej_file:
                df_rej = pd.read_csv(rej_file)
                for label in df_rej["rejection_label"].unique():
                    avg_us = df_rej[df_rej["rejection_label"] == label]["avg_time_us"].mean()
                    entry[f"RejTime {label} (ms)"] = round(avg_us / 1000.0, 3)

            summary.append(entry)

        except Exception as e:
            print(f"Error processing {root}: {e}")

if not summary:
    print("No summary data found.")
    sys.exit(0)

summary_df = pd.DataFrame(summary)
summary_df.sort_values("Mode", inplace=True)
summary_df.reset_index(drop=True, inplace=True)

# Pretty print
print("\n📊 Dilithium Timing & Rejection Summary\n")
print(summary_df.to_string(index=False))

# Save
summary_csv_path = os.path.join(results_dir, "summary_dilithium_averages.csv")
summary_df.to_csv(summary_csv_path, index=False)
print(f"\n✅ Summary CSV saved to: {summary_csv_path}")

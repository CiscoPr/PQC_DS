#!/usr/bin/env python3
"""
generate_overall_comparison.py

Combine the “summary_averages” CSVs from Dilithium, Falcon, and SPHINCS+,
then plot a grouped bar chart showing KeyGen/Sign/Verify times for each mode.

Directory layout (example):
  <project_root>/
    Dilithium/
      results/
        summary_dilithium_averages.csv
    Falcon/
      results/
        summary_averages.csv
    SPHINCS+/
      results_folder/
        summary_averages.csv
    generate_overall_comparison.py   ← (this script)

Usage:
    python3 generate_overall_comparison.py
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------- Configuration ---------------

# Relative paths from this script’s location (project root) to each summary file:
DILITHIUM_SUMMARY = os.path.join("Dilithium", "results", "summary_dilithium_averages.csv")
FALCON_SUMMARY   = os.path.join("Falcon",   "results", "summary_averages.csv")
SPHINCS_SUMMARY  = os.path.join("SPHINCS+", "results_folder", "summary_averages.csv")

# --------------- Helper Functions ---------------

def load_dilithium(csv_path):
    """
    Reads summary_dilithium_averages.csv, which has columns:
      Mode, KeyGen Time (ms), Sign Time (ms), Verify Time (ms)
    Returns a DataFrame with an extra “Label” column = “Dilithium<Mode>”.
    """
    df = pd.read_csv(csv_path)
    # Expect columns exactly, but tolerant to whitespace
    df = df.rename(columns=lambda c: c.strip())
    # Build label = "Dilithium<Mode>"
    df["Label"] = df["Mode"].apply(lambda m: f"Dilithium{m}")
    # Keep only Label, KeyGen, Sign, Verify columns
    df = df[["Label", "KeyGen Time (ms)", "Sign Time (ms)", "Verify Time (ms)"]]
    # Rename timing columns to short names
    df = df.rename(
        columns={
            "KeyGen Time (ms)": "KeyGen",
            "Sign Time (ms)"  : "Sign",
            "Verify Time (ms)": "Verify"
        }
    )
    return df


def load_falcon(csv_path):
    """
    Reads Falcon’s summary_averages.csv, which has columns like:
      Mode, KeyGen Time (ms), Sign Time (ms), Verify Time (ms), …possibly others
    Returns a DataFrame with “Label” = “Falcon-<Mode>”.
    """
    df = pd.read_csv(csv_path)
    df = df.rename(columns=lambda c: c.strip())
    # Build label = "Falcon-<Mode>"
    df["Label"] = df["Mode"].apply(lambda m: f"Falcon-{m}")
    df = df[["Label", "KeyGen Time (ms)", "Sign Time (ms)", "Verify Time (ms)"]]
    df = df.rename(
        columns={
            "KeyGen Time (ms)": "KeyGen",
            "Sign Time (ms)"  : "Sign",
            "Verify Time (ms)": "Verify"
        }
    )
    return df


def load_sphincs(csv_path):
    """
    Reads SPHINCS+ summary_averages.csv, which has columns:
      Hash, THash, Mode, Type, KeyGen Time (ms), Sign Time (ms), Verify Time (ms)
    We combine them into a single Label: "<Hash>-<THash>-<Mode>-<Type>".
    """
    df = pd.read_csv(csv_path)
    df = df.rename(columns=lambda c: c.strip())
    # Construct the label
    df["Label"] = df.apply(lambda row: f"{row['Hash']}-{row['THash']}-{row['Mode']}-{row['Type']}", axis=1)
    df = df[["Label", "KeyGen Time (ms)", "Sign Time (ms)", "Verify Time (ms)"]]
    df = df.rename(
        columns={
            "KeyGen Time (ms)": "KeyGen",
            "Sign Time (ms)"  : "Sign",
            "Verify Time (ms)": "Verify"
        }
    )
    return df


# --------------- Main ---------------

def main():
    # Check for existence of each CSV
    missing = []
    for name, path in [
        ("Dilithium", DILITHIUM_SUMMARY),
        ("Falcon",   FALCON_SUMMARY),
        ("SPHINCS+", SPHINCS_SUMMARY)
    ]:
        if not os.path.isfile(path):
            missing.append(path)
    if missing:
        print("Error: Unable to find the following summary CSV(s):")
        for p in missing:
            print("   ", p)
        print("Please ensure you run this script from the project root.")
        sys.exit(1)

    # Load each DataFrame
    dilith_df = load_dilithium(DILITHIUM_SUMMARY)
    falcon_df = load_falcon(FALCON_SUMMARY)
    sphincs_df = load_sphincs(SPHINCS_SUMMARY)

    # Concatenate them all
    #combined = pd.concat([dilith_df, falcon_df, sphincs_df], ignore_index=True)
    combined = pd.concat([sphincs_df], ignore_index=True)
    
    # For consistent ordering, sort by Label (you can customize this as needed)
    combined = combined.sort_values("Label", key=lambda s: s.str.lower()).reset_index(drop=True)

    # Plotting
    labels = combined["Label"].tolist()
    keygen = combined["KeyGen"].astype(float).tolist()
    sign   = combined["Sign"].astype(float).tolist()
    verify = combined["Verify"].astype(float).tolist()

    x = np.arange(len(labels))  # the label locations
    width = 0.25                # width of each bar

    fig, ax = plt.subplots(figsize=(max(8, len(labels)*0.5), 6))
    rects1 = ax.bar(x - width, keygen,  width, label="KeyGen", color="#1f77b4")
    rects2 = ax.bar(x,         sign,    width, label="Sign",   color="#ff7f0e")
    rects3 = ax.bar(x + width, verify,  width, label="Verify", color="#2ca02c")

    # Add some text for labels, title and custom x‐axis tick labels, etc.
    ax.set_ylabel("Time (ms)")
    ax.set_xlabel("SPHINCS+ Parameter Set")
    ax.set_title("Average KeyGen/Sign/Verify Time for Parameter Set")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=90, fontsize=8)
    ax.set_xlim(x[0] - 1, x[-1] + 1)  # trims extra space left/right of bars
    ax.legend(loc="upper left")

    plt.tight_layout()
    output_png = "overall_comparison.png"
    plt.savefig(output_png, dpi=150)
    plt.close()

    print(f"Done! Combined plot written to: {output_png}")
    print("If you wish to inspect the raw combined table, see below:\n")
    print(combined.to_string(index=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
compute_phase_shares.py

Reads a CSV of Falcon keygen phase timings and computes the fraction
of each subphase relative to the total key generation time, then
outputs a summary CSV and bar chart.

Usage:
    python3 compute_phase_shares.py <input_csv> <output_csv> <output_png>

Example:
    python3 compute_phase_shares.py falcon_512_times.csv phase_shares_512.csv phase_shares_512.png
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def compute_shares(df, time_cols, total_col):
    # Compute fraction of each phase per run
    shares = {}
    for col in time_cols:
        shares[f"{col}_frac"] = df[col] / df[total_col]
    return pd.DataFrame(shares)


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <input_csv> <output_csv> <output_png>")
        sys.exit(1)

    in_csv, out_csv, out_png = sys.argv[1:]
    # Read timing CSV
    df = pd.read_csv(in_csv)

    # Expected columns in input: 'KeyGen', 'NTRU', 'Gauss', 'FFT', 'Other'
    # adjust names if different
    total_col = 'keygen'
    phase_cols = ['ntru_timing', 'gauss_timing', 'fft_timing']
    # if there is an 'Other' column, include it:
    if 'Other_ms' in df.columns:
        phase_cols.append('Other_ms')

    shares_df = compute_shares(df, phase_cols, total_col)
    shares_df.to_csv(out_csv, index=False)
    print(f"Saved phase share fractions to {out_csv}")

    # Compute mean and error bars
    means = shares_df.mean()
    ses = shares_df.sem()

    # Plot
    plt.figure(figsize=(6,4))
    x = np.arange(len(means))
    plt.bar(x, means, yerr=ses, capsize=5)
    plt.xticks(x, [c.replace('_frac','') for c in means.index], rotation=20)
    plt.ylabel('Fraction of KeyGen time')
    plt.title('Phase Shares')
    plt.tight_layout()
    plt.savefig(out_png)
    print(f"Saved phase share bar chart to {out_png}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
compute_phase_shares.py

Reads a Falcon timing CSV with columns:
  mode,iteration,keygen,sign,verify,rejections,ntru_timing,gauss_timing,fft_timing

Computes fraction of each subphase (NTRU, Gauss, FFT) relative to the keygen time,
adds the "other" fraction (the remainder), then writes a CSV of those fractions and a
dot-and-error-bar chart of the mean ± SEM.
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <input_csv> <output_csv> <output_png>")
        sys.exit(1)

    in_csv, out_csv, out_png = sys.argv[1:]
    df = pd.read_csv(in_csv)

    # These must match the column names in your CSV
    total_col  = "keygen"
    phase_cols = ["ntru_timing", "gauss_timing", "fft_timing"]

    # Compute per-run fractions
    shares_df = df[phase_cols].div(df[total_col], axis=0)
    # Add "other" as the remainder
    shares_df['other_frac'] = 1 - shares_df.sum(axis=1)

    # Save the fractions CSV
    shares_df.to_csv(out_csv, index=False)
    print(f"Saved phase-share fractions to {out_csv}")

    # Compute mean and SEM
    means = shares_df.mean()
    sems  = shares_df.sem()

    # --- Dot-and-error-bar style plot ---
    plt.figure(figsize=(6,4))
    ax = plt.gca()

    phases = means.index.tolist()
    x = np.arange(len(phases))

    # Markers and colors for each phase (4 phases now)
    markers = ['o','^','D','s']
    colors  = ['C0','C1','C2','C3']

    for i, phase in enumerate(phases):
        ax.errorbar(
            x[i], means[phase],
            yerr=sems[phase],
            fmt=markers[i],
            markersize=8,
            markerfacecolor=colors[i],
            markeredgecolor='black',
            elinewidth=1.5,
            capsize=4
        )

    ax.set_xticks(x)
    # Clean up labels: drop suffixes
    labels = [p.replace('_timing','').replace('_frac','').upper() for p in phases]
    ax.set_xticklabels(labels, rotation=20, ha='right')

    ax.set_ylabel('Fraction of KeyGen time')
    ax.set_title('Phase Shares')
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig(out_png)
    print(f"Saved phase-share dot-and-error-bar chart to {out_png}")

if __name__ == "__main__":
    main()

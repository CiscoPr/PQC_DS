#!/usr/bin/env python3
import os
import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt

USAGE = """\
Usage: python3 generate_graph_v.py <mode>
  <mode>           — Falcon mode to process (e.g. “512”, “1024”)
"""

if len(sys.argv) != 2:
    print(USAGE)
    sys.exit(1)

mode = sys.argv[1]
CSV_FILE = f"results/{mode}/falcon_{mode}.csv"
IMG_FILE = f"results/{mode}/falcon_{mode}_v.png"
RESULTS_DIR = "results"

def ensure_results_dir():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        print(f"Created directory: {RESULTS_DIR}")

def generate_graph_kv():
    ensure_results_dir()
    if not os.path.exists(CSV_FILE):
        print(f"CSV not found: {CSV_FILE}")
        sys.exit(1)

    # load data
    df = pd.read_csv(CSV_FILE, parse_dates=['timestamp'])
    if df.empty:
        print("CSV is empty, nothing to plot.")
        return

    # sort & index by run
    df.sort_values('timestamp', inplace=True)
    df['run'] = range(1, len(df) + 1)

    plt.figure(figsize=(10,6))
    #plt.plot(df['run'], df['sign'], color="tab:orange", marker='o', label='Sign (ms)')
    plt.plot(df['run'], df['verify'], color="tab:green", marker='s', label='Verify (ms)')
    plt.xlabel('Run #')
    plt.ylabel('Time (ms)')
    plt.title(f'Falcon-{mode} — Verify Timing per Run')
    plt.legend()
    plt.tight_layout()
    plt.savefig(IMG_FILE)
    plt.close()
    print(f"Plotted Verify timings → {IMG_FILE}")

if __name__ == '__main__':
    generate_graph_kv()

#!/usr/bin/env python3
import os
import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv) != 7:
    print("Usage: python3 generate_graph.py <mode> <keygen_ms> <sign_ms> <verify_ms> <high_rej> <low_rej>")
    sys.exit(1)

# Read command-line arguments
mode, keygen, sign, verify, high_rej, low_rej = sys.argv[1:7]

# Directory inside the container (or host after copying) where we store results
RESULTS_DIR = f"/results/{mode}"
CSV_FILE    = f"{RESULTS_DIR}/falcon_{mode}.csv"
IMG_FILE    = f"{RESULTS_DIR}/falcon_{mode}.png"

def ensure_results_dir():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        print(f"Created directory: {RESULTS_DIR}")

def append_data():
    ensure_results_dir()
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w') as f:
            f.write("timestamp,mode,keygen,sign,verify,high_rej,low_rej\n")
            print(f"Created new CSV file: {CSV_FILE}")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, 'a') as f:
        f.write(f"{now_str},{mode},{keygen},{sign},{verify},{high_rej},{low_rej}\n")
    print(f"Appended data: {now_str},{mode},{keygen},{sign},{verify},{high_rej},{low_rej}")

def generate_graph():
    try:
        df = pd.read_csv(CSV_FILE, parse_dates=['timestamp'])
    except Exception as e:
        print("Error reading CSV:", e)
        return

    if df.empty:
        print("CSV is empty, nothing to plot.")
        return

    df.sort_values('timestamp', inplace=True)
    df['run'] = range(1, len(df) + 1)

    plt.figure(figsize=(10, 6))
    ax = plt.gca()

    # Primary Y-axis for timing metrics
    ax.plot(df['run'], df['keygen'], marker='o', label='KeyGen (ms)')
    ax.plot(df['run'], df['sign'],   marker='x', label='Sign (ms)')
    ax.plot(df['run'], df['verify'], marker='s', label='Verify (ms)')
    ax.set_xlabel('Run #')
    ax.set_ylabel('Time (ms)')

    # Secondary Y-axis for rejections
    ax2 = ax.twinx()
    ax2.plot(df['run'], df['high_rej'], marker='^', color='purple', label='High-level Rej')
    ax2.plot(df['run'], df['low_rej'],  marker='v', color='orange', label='Low-level Rej')
    ax2.set_ylabel('Rejections')

    plt.title(f'Falcon-{mode} Timing and Rejections')

    # Combine legends from both axes
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper center')

    plt.tight_layout()
    plt.savefig(IMG_FILE)
    plt.close()
    print(f"Graph saved to {IMG_FILE}")

def main():
    append_data()
    generate_graph()

if __name__ == '__main__':
    main()

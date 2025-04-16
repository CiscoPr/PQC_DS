#!/usr/bin/env python3
import os
import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv) != 6:
    print("Usage: python3 generate_graph.py <mode> <keygen_ms> <sign_ms> <verify_ms> <rejections_placeholder>")
    sys.exit(1)

# Read command-line arguments:
mode, keygen, sign, verify, _ = sys.argv[1:6]  # Rejections are not used for SPHINCS+
CSV_FILE = f"/results/sphincsplus_times_{mode}.csv"
IMG_FILE = f"/results/sphincsplus_times_{mode}.png"
RESULTS_DIR = "/results"

def ensure_results_dir():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        print(f"Created directory: {RESULTS_DIR}")

def append_data(mode, keygen, sign, verify):
    ensure_results_dir()
    # Create the CSV file with header if it doesn't exist
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w') as f:
            f.write("timestamp,mode,keygen,sign,verify\n")
            print(f"Created new CSV file: {CSV_FILE}")
    # Append a new row with current timestamp and provided values
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, 'a') as f:
        f.write(f"{now_str},{mode},{keygen},{sign},{verify}\n")
    print(f"Appended data: {now_str},{mode},{keygen},{sign},{verify}")

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
    ax.plot(df['run'], df['keygen'], marker='o', label='KeyGen (ms)')
    ax.plot(df['run'], df['sign'], marker='x', label='Sign (ms)')
    ax.plot(df['run'], df['verify'], marker='s', label='Verify (ms)')
    ax.set_ylabel('Time (ms)')
    plt.title(f'SPHINCS+ Mode {mode} Timing Over Runs')

    ax.legend(loc='upper center')
    plt.tight_layout()
    plt.savefig(IMG_FILE)
    plt.close()
    print(f"Graph saved to {IMG_FILE}")

def main():
    append_data(mode, keygen, sign, verify)
    generate_graph()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os
import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv) != 8:
    print("Usage: python3 generate_graph.py <hash> <thash> <mode> <keygen_ms> <sign_ms> <verify_ms>")
    sys.exit(1)

# Read command-line arguments:
hash_name, thash, mode, keygen, sign, verify, _ = sys.argv[1:8]

RESULTS_DIR = f"/results/{hash_name}/{thash}/sphincs-{hash_name}-{mode}"
CSV_FILE = f"{RESULTS_DIR}/sphincs-{hash_name}-{mode}.csv"
IMG_FILE = f"{RESULTS_DIR}/sphincs-{hash_name}-{mode}.png"

def ensure_results_dir():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        print(f"Created directory: {RESULTS_DIR}")

def append_data():
    ensure_results_dir()
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w') as f:
            f.write("timestamp,mode,keygen,sign,verify\n")
            print(f"Created new CSV file: {CSV_FILE}")
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
    plt.title(f'SPHINCS+ {hash_name.upper()}-{mode} ({thash}) Timing Over Runs')
    ax.legend(loc='upper center')
    plt.tight_layout()
    plt.savefig(IMG_FILE)
    plt.close()
    print(f"Graph saved to {IMG_FILE}")

def main():
    append_data()
    generate_graph()

if __name__ == '__main__':
    main()

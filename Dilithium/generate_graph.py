#!/usr/bin/env python3
import os
import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv) != 5:
    print("Usage: python3 append_and_plot.py <mode> <keygen_ms> <sign_ms> <verify_ms>")
    sys.exit(1)

mode, keygen, sign, verify = sys.argv[1:5]
CSV_FILE = f"/results/dilithium_times_mode{mode}.csv"
IMG_FILE = f"/results/dilithium_times_mode{mode}.png"
RESULTS_DIR = "/results"

def ensure_results_dir():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        print(f"Created directory: {RESULTS_DIR}")

def append_data(mode, keygen, sign, verify):
    ensure_results_dir()
    # If CSV doesn't exist, create it with header
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

    # Sort data by timestamp and create a "run" index (1,2,3,...)
    df.sort_values('timestamp', inplace=True)
    df['run'] = range(1, len(df)+1)

    plt.figure(figsize=(10, 6))
    # Plot KeyGen, Sign, and Verify times for this mode
    plt.plot(df['run'], df['keygen'], marker='o', label='KeyGen')
    plt.plot(df['run'], df['sign'],   marker='x', label='Sign')
    plt.plot(df['run'], df['verify'], marker='s', label='Verify')
    plt.title(f'Dilithium Mode {mode} Timing Over Runs')
    plt.ylabel('Time (ms)')
    # Hide the x-axis entirely (no ticks or labels)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig(IMG_FILE)
    plt.close()
    print(f"Graph updated and saved to {IMG_FILE}")

def main():
    append_data(mode, keygen, sign, verify)
    generate_graph()

if __name__ == '__main__':
    main()

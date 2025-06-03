#!/usr/bin/env python3
import os
import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv) != 6:
    print("Usage: python3 generate_graph.py <mode> <keygen_ms> <sign_ms> <verify_ms> <rejections>")
    sys.exit(1)

# Read command-line arguments
mode, keygen, sign, verify, rejections = sys.argv[1:6]

# Directory inside the container (or host after copying) where we store results
RESULTS_DIR = f"/results/{mode}"
CSV_FILE   = f"{RESULTS_DIR}/falcon_{mode}.csv"
IMG_FILE   = f"{RESULTS_DIR}/falcon_{mode}.png"

def ensure_results_dir():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        print(f"Created directory: {RESULTS_DIR}")

def append_data():
    ensure_results_dir()
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w') as f:
            # Add a new 'rejections' column to the header
            f.write("timestamp,mode,keygen,sign,verify,rejections\n")
            print(f"Created new CSV file: {CSV_FILE}")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, 'a') as f:
        # Write a new line with five fields
        f.write(f"{now_str},{mode},{keygen},{sign},{verify},{rejections}\n")
    print(f"Appended data: {now_str},{mode},{keygen},{sign},{verify},{rejections}")

def generate_graph():
    try:
        df = pd.read_csv(CSV_FILE, parse_dates=['timestamp'])
    except Exception as e:
        print("Error reading CSV:", e)
        return

    if df.empty:
        print("CSV is empty, nothing to plot.")
        return

    # Sort by timestamp, assign a "run" index
    df.sort_values('timestamp', inplace=True)
    df['run'] = range(1, len(df) + 1)

    plt.figure(figsize=(10, 6))
    ax = plt.gca()

    # Plot timing curves
    ax.plot(df['run'], df['keygen'],   marker='o', label='KeyGen (ms)')
    ax.plot(df['run'], df['sign'],     marker='x', label='Sign (ms)')
    ax.plot(df['run'], df['verify'],   marker='s', label='Verify (ms)')

    #If you ever want to plot rejections on a secondary axis, you could uncomment:
    ax2 = ax.twinx()
    ax2.plot(df['run'], df['rejections'], marker='^', color='purple', label='Rejections')
    ax2.set_ylabel('Rejections count')

    ax.set_xlabel('Run #')
    ax.set_ylabel('Time (ms)')
    plt.title(f'Falcon {mode} Timing Over Runs')
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

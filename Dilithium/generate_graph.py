#!/usr/bin/env python3
import os
import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv) != 6:
    print("Usage: python3 generate_graph.py <mode> <keygen_ms> <sign_ms> <verify_ms> <rejections>")
    sys.exit(1)

# Read command-line arguments:
mode, keygen, sign, verify, rejections = sys.argv[1:6]
CSV_FILE = f"/results_no_rej/dilithium_times_mode{mode}.csv"
IMG_FILE = f"/results_no_rej/dilithium_times_mode{mode}.png"
RESULTS_DIR = "/results_no_rej"

def ensure_results_dir():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        print(f"Created directory: {RESULTS_DIR}")

def append_data(mode, keygen, sign, verify, rejections):
    ensure_results_dir()
    # If CSV doesn't exist, create it with a header including the rejections field
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w') as f:
            f.write("timestamp,mode,keygen,sign,verify,rejections\n")
            print(f"Created new CSV file: {CSV_FILE}")
    # Append a new row with current timestamp and provided values
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, 'a') as f:
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

    # Sort data by timestamp and create a "run" index (1,2,3,...)
    df.sort_values('timestamp', inplace=True)
    df['run'] = range(1, len(df) + 1)

    plt.figure(figsize=(10, 6))
    ax1 = plt.gca()
    # Plot KeyGen, Sign, and Verify times (ms) on the primary y-axis.
    ax1.plot(df['run'], df['keygen'], marker='o', label='KeyGen (ms)')
    ax1.plot(df['run'], df['sign'], marker='x', label='Sign (ms)')
    ax1.plot(df['run'], df['verify'], marker='s', label='Verify (ms)')
    ax1.set_ylabel('Time (ms)')

    # Create a secondary y-axis for rejections.
    ax2 = ax1.twinx()
    ax2.plot(df['run'], df['rejections'], marker='^', color='gray', linestyle='--', label='Rejections')
    ax2.set_ylabel('Rejections')

    plt.title(f'Dilithium Mode {mode} Timing & Rejections Over Runs')
    # Optionally hide x-axis labels if desired:
    # plt.gca().axes.get_xaxis().set_visible(False)

    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center')

    plt.tight_layout()
    plt.savefig(IMG_FILE)
    plt.close()
    print(f"Graph updated and saved to {IMG_FILE}")

def main():
    append_data(mode, keygen, sign, verify, rejections)
    generate_graph()

if __name__ == '__main__':
    main()

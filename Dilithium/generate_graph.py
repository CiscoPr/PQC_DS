#!/usr/bin/env python3
import os
import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv) != 9:
    print("Usage: python3 generate_graph.py <mode> <keygen_ms> <sign_ms> <verify_ms> <znorm_rej> <lowbits_rej> <hintnorm_rej> <hintcount_rej>")
    sys.exit(1)

# Read command-line arguments
mode, keygen, sign, verify, znorm, lowbits, hintnorm, hintcount = sys.argv[1:9]
CSV_FILE = f"/results/dilithium_times_mode{mode}.csv"
IMG_FILE = f"/results/dilithium_times_mode{mode}.png"
RESULTS_DIR = "/results"

def ensure_results_dir():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        print(f"Created directory: {RESULTS_DIR}")

def append_data():
    ensure_results_dir()
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w') as f:
            f.write("timestamp,mode,keygen,sign,verify,znorm,lowbits,hintnorm,hintcount\n")
            print(f"Created new CSV file: {CSV_FILE}")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, 'a') as f:
        f.write(f"{now_str},{mode},{keygen},{sign},{verify},{znorm},{lowbits},{hintnorm},{hintcount}\n")
    print(f"Appended data: {now_str},{mode},{keygen},{sign},{verify},{znorm},{lowbits},{hintnorm},{hintcount}")

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

    plt.figure(figsize=(12, 7))
    ax1 = plt.gca()

    # Primary Y-axis: timing
    #ax1.plot(df['run'], df['keygen'], marker='o', label='KeyGen (ms)')
    ax1.plot(df['run'], df['sign'], marker='x', color='tab:orange', label='Sign (ms)')
    #ax1.plot(df['run'], df['verify'], marker='s', label='Verify (ms)')
    ax1.set_ylabel('Time (ms)', color='black')

    # Secondary Y-axis: rejection counts
    ax2 = ax1.twinx()
    ax2.plot(df['run'], df['znorm'], marker='^', linestyle='--', color='tab:red', label='znorm')
    ax2.plot(df['run'], df['lowbits'], marker='v', linestyle='--', color='tab:blue', label='lowbits')
    #ax2.plot(df['run'], df['hintnorm'], marker='>', linestyle='--', color='tab:green', label='hintnorm')
    #ax2.plot(df['run'], df['hintcount'], marker='<', linestyle='--', color='tab:purple', label='hintcount')
    ax2.set_ylabel('Rejection Count (per run)', color='black')

    plt.title(f'Dilithium Mode {mode} - Timing and Rejections per Run')
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', ncol=3)
    
    
    plt.tight_layout()
    plt.savefig(IMG_FILE)
    plt.close()
    print(f"Graph updated and saved to {IMG_FILE}")

def main():
    append_data()
    generate_graph()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

USAGE = """\
Usage: python3 generate_all_sphincs_kv.py <results_root>
  <results_root>  — top-level folder under which to recurse (e.g. "results_folder")
"""

if len(sys.argv) != 2:
    print(USAGE)
    sys.exit(1)

RESULTS_ROOT = sys.argv[1]

def plot_kv(csv_path: str):
    """
    Read a SPHINCS+ CSV of the form:
      timestamp,mode,keygen,sign,verify,znorm,lowbits,hintnorm,hintcount
    and plot only keygen & verify (converted to ms) vs run#,
    saving to the same dir with suffix _kv.png
    """
    try:
        df = pd.read_csv(csv_path, parse_dates=['timestamp'])
    except Exception as e:
        print(f"[!] Failed to read {csv_path}: {e}")
        return

    if df.empty:
        print(f"[!] Empty CSV, skipping: {csv_path}")
        return

    df = df.sort_values('timestamp').reset_index(drop=True)
    df['run'] = df.index + 1

    plt.figure(figsize=(10,6))
    plt.plot(df['run'], df['keygen'], color="tab:blue", marker='o', label='KeyGen (ms)')
    plt.plot(df['run'], df['verify'], color="tab:green", marker='s', label='Verify (ms)')
    plt.xlabel('Run #')
    plt.ylabel('Time (ms)')
    # derive a nice title from the CSV’s parent folder name
    variant = os.path.basename(os.path.dirname(csv_path))
    plt.title(f'{variant} — KeyGen & Verify Timing per Run')
    plt.legend()
    plt.tight_layout()

    out_png = csv_path[:-4] + '_kv.png'
    plt.savefig(out_png)
    plt.close()
    print(f"[✓] Wrote {out_png}")

def main():
    if not os.path.isdir(RESULTS_ROOT):
        print(f"[!] Not a directory: {RESULTS_ROOT}")
        sys.exit(1)

    for root, _, files in os.walk(RESULTS_ROOT):
        for fn in files:
            if fn.lower().endswith('.csv'):
                full = os.path.join(root, fn)
                plot_kv(full)

if __name__ == '__main__':
    main()

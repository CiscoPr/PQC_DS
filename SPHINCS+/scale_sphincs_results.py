#!/usr/bin/env python3
"""
Recursively find all CSVs under `results_folder` and divide every numeric column
(except 'timestamp' and 'mode') by 10, writing the result back to the same file.
"""

import os
import pandas as pd

# Change this if your results folder is named differently or located elsewhere:
ROOT = "results_folder"

# Column names that we do NOT touch:
EXCLUDE_COLS = {"timestamp", "mode"}

def is_csv(filename: str) -> bool:
    return filename.lower().endswith(".csv")

def process_csv(path: str) -> None:
    try:
        df = pd.read_csv(path, parse_dates=["timestamp"])
    except Exception:
        # If 'timestamp' isn’t parseable as a date, just load normally:
        df = pd.read_csv(path)

    # For every column except timestamp/mode, attempt to divide by 10
    for col in df.columns:
        if col in EXCLUDE_COLS:
            continue
        # Only divide columns that are numeric (int or float). Pandas will coerce if possible.
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = (df[col] / 10.0).round(3)

    # Overwrite the CSV in place, preserving the same columns/order
    df.to_csv(path, index=False)
    print(f"  → Scaled: {path}")

def main():
    if not os.path.isdir(ROOT):
        print(f"Error: '{ROOT}' is not a directory or does not exist.")
        return

    print(f"Scanning for CSV files under '{ROOT}' …")
    for dirpath, dirnames, filenames in os.walk(ROOT):
        for fn in filenames:
            if is_csv(fn):
                full = os.path.join(dirpath, fn)
                process_csv(full)

    print("Done.")

if __name__ == "__main__":
    main()

import os
import pandas as pd
import matplotlib.pyplot as plt

# Base directory containing the results
base_dir = "results"
columns_to_scale = ["znorm", "lowbits", "hintnorm", "hintcount"]

def generate_graph(csv_path, mode):
    try:
        df = pd.read_csv(csv_path, parse_dates=['timestamp'])
    except Exception as e:
        print(f"Error reading {csv_path}:", e)
        return

    if df.empty:
        print(f"CSV {csv_path} is empty, nothing to plot.")
        return

    df.sort_values('timestamp', inplace=True)
    df['run'] = range(1, len(df) + 1)

    plt.figure(figsize=(12, 7))
    ax1 = plt.gca()

    # Plot signing time on primary axis
    ax1.plot(df['run'], df['sign'], marker='x', color='tab:orange', label='Sign (ms)')
    ax1.set_ylabel('Time (ms)', color='black')

    # Plot rejection counts on secondary axis
    ax2 = ax1.twinx()
    ax2.plot(df['run'], df['znorm'], marker='^', linestyle='--', color='tab:red', label='znorm')
    ax2.plot(df['run'], df['lowbits'], marker='v', linestyle='--', color='tab:blue', label='lowbits')
    # Uncomment below to include hint-based rejections:
    # ax2.plot(df['run'], df['hintnorm'], marker='>', linestyle='--', color='tab:green', label='hintnorm')
    # ax2.plot(df['run'], df['hintcount'], marker='<', linestyle='--', color='tab:purple', label='hintcount')
    ax2.set_ylabel('Rejection Count (per run)', color='black')

    plt.title(f'Dilithium Mode {mode} - Timing and Rejections per Run')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', ncol=3)

    plt.tight_layout()
    graph_path = os.path.join(os.path.dirname(csv_path), "rejection_plot.png")
    plt.savefig(graph_path)
    plt.close()
    print(f"Saved plot: {graph_path}")

# Process each mode
for mode_folder in os.listdir(base_dir):
    mode_path = os.path.join(base_dir, mode_folder)
    csv_path = os.path.join(mode_path, "dilithium_times.csv")

    if not os.path.isfile(csv_path):
        print(f"Skipped (missing file): {csv_path}")
        continue

    # Load and modify CSV
    df = pd.read_csv(csv_path)
    for col in columns_to_scale:
        if col in df.columns:
            df[col] = df[col] / 10.0

    # Save modified CSV
    df.to_csv(csv_path, index=False)
    print(f"Updated: {csv_path}")

    # Generate graph
    generate_graph(csv_path, mode=mode_folder.replace("mode", ""))

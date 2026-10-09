import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


# Project directories
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data" / "raw"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"


def load_signal(file_path):

    timestamps = []
    signals = []

    with open(file_path, "r", newline="") as csv_file:

        reader = csv.DictReader(csv_file)

        for row in reader:

            timestamps.append(
                int(row["timestamp_ms"])
            )

            signals.append(
                float(row["signal"])
            )

    return timestamps, signals


def plot_signal(timestamps, signals, output_path):

    # Convert milliseconds to seconds
    start_time = timestamps[0]

    time_s = [
        (t - start_time) / 1000.0
        for t in timestamps
    ]

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(
        time_s,
        signals,
        linewidth=0.8,
        label="Simulated Biosignal"
    )

    # Configure graph
    ax.set_title("BioLoop-Pi: Simulated Biosignal")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (a.u.)")

    ax.grid(True, alpha=0.3)
    ax.legend()

    # Save figure
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)

    plt.close(fig)


def main():

    # Find CSV files
    csv_files = list(DATA_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found.")
        return

    # Select the most recent CSV file
    latest_file = max(
        csv_files,
        key=lambda file: file.stat().st_mtime
    )

    print(f"Loading: {latest_file.name}")

    # Load signal data
    timestamps, signals = load_signal(latest_file)

    if len(timestamps) < 2:
        print("Not enough samples to plot.")
        return

    print(f"Loaded {len(signals)} samples.")

    # Create output directory
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Output file path
    output_path = OUTPUT_DIR / "simulated_signal_plot.png"

    # Generate plot
    plot_signal(
        timestamps,
        signals,
        output_path
    )

    print(f"Plot saved to: {output_path}")


if __name__ == "__main__":
    main()

import csv
import statistics
from pathlib import Path

# Configuration
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"

TARGET_SAMPLE_RATE = 100  # Hz


def load_timestamps(file_path):
    timestamps = []

    with open(file_path, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            timestamps.append(int(row["timestamp_ms"]))

    return timestamps


def analyze_sampling(timestamps):
    if len(timestamps) < 2:
        raise ValueError("At least 2 samples are required.")

    # Calculate intervals between consecutive samples
    intervals = [
        timestamps[i + 1] - timestamps[i]
        for i in range(len(timestamps) - 1)
    ]

    if any(dt <= 0 for dt in intervals):
        raise ValueError("Timestamps must be increasing.")

    # Interval statistics
    mean_interval = statistics.mean(intervals)
    min_interval = min(intervals)
    max_interval = max(intervals)

    # Population standard deviation of intervals
    jitter_std = statistics.pstdev(intervals)

    # Actual sampling rate
    actual_rate = 1000 / mean_interval

    # Error relative to target sampling rate
    rate_error = (
        abs(TARGET_SAMPLE_RATE - actual_rate)
        / TARGET_SAMPLE_RATE
        * 100
    )

    # Duration between first and last samples
    duration = (
        timestamps[-1] - timestamps[0]
    ) / 1000

    print("=== BioLoop-Pi Sampling Analysis ===")
    print(f"Samples: {len(timestamps)}")
    print(f"Duration: {duration:.3f} s")
    print(f"Mean interval: {mean_interval:.3f} ms")
    print(f"Min interval: {min_interval} ms")
    print(f"Max interval: {max_interval} ms")
    print(f"Interval jitter (std): {jitter_std:.3f} ms")
    print(f"Actual sampling rate: {actual_rate:.3f} Hz")
    print(f"Sampling rate error: {rate_error:.2f}%")


def main():
    # Find recorded CSV files
    csv_files = list(DATA_DIR.glob("simulated_signal_*.csv"))

    if not csv_files:
        print("No CSV files found.")
        return

    # Select the latest CSV file
    latest_file = max(
        csv_files,
        key=lambda file: file.stat().st_mtime
    )

    print(f"Analyzing: {latest_file.name}")

    timestamps = load_timestamps(latest_file)

    analyze_sampling(timestamps)


if __name__ == "__main__":
    main()

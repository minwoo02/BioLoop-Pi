import serial
import matplotlib.pyplot as plt

from collections import deque
from matplotlib.animation import FuncAnimation


# Configuration
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

WINDOW_SECONDS = 5
MAX_SAMPLES = 1000
UPDATE_INTERVAL_MS = 50


def main():
    # Open USB Serial connection
    with serial.Serial(
        SERIAL_PORT,
        BAUD_RATE,
        timeout=0.01
    ) as ser:

        # Buffers for incoming samples
        timestamps = deque(maxlen=MAX_SAMPLES)
        signals = deque(maxlen=MAX_SAMPLES)

        start_time = None

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 5))

        line, = ax.plot(
            [],
            [],
            linewidth=1.0,
            label="Simulated Biosignal"
        )

        ax.set_title("BioLoop-Pi: Real-time Signal")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude (a.u.)")

        ax.set_xlim(0, WINDOW_SECONDS)
        ax.set_ylim(-0.4, 1.6)

        ax.grid(True, alpha=0.3)
        ax.legend()

        def update(frame):
            nonlocal start_time

            # Read available serial data
            for _ in range(100):
                if ser.in_waiting == 0:
                    break

                raw = ser.readline().decode(
                    "utf-8",
                    errors="ignore"
                ).strip()

                try:
                    timestamp_ms, signal = raw.split(",")

                    timestamp_ms = int(timestamp_ms)
                    signal = float(signal)

                except ValueError:
                    continue

                # Convert timestamps to relative seconds
                if start_time is None:
                    start_time = timestamp_ms

                time_s = (
                    timestamp_ms - start_time
                ) / 1000.0

                timestamps.append(time_s)
                signals.append(signal)

            # Update graph
            if timestamps:
                line.set_data(
                    list(timestamps),
                    list(signals)
                )

                latest_time = timestamps[-1]

                right = max(
                    WINDOW_SECONDS,
                    latest_time
                )

                ax.set_xlim(
                    right - WINDOW_SECONDS,
                    right
                )

            return line,

        # Update approximately 20 times per second
        animation = FuncAnimation(
            fig,
            update,
            interval=UPDATE_INTERVAL_MS,
            blit=False,
            cache_frame_data=False
        )

        print("BioLoop-Pi live plot started.")

        try:
            plt.show()
        finally:
            plt.close(fig)


if __name__ == "__main__":
    main()

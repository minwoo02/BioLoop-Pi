import math
import random
import time

SAMPLE_RATE = 100
SAMPLE_INTERVAL_MS = 1000 // SAMPLE_RATE

def generate_signal(t):
    """
    Generate a simple simulated biosignal.

    Componets:
    - 2 Hz base waveform
    - random noise
    - occasional burst-like activity
    """

    # 2 Hz sine wave
    base_signal = 0.2 * math.sin(2 * math.pi * 2 * t)

    #Random noise
    noise = random.uniform(-0.05, 0.05)

    #Random burst-like event
    burst = 0.0

    if random.random() < 0.02:
        burst = random.uniform(0.8, 1.2)

    return base_signal + noise + burst


def main():
    print("BioLoop-Pi signal generator started.")
    print("timestamp_ms,signal")

    start_time = time.ticks_ms()
    next_sample_time = start_time

    while True:
        # Remaining time until the next sample
        remaining_ms = time.ticks_diff(
            next_sample_time,
            time.ticks_ms()
        )

        # Wait only until the scheduled time
        if remaining_ms > 0:
            time.sleep_ms(remaining_ms)

        # Record actual sampling timestamp
        current_time = time.ticks_ms()

        elapsed_ms = time.ticks_diff(
            current_time,
            start_time
        )

        t = elapsed_ms / 1000.0

        # Generate and transmit sample
        signal = generate_signal(t)

        print("{},{}".format(elapsed_ms, signal))

        # Schedule the next sample
        next_sample_time = time.ticks_add(
            next_sample_time,
            SAMPLE_INTERVAL_MS
        )

        # Avoid immediate catch-up bursts if late
        if time.ticks_diff(
            next_sample_time,
            time.ticks_ms()
        ) <= 0:
            next_sample_time = time.ticks_add(
                time.ticks_ms(),
                SAMPLE_INTERVAL_MS
            )


if __name__ == "__main__":
    main()

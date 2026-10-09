import math
import random
import time

SAMPLE_RATE = 100
SAMPLE_INTERVAL_MS = 1000

def generate_signal(t):
    """
    Generate a simple simulated biosignal.

    Componets:
    - 2 Hz base waveform
    - random noise
    - occasional burst-like activity
    """

    base_signal = 0.2 * math.sin(2 * math.pi * 2 * t)

    noise = random.uniform(-0.05, 0.05)

    burst = 0.0

    if random.random() < 0.2:
        burst = random.uniform(0.8, 1.2)

    return base_signal + noise + burst

print("BioLoop-Pi simulated biosignal generator started.")
print("timestamp_ms, signal")

start_time = time.ticks_ms()

while True:
    current_time = time.ticks_ms()

    elapsed_ms = time.ticks_diff(
        current_time,
        start_time
    )

    t = elapsed_ms / 1000.0

    signal = generate_signal(t)

    print("{},{}".format(
        elapsed_ms,
        signal
    ))

    time.sleep_ms(SAMPLE_INTERVAL_MS)
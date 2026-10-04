import serial

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200


def parse_data(line):
    """
    Parse one line received from the Pico.

    Expected format:
        timestamp_ms,signal

    Example:
        1250,0.3842
    """
    timestamp_ms, signal = line.split(",")

    return int(timestamp_ms), float(signal)


def main():
    print("BioLoop-Pi receiver")
    print(f"Opening serial port: {SERIAL_PORT} @ {BAUD_RATE} baud")

    try:
        with serial.Serial(
            SERIAL_PORT,
            BAUD_RATE,
            timeout=1
        ) as ser:

            print("Serial connection established.")
            print("Waiting for data...\n")

            while True:
                try:
                    raw_data = ser.readline().decode(
                        "utf-8",
                        errors="ignore"
                    ).strip()

                    if not raw_data:
                        continue

                    # Informational messages from the Pico
                    if (
                        raw_data.startswith("BioLoop")
                        or raw_data.startswith("timestamp")
                    ):
                        print(raw_data)
                        continue

                    try:
                        timestamp_ms, signal = parse_data(raw_data)

                        print(
                            f"time={timestamp_ms:8d} ms | "
                            f"signal={signal: .4f}"
                        )

                    except ValueError:
                        print(f"Invalid data: {raw_data}")

                except KeyboardInterrupt:
                    print("\nReceiver stopped by user.")
                    break

    except serial.SerialException as error:
        print(f"Serial connection error: {error}")


if __name__ == "__main__":
    main()
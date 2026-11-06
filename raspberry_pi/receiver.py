import serial

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200


def main():
    ser = serial.Serial(
        SERIAL_PORT,
        BAUD_RATE,
        timeout=1
    )

    print("BioLoop-Pi receiver started.")

    try:
        while True:
            raw_data = ser.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if not raw_data:
                continue

            try:
                seq_str, timestamp_str, signal_str = (
                    raw_data.split(",")
                )

                sequence = int(seq_str)
                timestamp_ms = int(timestamp_str)
                signal = float(signal_str)

            except ValueError:
                continue

            print(
                f"seq={sequence} | "
                f"time={timestamp_ms} ms | "
                f"signal={signal:.4f}"
            )

    except KeyboardInterrupt:
        print("\nReceiver stopped.")

    finally:
        ser.close()


if __name__ == "__main__":
    main()

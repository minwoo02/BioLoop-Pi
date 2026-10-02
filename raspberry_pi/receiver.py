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
    print(f"Listening on {SERIAL_PORT}")

    while True:
        raw_data = ser.readline().decode("utf-8").strip()

        if not raw_data:
            continue

        # Pico 시작 메시지는 무시
        if raw_data.startswith("BioLoop") or raw_data.startswith("timestamp"):
            print(raw_data)
            continue

        try:
            timestamp_ms, signal = raw_data.split(",")

            timestamp_ms = int(timestamp_ms)
            signal = float(signal)

            print(
                f"time={timestamp_ms:6d} ms | "
                f"signal={signal: .4f}"
            )

        except ValueError:
            print(f"Invalid data: {raw_data}")

if __name__ == "__main__":
    main()
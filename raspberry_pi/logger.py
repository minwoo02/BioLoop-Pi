import serial
import csv
from datetime import datetime
from pathlib import Path


SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"


def main():
    # data/raw 폴더가 없으면 자동 생성
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

    filename = (
        "simulated_signal_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
    )

    file_path = DATA_DIR / filename
    sample_count = 0

    # Pico와 Serial 연결
    ser = serial.Serial(
        SERIAL_PORT,
        BAUD_RATE,
        timeout=1
    )

    print("BioLoop-Pi data logger started.")
    print(f"Listening on {SERIAL_PORT}")
    print(f"Saving data to: {file_path}")
    print("Press Ctrl+C to stop.\n")

    try:
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)

            # CSV header
            writer.writerow([
                "seq",
                "timestamp_ms",
                "signal"
            ])

            while True:
                raw_data = ser.readline().decode(
                    "utf-8",
                    errors="ignore"
                ).strip()

                if not raw_data:
                    continue

                try:
                    # Parse three fields
                    seq, timestamp_ms, signal = raw_data.split(",")

                    # Convert to numeric types
                    seq = int(seq)
                    timestamp_ms = int(timestamp_ms)
                    signal = float(signal)

                    # Save received sample
                    writer.writerow([
                        seq,
                        timestamp_ms,
                        signal
                    ])

                    sample_count += 1

                    # 100 samples마다 파일에 확실히 기록
                    if sample_count % 100 == 0:
                        csv_file.flush()

                        print(
                            f"{sample_count} samples recorded"
                        )

                except ValueError:
                    # MicroPython 시작 메시지 등은 무시
                    continue

    except KeyboardInterrupt:
        print("\nRecording stopped.")
        print(f"Total samples: {sample_count}")
        print(f"Saved to: {file_path}")

    finally:
        ser.close()


if __name__ == "__main__":
    main()
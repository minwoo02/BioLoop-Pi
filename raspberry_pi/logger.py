import csv
import os
from datetime import datetime

import serial


SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

DATA_DIR = "data/raw"


def main():
    # data/raw 폴더가 없으면 자동 생성
    os.makedirs(DATA_DIR, exist_ok=True)

    # 기록 시작 시간을 파일명에 사용
    start_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = os.path.join(
        DATA_DIR,
        f"simulated_signal_{start_time}.csv"
    )

    # Pico와 Serial 연결
    ser = serial.Serial(
        SERIAL_PORT,
        BAUD_RATE,
        timeout=1
    )

    sample_count = 0

    print("BioLoop-Pi data logger started.")
    print(f"Listening on {SERIAL_PORT}")
    print(f"Saving data to: {file_path}")
    print("Press Ctrl+C to stop.\n")

    try:
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)

            # CSV header
            writer.writerow([
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
                    timestamp_ms, signal = raw_data.split(",")

                    timestamp_ms = int(timestamp_ms)
                    signal = float(signal)

                    writer.writerow([
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
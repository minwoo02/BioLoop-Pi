# Biosignal Data Logger

**Date:** 2026-10-06

## 오늘의 목표

Raspberry Pi Pico 2 W에서 USB Serial로 전달되는 simulated biosignal을
Raspberry Pi 5에서 수신하여 CSV 파일로 저장할 수 있는 data logger를 구현한다.

이번 단계에서는 `logger.py`의 코드를 작성하고,
각 코드가 어떤 역할을 수행하는지 분석하였다.

## 현재 시스템 구조

```text
Raspberry Pi Pico 2 W
        |
        | main.py
        | simulated biosignal
        |
        | USB Serial
        v
Raspberry Pi 5
        |
        | logger.py
        v
CSV Data File
```

## 구현한 파일

```text
raspberry_pi/logger.py
```

`logger.py`는 Pico에서 전송되는 데이터를 읽어 다음과 같은 CSV 형식으로 저장하도록 설계하였다.

```text
timestamp_ms,signal
100,0.1523
110,0.1834
120,0.1642
```

## 주요 설정

### Serial Port

```python
SERIAL_PORT = "/dev/ttyACM0"
```

Raspberry Pi에서 Pico 2 W가 USB Serial 장치로 인식되는 경로이다.

### Baud Rate

```python
BAUD_RATE = 115200
```

Serial 연결을 설정할 때 사용하는 통신 속도 값이다.

현재 Pico는 USB CDC Serial을 사용하므로 일반적인 UART 통신과는 동작 방식에 차이가 있지만,
Python Serial 인터페이스를 구성하기 위해 baud rate 값을 지정한다.

### Data Directory

```python
DATA_DIR = "data/raw"
```

수집한 원시 데이터를 저장하는 경로이다.

실험에서 생성되는 원시 데이터는 GitHub에 직접 업로드하지 않고
로컬 환경에서 관리하도록 `.gitignore`에 `data/raw/`를 등록해 두었다.

## 데이터 저장 과정

`logger.py`의 전체 데이터 흐름은 다음과 같다.

```text
Pico 데이터 수신
        ↓
Serial readline()
        ↓
timestamp와 signal 분리
        ↓
문자열을 숫자로 변환
        ↓
CSV 파일에 한 줄 저장
        ↓
sample_count 증가
        ↓
다음 데이터 수신
```

## CSV 파일 생성

먼저 다음 코드를 통해 데이터 저장 폴더가 존재하지 않을 경우 자동으로 생성한다.

```python
os.makedirs(DATA_DIR, exist_ok=True)
```

측정할 때마다 기존 파일을 덮어쓰지 않도록 현재 시간을 파일명에 포함한다.

예:

```text
simulated_signal_20261006_010000.csv
```

따라서 여러 번 실험하더라도 각각의 데이터 파일을 별도로 보관할 수 있다.

## CSV Writer

CSV 파일의 첫 번째 행에는 다음 header를 기록한다.

```text
timestamp_ms,signal
```

이후 Pico에서 수신한 각 sample을 한 행씩 저장한다.

## Sample Count

```python
sample_count += 1
```

저장된 sample의 개수를 확인하기 위한 counter를 사용한다.

100개의 sample이 저장될 때마다 현재 기록 상태를 출력하도록 구성하였다.

현재 simulated biosignal의 sampling rate가 100 Hz이므로
100 samples는 약 1초의 데이터에 해당한다.

## Buffer와 flush

Python은 파일을 작성할 때 데이터를 즉시 저장장치에 기록하지 않고
일시적으로 buffer에 보관할 수 있다.

다음 코드를 사용하여 100 samples마다 buffer의 데이터를 실제 파일에 기록하도록 하였다.

```python
csv_file.flush()
```

이를 통해 프로그램이 갑자기 종료되는 경우 발생할 수 있는 데이터 손실을 줄일 수 있다.

## Exception Handling

이번 코드에서 `try`, `except`, `finally` 구조를 사용하였다.

### ValueError

Pico에서 전달되는 데이터가 예상한

```text
timestamp,signal
```

형식이 아닐 경우 `ValueError`가 발생할 수 있다.

이 경우 해당 데이터를 무시하고 다음 Serial 데이터를 읽도록 처리하였다.

```python
except ValueError:
    continue
```

### KeyboardInterrupt

사용자가 `Ctrl + C`를 입력하여 데이터 기록을 중단하면
Python에서 `KeyboardInterrupt`가 발생한다.

이를 처리하여 긴 traceback 대신
기록한 sample 수와 저장 파일 위치를 출력하도록 구성하였다.

### finally

프로그램이 종료될 때 Serial Port를 반드시 닫도록 다음 코드를 사용하였다.

```python
finally:
    ser.close()
```

이를 통해 `/dev/ttyACM0` 장치가 불필요하게 열린 상태로 남는 것을 방지한다.

## `receiver.py`와 `logger.py`의 차이

### receiver.py

```text
Pico
 ↓
Serial 데이터 수신
 ↓
Terminal 출력
```

Pico와 Raspberry Pi 사이의 통신이 정상적으로 이루어지는지 확인하기 위한 프로그램이다.

### logger.py

```text
Pico
 ↓
Serial 데이터 수신
 ↓
Parsing
 ↓
CSV 저장
```

실험 데이터를 실제 파일로 기록하기 위한 프로그램이다.

## 현재까지 이해한 내용

- Raspberry Pi에서 Pico는 `/dev/ttyACM0` Serial 장치로 접근한다.
- Pico의 `print()` 출력은 USB Serial을 통해 Raspberry Pi에 전달된다.
- `ser.readline()`을 사용하여 한 줄씩 데이터를 수신한다.
- CSV를 이용하여 timestamp와 signal 값을 구조적으로 저장할 수 있다.
- `try-except`를 이용하여 잘못된 데이터나 사용자 종료를 처리한다.
- `finally`를 이용하여 Serial Port를 안전하게 닫는다.
- `flush()`를 이용해 buffer의 데이터를 주기적으로 파일에 반영한다.

## 현재 상태

- [x] `logger.py` 작성
- [x] Serial data logging 구조 이해
- [x] CSV 저장 방식 이해
- [x] Exception handling 구조 분석
- [x] Raspberry Pi 5에서 `logger.py` 실제 실행
- [x] CSV 파일 생성 확인
- [ ] 저장된 sample 확인
- [ ] 저장 데이터 visualization

## 다음 단계

저장된 signal을 Python으로 시각화하고 분석하는 단계로 진행한다.
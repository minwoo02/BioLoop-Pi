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

---

## Experiment Results — 2026-10-09

### 1. 실험 목적

Raspberry Pi Pico 2 W에서 생성한 simulated biosignal을
USB Serial 통신을 통해 Raspberry Pi 5로 전송하고,
`logger.py`를 이용하여 CSV 파일에 정상적으로 기록되는지 검증하였다.

추가로 CSV에 저장된 timestamp를 이용하여
실제 평균 sampling rate를 계산하고,
설정한 sampling rate와 비교하였다.

### 2. 실험 환경

| 항목 | 구성 |
|---|---|
| Microcontroller | Raspberry Pi Pico 2 W |
| Host Computer | Raspberry Pi 5 4GB |
| Firmware | MicroPython |
| Communication | USB CDC Serial |
| Serial Interface | `/dev/ttyACM0` |
| Data Logger | `raspberry_pi/logger.py` |
| Target Sampling Rate | 100 Hz |
| Data Format | CSV |
| Development Environment | Mac SSH → Raspberry Pi 5 |

### 3. 초기 실험에서 발견한 문제

초기에는 `signal_generator.py`에서 설정한 sampling rate와
실제 측정된 sampling rate가 일치하지 않는 문제가 발생하였다.

첫 번째 실험에서는 다음과 같이 설정되어 있었다.

```python
SAMPLE_RATE = 100
SAMPLE_INTERVAL_MS = 100
```

실제 측정 결과 평균 sampling rate는 약 9.97 Hz였다.

이후 설정값을 확인하는 과정에서 다음과 같은 코드도 발견하였다.

```python
SAMPLE_RATE = 100
SAMPLE_INTERVAL_MS = 1000
```

이 경우 실제 sampling interval은 약 1000 ms였으며,
CSV 데이터에서도 약 1 Hz의 sampling rate가 관찰되었다.

문제의 원인은 `SAMPLE_RATE` 변수와 실제 대기 시간을 결정하는
`SAMPLE_INTERVAL_MS` 값이 일치하지 않았기 때문이었다.

### 4. 문제 해결

Sampling rate를 변경할 때 sampling interval도 함께 변경되도록
다음과 같이 코드를 수정하였다.

```python
SAMPLE_RATE = 100
SAMPLE_INTERVAL_MS = 1000 // SAMPLE_RATE
```

이렇게 하면 설정된 sampling rate를 기준으로
sampling interval을 밀리초 단위로 계산할 수 있다.

100 Hz를 설정하면 다음과 같다.

$$
T_s = \frac{1}{f_s}
$$

$$
T_s = \frac{1}{100} = 0.01\,s = 10\,ms
$$

단, 현재 코드는 `time.sleep_ms()`를 이용하기 때문에
반복문 내부의 연산 시간과 USB Serial 출력 시간까지 포함하면
실제 sampling interval이 10 ms보다 길어질 수 있다.

### 5. 최종 실험 결과

수정된 코드를 Pico 내부 Flash Memory에 `main.py`로 저장한 후,
Raspberry Pi에서 `logger.py`를 실행하여 데이터를 다시 수집하였다.

**Recorded File**

```text
data/raw/simulated_signal_20261009_162918.csv
```

**Measurement Results**

| Parameter | Target | Measured |
|---|---:|---:|
| Sampling Rate | 100 Hz | 95.820 Hz |
| Sampling Interval | 10 ms | 10.436 ms |
| Minimum Interval | 10 ms | 10 ms |
| Maximum Interval | 10 ms | 16 ms |
| Recorded Samples | - | 1,115 |
| Sampling Rate Error | 0% | 4.18% |

CSV 파일에는 총 1,115개의 sample이 기록되었다.

### 6. 평균 Sampling Rate 계산

CSV 파일에 저장된 timestamp를 이용하여
각 sample 사이의 시간 간격을 계산하였다.

$$
\Delta t_i = t_{i+1} - t_i
$$

측정된 평균 sampling interval은 다음과 같다.

$$
\overline{\Delta t} = 10.436\,ms
$$

따라서 실제 평균 sampling rate는 다음과 같이 계산하였다.

$$
f_{s,\mathrm{avg}} = \frac{1000}{\overline{\Delta t}}
$$

$$
f_{s,\mathrm{avg}} \approx 95.820\,Hz
$$

목표 sampling rate 대비 오차는 다음과 같다.

$$
\mathrm{Error} =
\frac{|f_{\mathrm{target}} - f_{\mathrm{actual}}|}
{f_{\mathrm{target}}} \times 100
$$

$$
\mathrm{Error} =
\frac{|100 - 95.820|}{100} \times 100
= 4.18\%
$$

### 7. 결과 분석 및 고찰

실제 측정된 평균 sampling rate는 95.820 Hz로,
목표인 100 Hz보다 약 4.18% 낮게 나타났다.

현재 신호 생성 코드는 다음 순서로 실행된다.

```text
Timestamp 측정
        ↓
Simulated Signal 생성
        ↓
USB Serial 출력
        ↓
sleep_ms(10)
        ↓
다음 반복
```

따라서 실제 sampling interval은 단순히
`time.sleep_ms(10)`의 대기 시간만으로 결정되지 않는다.

반복문 내부의 연산 및 USB Serial 출력에 필요한 시간이
추가되기 때문에 실제 sampling rate가 목표보다 낮아질 수 있다.

이번 실험에서는 최소 10 ms, 최대 16 ms의
sampling interval이 관찰되었다.

이는 시간 간격에 변동이 있음을 보여주지만,
정확한 jitter 특성과 데이터 손실 여부는 추가 분석이 필요하다.

향후에는 timer 기반 sampling 및 buffering 구조를 도입하여
sampling interval의 정확성과 안정성을 개선할 예정이다.

### 8. 결론

이번 실험을 통해 다음 사항을 확인하였다.

- Raspberry Pi Pico 2 W의 simulated biosignal 생성
- USB Serial 통신을 이용한 데이터 전송
- Raspberry Pi 5에서 CSV Data Logging
- 총 1,115개 sample 기록
- 실제 평균 sampling rate 95.820 Hz 측정
- 목표 sampling rate 대비 4.18% 오차 확인
- 코드의 sampling interval 설정 오류 발견 및 수정

이를 통해 BioLoop-Pi의 기본적인
**Signal Generation → Transmission → Data Logging**
파이프라인이 정상적으로 동작함을 확인하였다.

향후에는 sampling timing의 정확성을 개선하고,
저장된 데이터를 시각화하여 신호의 특성을 분석할 예정이다.

## 현재 상태

- [x] `logger.py` 작성
- [x] Serial data logging 구조 이해
- [x] CSV 저장 방식 이해
- [x] Exception handling 구조 분석
- [x] Raspberry Pi 5에서 `logger.py` 실제 실행
- [x] CSV 파일 생성 확인
- [x] 저장된 sample 확인
- [x] Sampling interval 설정 오류 수정
- [x] 평균 sampling rate 측정
- [x] 목표 sampling rate와 실제 측정값 비교
- [ ] 저장 데이터 visualization
- [ ] Sampling jitter 상세 분석
- [ ] 정확한 sampling timing 제어
## 다음 단계

저장된 signal을 Python으로 시각화하고 분석하는 단계로 진행한다.
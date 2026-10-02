# Pico to Raspberry Pi Serial Communication

**Date:** 2026-10-02

## 오늘의 목표

Raspberry Pi Pico 2 W에서 생성한 simulated biosignal을 USB Serial을 통해 Raspberry Pi 5로 전송하고, Raspberry Pi에서 데이터를 수신한다.

## 구현한 내용

### Raspberry Pi Pico 2 W

- MicroPython 설치 및 동작 확인
- `signal_generator.py` 작성
- 100 Hz sampling rate로 simulated biosignal 생성
- USB Serial을 통해 timestamp와 signal 값을 출력
- `signal_generator.py`를 Pico 내부에 `main.py`로 저장
- Pico 부팅 시 `main.py` 자동 실행 확인

출력 형식:

```text
timestamp_ms,signal
```

예:

```text
100,0.1523
110,0.1834
120,0.1642
```

## Raspberry Pi 5

- Pico 2 W를 Raspberry Pi 5의 USB 포트에 연결
- Pico가 `/dev/ttyACM0`로 인식되는 것을 확인
- `receiver.py` 작성
- PySerial을 사용하여 Pico의 USB Serial 데이터를 수신
- timestamp와 signal 데이터를 파싱하여 터미널에 출력

예:

```text
BioLoop-Pi receiver started.
Listening on /dev/ttyACM0

time=   100 ms | signal= 0.1523
time=   110 ms | signal= 0.1834
time=   120 ms | signal= 0.1642
```

## mpremote

MicroPython이 설치된 Pico를 Raspberry Pi 터미널에서 제어하기 위해 `mpremote`를 사용하였다.

### Raspberry Pi에 있는 코드를 Pico에서 임시 실행

```bash
mpremote connect /dev/ttyACM0 run pico/signal_generator.py
```

이 명령은 Raspberry Pi에 저장된 `signal_generator.py`를 Pico에서 임시로 실행한다.

Pico Flash에는 해당 파일이 영구 저장되지 않는다.

### Pico Flash에 `main.py`로 저장

```bash
mpremote connect /dev/ttyACM0 fs cp pico/signal_generator.py :main.py
```

이 명령은 Raspberry Pi에 있는 `signal_generator.py`를 Pico 내부 Flash Memory에 `main.py`라는 이름으로 저장한다.

MicroPython은 부팅 시 `main.py`를 자동으로 실행한다.

### Pico 재부팅

```bash
mpremote connect /dev/ttyACM0 reset
```

Pico를 재부팅하면 내부 Flash에 저장된 `main.py`가 자동으로 실행된다.

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
        | receiver.py
        v
Serial Data Parsing
```

현재 Pico와 Raspberry Pi는 다음과 같이 역할을 분담한다.

### Pico 2 W

- simulated biosignal 생성
- 일정한 sampling interval 유지
- USB Serial을 통한 데이터 송신

### Raspberry Pi 5

- Serial 데이터 수신
- timestamp와 signal 값 parsing
- 향후 데이터 저장 및 신호처리 수행

## 문제 및 해결

### 1. MicroPython REPL 데이터만 수신되는 문제

처음 `receiver.py`를 실행했을 때 다음과 같은 데이터가 출력되었다.

```text
MicroPython v1.29.0 ...
Type "help()" for more information.
>>>
```

이는 Pico에서 `signal_generator.py`가 실행되고 있지 않고 MicroPython REPL 상태에 있었기 때문이었다.

`signal_generator.py`를 Pico 내부 Flash Memory에 `main.py`로 저장하여 해결하였다.

### 2. `mpremote` 명령을 사용할 수 없는 문제

처음에는 다음과 같은 메시지가 출력되었다.

```text
-bash: mpremote: command not found
```

Raspberry Pi에 `mpremote`를 설치한 후 Pico 내부 파일 관리와 코드 실행이 가능해졌다.

### 3. `receiver.py` 종료 시 KeyboardInterrupt 출력

`receiver.py` 실행 중 `Ctrl + C`를 누르면 다음과 같은 메시지가 출력되었다.

```text
KeyboardInterrupt
```

이는 프로그램 오류가 아니라 사용자가 실행 중인 Python 프로그램을 직접 중단했기 때문에 발생한 정상적인 동작이다.

## 현재 상태

- [x] Pico 2 W MicroPython 설정
- [x] Pico 2 W 기본 동작 확인
- [x] Simulated biosignal 생성
- [x] USB Serial 통신 확인
- [x] Raspberry Pi 5에서 Pico 인식
- [x] Raspberry Pi에서 Serial 데이터 수신
- [x] Pico Flash에 `main.py` 저장
- [x] Pico 부팅 시 signal generator 자동 실행

## 다음 단계

Pico에서 전달받은 signal 데이터를 Raspberry Pi 5에서 CSV 파일로 저장한다.

이후 저장된 데이터를 이용하여 다음 작업을 진행할 예정이다.

- Signal visualization
- Digital filtering
- FFT analysis
- Feature extraction
- Deep learning 기반 signal decoding

## Development Environment

현재 Raspberry Pi 5는 Mac에서 SSH를 통해 원격으로 개발하고 있다.

향후 HDMI 모니터를 연결하여 Raspberry Pi OS 데스크톱 환경에서
직접 개발 및 real-time visualization을 수행하는 방식으로 변경할 수 있다.
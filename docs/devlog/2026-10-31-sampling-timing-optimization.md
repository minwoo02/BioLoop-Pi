# Phase 1-9 — Sampling Timing Optimization

**Date:** 2026-10-31  
**Project:** BioLoop-Pi  
**Environment:** Raspberry Pi Pico 2 W, Raspberry Pi 5, MicroPython, Python

## 1. Objective

이번 단계에서는 Raspberry Pi Pico 2 W의 가상 생체신호 생성 과정에서 발생하는 Sampling Rate Error와 Sampling Interval Jitter를 개선하였다.

기존에는 `time.sleep_ms()`를 이용하여 샘플링 간격을 제어했지만, 신호 생성 및 USB Serial 출력에 소요되는 시간이 반복 주기에 누적되는 문제가 있었다.

이를 개선하기 위해 예약된 샘플링 시각을 기준으로 동작하는 **Periodic Scheduling** 방식을 적용하고, 변경 전후 성능을 비교하였다.

## 2. Problem Identification

Phase 1-7에서 측정한 기존 성능은 다음과 같았다.

| Parameter | Result |
|---|---:|
| Target Sampling Rate | 100 Hz |
| Actual Sampling Rate | 95.820 Hz |
| Mean Sampling Interval | 10.436 ms |
| Interval Jitter (Std) | 0.522 ms |
| Sampling Rate Error | 4.18% |

기존 코드는 다음과 같은 구조였다.

```python
while True:
    current_time = time.ticks_ms()
    signal = generate_signal(t)

    print("{},{}".format(elapsed_ms, signal))

    time.sleep_ms(SAMPLE_INTERVAL_MS)
```

이 방식은 신호 생성과 Serial 출력이 완료된 후 지정된 시간만큼 대기한다.

따라서 실제 반복 주기는 다음과 같이 증가할 수 있다.

`Sampling Period ≈ Processing Time + Sleep Time`

목표 간격을 10 ms로 설정하더라도 실제 샘플링 간격은 10 ms보다 길어질 수 있다.

## 3. Implementation

**Modified File:** `pico/signal_generator.py`

### 3.1 Periodic Scheduling

기존의 고정 대기 방식 대신 다음 샘플링 목표 시각을 명시적으로 관리하도록 수정하였다.

```python
start_time = time.ticks_ms()
next_sample_time = start_time

while True:
    remaining_ms = time.ticks_diff(
        next_sample_time,
        time.ticks_ms()
    )

    if remaining_ms > 0:
        time.sleep_ms(remaining_ms)

    current_time = time.ticks_ms()

    # Generate and transmit signal
    ...

    next_sample_time = time.ticks_add(
        next_sample_time,
        SAMPLE_INTERVAL_MS
    )
```

기존 방식과 달리 이전에 예약한 시각에 샘플링 간격을 더해 다음 목표 시각을 계산한다.

예를 들어 목표 간격이 10 ms이면 샘플링 목표 시각은 0, 10, 20, 30 ms 순서로 설정된다.

이로써 처리 시간이 매 반복마다 누적되는 현상을 줄일 수 있다.

### 3.2 Handling Missed Deadlines

신호 생성이나 USB Serial 출력이 지연되어 다음 예약 시각까지 놓친 경우, 다음 샘플링 시각을 재설정하도록 구현하였다.

```python
if time.ticks_diff(
    next_sample_time,
    time.ticks_ms()
) <= 0:
    next_sample_time = time.ticks_add(
        time.ticks_ms(),
        SAMPLE_INTERVAL_MS
    )
```

이는 밀린 샘플을 빠르게 연속 생성하는 현상을 방지하기 위한 처리다.

단, 예약 시각을 놓친 경우 기존 시간표에서 벗어날 수 있으며, 누락된 샘플을 복구하는 기능은 아니다.

## 4. Experimental Setup

- **Signal Source:** Raspberry Pi Pico 2 W
- **Data Receiver:** Raspberry Pi 5
- **Communication:** USB Serial
- **Target Sampling Rate:** 100 Hz
- **Target Sampling Interval:** 10 ms
- **Signal:** 2 Hz Sine Wave + Random Noise + Burst-like Events
- **Data Logger:** `raspberry_pi/logger.py`
- **Analysis Script:** `raspberry_pi/analyze_sampling.py`

### Dataset

**Before Optimization**

`simulated_signal_20261009_162918.csv`

**After Optimization**

`simulated_signal_20261031_192750.csv`

각 CSV 파일의 Timestamp를 이용하여 연속된 샘플링 간격을 계산하고, 평균 샘플링 주파수와 표준편차를 비교하였다.

## 5. Experimental Results

| Parameter | Before | After |
|---|---:|---:|
| Recorded Samples | 1,115 | 3,682 |
| Duration | 11.626 s | 36.810 s |
| Mean Interval | 10.436 ms | 10.000 ms |
| Min Interval | 10 ms | 9 ms |
| Max Interval | 16 ms | 11 ms |
| Interval Jitter (Std) | 0.522 ms | 0.160 ms |
| Actual Sampling Rate | 95.820 Hz | 100.000 Hz |
| Sampling Rate Error | 4.18% | 0.00% |

### 5.1 Sampling Rate Accuracy

기존 평균 샘플링 주파수는 95.820 Hz였으나, Periodic Scheduling 적용 후 100.000 Hz로 측정되었다.

목표 대비 샘플링 주파수 오차는 표시된 정밀도 기준으로 4.18%에서 0.00%로 감소하였다.

### 5.2 Sampling Interval Stability

샘플링 간격의 표준편차는 0.522 ms에서 0.160 ms로 감소하였다.

이는 약 **69.3%의 표준편차 감소**에 해당한다.

또한 최대 샘플링 간격이 16 ms에서 11 ms로 감소하여, 샘플링 간격이 목표인 10 ms 주변에 더 밀집하게 나타났다.

## 6. Discussion

이번 실험에서는 예약 시각 기반의 샘플링 스케줄링이 기존의 고정 대기 방식보다 평균 샘플링 주파수와 간격 안정성 측면에서 더 나은 결과를 보였다.

이를 통해 단순히 일정 시간 대기하는 것과 정확한 시점을 목표로 동작하도록 스케줄링하는 것은 서로 다르다는 점을 확인하였다.

다만 다음과 같은 한계가 존재한다.

1. Timestamp 해상도가 1 ms이므로 그보다 작은 시간 변동은 확인하기 어렵다.
2. Sampling Interval의 표준편차는 간격 변동의 지표이며 하드웨어 클록의 정밀 Jitter를 직접 측정한 값은 아니다.
3. 최적화 전후 데이터의 측정 시간이 다르고 각각 한 차례의 실험이므로, 반복 측정을 통한 재현성 검증이 필요하다.
4. 현재는 Sample Sequence Number가 없어 데이터 손실 여부를 독립적으로 확인하기 어렵다.
5. 소프트웨어 스케줄링 방식이므로 하드웨어 타이머 기반 샘플링의 정확도를 보장하지는 않는다.

## 7. Conclusion

이번 단계에서는 Pico 2 W의 신호 생성 스케줄링 방식을 개선하고, 실제 수집 데이터를 이용하여 성능 향상을 확인하였다.

- [x] 기존 Sampling Timing 문제 분석
- [x] Periodic Scheduling 방식 구현
- [x] Missed Deadline 처리 로직 추가
- [x] Pico 프로그램 업데이트
- [x] 개선된 방식으로 신호 데이터 수집
- [x] Sampling Rate 및 Jitter 비교
- [x] 최적화 전후 성능 개선 확인

**Main Findings**

- Actual Sampling Rate: 95.820 → 100.000 Hz
- Sampling Rate Error: 4.18 → 0.00%
- Interval Jitter Std: 0.522 → 0.160 ms
- Jitter Std Reduction: 약 69.3%

## 8. Next Step

**Phase 2 — Sampling & Communication Reliability**

다음 단계에서는 Sampling Accuracy뿐 아니라 실제 데이터 전달 과정의 신뢰성을 검증한다.

주요 개발 목표는 다음과 같다.

- Sample Sequence Number 추가
- USB Serial Data Loss Detection
- Serial Buffering 개선
- 장시간 데이터 수집 안정성 분석

이를 통해 실제 ADC 및 생체신호 센서와 연동할 수 있는 신뢰성 높은 데이터 수집 시스템으로 발전시키고자 한다.
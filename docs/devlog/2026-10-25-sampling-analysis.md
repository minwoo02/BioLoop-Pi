# Sampling Rate & Jitter Analysis

**Analysis Date:** 2026-10-25  
**Data Collection Date:** 2026-10-09  
**Phase:** 1-7

## 실험 목적

Raspberry Pi Pico 2 W에서 생성하고 Raspberry Pi 5에서 저장한 simulated biosignal의 timestamp를 이용하여 실제 sampling rate와 sampling interval의 변동성을 분석한다.

## 분석 대상

- Data File: `simulated_signal_20261009_162918.csv`
- Analysis Script: `raspberry_pi/analyze_sampling.py`
- Target Sampling Rate: 100 Hz
- Timestamp Resolution: 1 ms

## 측정 결과

| Parameter | Result |
|---|---:|
| Recorded Samples | 1,115 |
| Duration | 11.626 s |
| Mean Sampling Interval | 10.436 ms |
| Minimum Interval | 10 ms |
| Maximum Interval | 16 ms |
| Interval Jitter (Std) | 0.522 ms |
| Actual Sampling Rate | 95.820 Hz |
| Sampling Rate Error | 4.18% |

## 분석 방법

연속된 timestamp 사이의 간격을 계산하였다.

\[
\Delta t_i = t_{i+1} - t_i
\]

평균 sampling interval을 이용하여 실제 sampling rate를 계산하였다.

\[
f_s = \frac{1000}{\overline{\Delta t}}
\]

Sampling interval의 변동성을 평가하기 위해 모집단 표준편차를 계산하였다.

```python
jitter_std = statistics.pstdev(intervals)
```

## 결과 및 고찰

실제 평균 sampling rate는 95.820 Hz로, 목표인 100 Hz보다 4.18% 낮게 나타났다.

이는 현재 사용 중인 `time.sleep_ms()` 기반 반복문에서 신호 생성과 USB Serial 출력 등의 처리 시간이 추가되기 때문일 가능성이 있다.

Sampling interval의 표준편차는 0.522 ms였으며, 최소 10 ms에서 최대 16 ms까지의 간격이 관찰되었다.

이를 통해 전체 평균 sampling rate뿐 아니라 개별 sampling interval에도 변동이 존재한다는 것을 확인하였다.

다만 현재 timestamp는 밀리초 단위로 기록되므로 더 짧은 시간 변동을 정확히 평가하기 어렵다. 또한 sample sequence number가 없기 때문에 데이터 손실 여부는 별도의 검증이 필요하다.

## 결론

- CSV timestamp 기반 sampling rate 분석 완료
- 실제 평균 sampling rate 95.820 Hz 확인
- 목표 대비 4.18%의 sampling rate error 확인
- Interval jitter standard deviation 0.522 ms 확인
- 최소 및 최대 sampling interval 확인

현재 데이터 수집 시스템의 기본 기능은 검증되었으며, 향후 timer 기반 sampling과 buffering을 통해 timing accuracy를 개선할 예정이다.

## 현재 상태

- [x] Sampling interval 계산
- [x] 평균 sampling rate 분석
- [x] Sampling rate error 계산
- [x] Interval standard deviation 계산
- [x] 측정 결과 검증
- [ ] Timing optimization
- [ ] Data loss verification

## Next Step

Phase 1-8 — Real-time Signal Visualization

Raspberry Pi 5에서 USB Serial 데이터를 실시간으로 수신하고 HDMI 모니터에 신호 파형을 표시한다.
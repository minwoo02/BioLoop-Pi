# Project Setup

**Date:** 2026-10-02

## 오늘의 목표

BioLoop-Pi 프로젝트의 기본 GitHub 환경을 구성하고,
향후 개발 방향과 시스템 구조를 정리한다.

## 프로젝트 목적

BioLoop-Pi는 Raspberry Pi 5와 Raspberry Pi Pico 2 W를 이용하여
생체신호 수집, 신호처리, 머신러닝, 피드백 제어를 단계적으로 구현하는
개인 연구 프로젝트이다.

초기에는 실제 생체신호 대신 가상 신호를 사용하여
전체 데이터 흐름과 시스템 구조를 구현한 뒤,
향후 EMG, ECG, 외부 ADC, neural signal processing으로 확장할 예정이다.

## 시스템 역할

### Raspberry Pi Pico 2 W

- 센서 인터페이스
- ADC 데이터 수집
- 일정한 주기의 sampling
- GPIO 제어
- 실시간 제어
- Raspberry Pi 5와 통신

### Raspberry Pi 5

- 데이터 수신
- Python 기반 신호처리
- 실시간 시각화
- 데이터 저장
- 머신러닝
- 고수준 시스템 제어

## 현재 구성

- Raspberry Pi 5 4GB
- Raspberry Pi Pico 2 W
- Breadboard
- Jumper wires
- Resistor kit
- USB data cable

## 완료한 작업

- 로컬 BioLoop-Pi 폴더 생성
- Git 저장소 초기화
- GitHub repository 연결
- README 작성
- 기본 프로젝트 디렉터리 구성
- .gitignore 설정

## 다음 단계

Raspberry Pi Pico 2 W에서 가상의 biological signal을 생성하고,
USB Serial을 통해 Raspberry Pi 5로 데이터를 전송한다.

그 후 Raspberry Pi 5에서 실시간 그래프로 시각화한다.
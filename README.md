# BioLoop-Pi

A Raspberry Pi-based bioelectronic interface project for biosignal acquisition, signal processing, machine learning, and closed-loop feedback.

## Overview

BioLoop-Pi is a personal research project focused on building a modular bioelectronic interface using Raspberry Pi 5 and Raspberry Pi Pico 2 W.

The project starts with simulated biological signals and basic sensor interfaces, then gradually expands toward real biosignal acquisition, digital signal processing, machine learning, and closed-loop control.

The long-term goal is to develop a platform that can eventually be extended toward neural interfaces, MEA-based systems, and living-hybrid bioelectronic research.

## Project Goals

- Build a stable communication system between Raspberry Pi Pico 2 W and Raspberry Pi 5
- Acquire and visualize biological or simulated signals in real time
- Apply digital signal processing such as filtering and FFT
- Store and analyze signal data
- Apply machine learning using PyTorch
- Implement closed-loop feedback control
- Explore future expansion toward neural signal processing and living-hybrid systems

## System Architecture

Biological Signal / Sensor  
↓  
Analog Front End  
↓  
ADC  
↓  
Raspberry Pi Pico 2 W  
↓  
USB / UART  
↓  
Raspberry Pi 5  
↓  
Signal Processing  
↓  
Visualization / Data Logging / Machine Learning  
↓  
Decision  
↓  
Feedback Control  

## Hardware

### Main Platform

- Raspberry Pi 5 4GB
- Raspberry Pi Pico 2 W with Header

### Prototyping Components

- Breadboard
- Jumper wires
- Resistor kit
- USB data cable

### Planned Hardware

- External ADC
- Biosignal analog front-end
- EMG sensor
- ECG sensor
- Additional bioelectronic sensors

## Software

- Raspberry Pi OS
- Python
- MicroPython
- NumPy
- SciPy
- Matplotlib
- PySerial
- PyTorch
- Jupyter Notebook
- Git
- GitHub

## Project Roadmap

### Phase 0 - Project Setup

- [x] Create local project repository
- [x] Initialize Git
- [x] Connect local repository to GitHub
- [x] Create initial project structure
- [x] Create README

### Phase 1 - Pico to Raspberry Pi Communication

- [ ] Set up Raspberry Pi Pico 2 W
- [ ] Generate simulated biosignal data
- [ ] Send data through USB serial
- [ ] Receive data on Raspberry Pi 5
- [ ] Visualize the signal in real time

### Phase 2 - Signal Acquisition

- [ ] Read analog signals
- [ ] Add an external ADC
- [ ] Acquire real sensor data
- [ ] Save recorded data

### Phase 3 - Signal Processing

- [ ] Digital filtering
- [ ] FFT analysis
- [ ] Feature extraction
- [ ] Noise analysis

### Phase 4 - Machine Learning

- [ ] Prepare a biosignal dataset
- [ ] Build a PyTorch model
- [ ] Train a 1D CNN-based signal classifier
- [ ] Evaluate the model
- [ ] Run inference on Raspberry Pi 5

### Phase 5 - Closed-Loop Control

- [ ] Detect signal state
- [ ] Generate feedback commands
- [ ] Send commands to Raspberry Pi Pico 2 W
- [ ] Control an external device

## Future Research Direction

Future development may include:

- Neural spike detection
- Neural signal classification
- Multi-channel biosignal acquisition
- MEA-compatible signal processing
- Neural decoding
- Closed-loop neural interfaces
- Living-hybrid bioelectronic systems

## Repository Structure

BioLoop-Pi/

- README.md
- .gitignore
- pico/
- raspberry_pi/
- notebooks/
- data/
- docs/
  - devlog/
  - images/

## Current Status

Current phase: **Phase 0 - Project Setup**

Next milestone:

**Generate simulated biological signal data on Raspberry Pi Pico 2 W and visualize it in real time on Raspberry Pi 5.**

## License

License information will be added later.
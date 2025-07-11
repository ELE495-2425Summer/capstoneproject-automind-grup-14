# TOBB ETÜ ELE495 - Capstone Project

# Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Acknowledgements](#acknowledgements)

## Introduction
This capstone project aims to develop a voice-controlled autonomous ground vehicle using Raspberry Pi 5. The system is designed to understand and execute natural spoken commands in Turkish, enabling hands-free interaction with the vehicle.

Voice input is captured via a Bluetooth microphone and transcribed using OpenAI Whisper. The resulting text is processed by a language model to extract command logic in JSON format, which is then used to control the vehicle’s movement through motor drivers.

The vehicle also includes an RFID-based authentication system to ensure only authorized users can operate it. A custom Flutter-based mobile application communicates with a Flask backend running on the Raspberry Pi, allowing users to monitor and manage the system remotely.

This project demonstrates the integration of speech recognition, natural language processing, embedded control systems, and mobile app development to create a fully autonomous and voice-interactive robotic platform.

## Features
List the key features and functionalities of the project.
- Hardware: The hardware components used (should be listed with links)
- Operating System and packages
- Applications 
- Services

Key Functionalities
Voice-Controlled Autonomy: The vehicle receives and processes Turkish voice commands to perform autonomous navigation tasks without manual input.
User Authentication via RFID: Only authorized users can operate the vehicle through RFID card validation.
Real-Time Mobile App Interface: Users can monitor vehicle status, command execution, and log messages via a Flutter-based mobile app.
Command Understanding via LLM: Natural language commands are interpreted and converted into actionable JSON structures by a language model.
Obstacle Detection and Avoidance: Ultrasonic sensor ensures safe navigation by detecting and reacting to nearby obstacles.
Direction-Aware Turning: Integrated gyroscope (MPU-6050) enables accurate rotational control during turns.

Hardware Components
Raspberry Pi 5 – The main processing unit.
Bluetooth Microphone – For wireless audio input.
MPU-6050 Gyroscope – For detecting angular movement and orientation.
HC-SR04 Ultrasonic Sensor – For distance measurement and obstacle detection.
L298N Motor Driver – Controls the vehicle's DC motors.
RC522 RFID Reader + Tags – Used for verifying authorized users.
DC Geared Motors – Enable forward/backward movement and turning.
Power Supply (12V Battery + 5V Regulator) – Powers all onboard components.
microSD Card – For OS and software storage.

Operating System & Packages
OS: Raspberry Pi OS (Bookworm)
Programming Language: Python 3.11
Key Python Libraries:
openai – For Whisper and GPT API access
sounddevice, scipy, ffmpeg – For audio recording and processing
speechbrain, resemblyzer – For speaker verification
RPi.GPIO, gpiozero – For motor and sensor control
flask, requests – For API and mobile interface
pyserial – For UART communication with RFID module

Applications
Voice-Based Vehicle Control: Enables hands-free vehicle operation using natural spoken commands.
Access Restriction via RFID: Prevents unauthorized use by requiring RFID authentication.
Mobile Monitoring App: Shows real-time system state, sensor logs, and command execution feedback.
Autonomous Driving Logic: Uses LLM output to control movement based on conditions (e.g., “move forward until obstacle”).

Services
Speech Recognition Service: Converts live recorded audio to text using OpenAI Whisper.
Command Parsing Engine: Converts text commands into structured JSON control instructions using GPT-4.
Real-Time Flask API: Handles mobile app communication for sending/receiving commands and monitoring status.
Voice Feedback: Generates real-time spoken feedback using OpenAI TTS ("Nova" voice).
Speaker Verification: Ensures only known users can give commands using embedding-based audio comparison.

## Installation
Describe the steps required to install and set up the project. Include any prerequisites, dependencies, and commands needed to get the project running.

```bash
# Example commands
git clone https://github.com/username/project-name.git
cd project-name
```

## Usage
Provide instructions and examples on how to use the project. Include code snippets or screenshots where applicable.

## Screenshots
Include screenshots of the project in action to give a visual representation of its functionality. You can also add videos of running project to YouTube and give a reference to it here. 

## Acknowledgements
Give credit to those who have contributed to the project or provided inspiration. Include links to any resources or tools used in the project.

[Contributor 1](https://github.com/user1)
[Resource or Tool](https://www.nvidia.com)

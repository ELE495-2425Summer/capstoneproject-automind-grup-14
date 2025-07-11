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
1) Key Functionalities
    - Voice-Controlled Autonomy: The vehicle receives and processes Turkish voice commands to perform autonomous navigation tasks without manual input.
    - User Authentication via RFID: Only authorized users can operate the vehicle through RFID card validation.
    - Real-Time Mobile App Interface: Users can monitor vehicle status, command execution, and log messages via a Flutter-based mobile app.
    - Command Understanding via LLM: Natural language commands are interpreted and converted into actionable JSON structures by a language model.
    - Obstacle Detection and Avoidance: Ultrasonic sensor ensures safe navigation by detecting and reacting to nearby obstacles.
    - Direction-Aware Turning: Integrated gyroscope (MPU-6050) enables accurate rotational control during turns.

2) Hardware Components
    - Raspberry Pi 5 – The main processing unit.
    - Bluetooth Microphone – For wireless audio input.
    - MPU-6050 Gyroscope – For detecting angular movement and orientation.
    - HC-SR04 Ultrasonic Sensor – For distance measurement and obstacle detection.
    - L298N Motor Driver – Controls the vehicle's DC motors.
    - RC522 RFID Reader + Tags – Used for verifying authorized users.
    - DC Geared Motors – Enable forward/backward movement and turning.
    - Power Supply (12V Battery + 5V Regulator) – Powers all onboard components.
    - microSD Card – For OS and software storage.

3) Operating System & Packages
    - OS: Raspberry Pi OS (Bookworm)
    - Programming Language: Python 3.11
    - Key Python Libraries:
        - openai – For Whisper and GPT API access
        - sounddevice, scipy, ffmpeg – For audio recording and processing
        - speechbrain, resemblyzer – For speaker verification
        - RPi.GPIO, gpiozero – For motor and sensor control
        - flask, requests – For API and mobile interface
        - pyserial – For UART communication with RFID module

4) Applications
    - Voice-Based Vehicle Control: Enables hands-free vehicle operation using natural spoken commands.
    - Access Restriction via RFID: Prevents unauthorized use by requiring RFID authentication.
    - Mobile Monitoring App: Shows real-time system state, sensor logs, and command execution feedback.
    - Autonomous Driving Logic: Uses LLM output to control movement based on conditions (e.g., “move forward until obstacle”).

5) Services
    - Speech Recognition Service: Converts live recorded audio to text using OpenAI Whisper.
    - Command Parsing Engine: Converts text commands into structured JSON control instructions using GPT-4.
    - Real-Time Flask API: Handles mobile app communication for sending/receiving commands and monitoring status.
    - Voice Feedback: Generates real-time spoken feedback using OpenAI TTS ("Nova" voice).
    - Speaker Verification: Ensures only known users can give commands using embedding-based audio comparison.

## Installation
1) Prerequisites
    - Raspberry Pi 5 (with internet access)
    - Raspberry Pi OS (Bookworm 64-bit) installed and bootable on a microSD card
    - SSH access or monitor + keyboard setup
    - Internet connection for package installations
    - A verified OpenAI API key
    - Android device with the mobile app (for remote control)

2) Hardware Connections
- Connect the following modules to the Raspberry Pi as per your wiring plan:
    - L298N Motor Driver: Connect ENA, ENB, IN1–IN4 to GPIO pins (e.g., 12, 13, 17, 18, 22, 23)
    - HC-SR04 Ultrasonic Sensor: Connect Trig and Echo to GPIO (e.g., GPIO5, GPIO6)
    - MPU-6050 Gyroscope: Connect to I2C pins (SDA = GPIO2, SCL = GPIO3)
    - RC522 RFID Reader: Connect via UART (e.g., GPIO14 TX, GPIO15 RX)
    - Bluetooth Microphone: Pair over Bluetooth via the GUI or bluetoothctl
    - Power Supply: 12V battery (L298N) + 5V step-down for Raspberry Pi
    > Ensure GPIOs are protected with voltage dividers, zener diodes, or opto-isolators if needed.

3) Software Setup
    1. Update System & Install Git
        ```bash
        sudo apt update
        sudo apt upgrade -y
        sudo apt install git python3-pip python3-venv -y
        ```
    2. Clone the Repository
        ```bash
        git clone https://github.com/ELE495-2425Summer/capstoneproject-automind-grup-14.git
        cd capstoneproject-automind-grup-14
        ```
    3. Create Virtual Environment (Optional but Recommended)
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    4. Install Python Dependencies
        ```bash
        pip install -r requirements.txt
        ```
    Alternatif olarak manuel yüklemek için:
        ```bash
        pip install openai flask sounddevice scipy numpy RPi.GPIO gpiozero pyserial speechbrain
        ```
        > ffmpeg paketinin sistemde kurulu olması gerekir. Kurulum:
        ```bash
        sudo apt install ffmpeg"
        ```

4) Folder Structure
    - capstoneproject-automind-grup-14/
    <mic_test.py                # Microphone test script
    <speech_to_text.py          # Whisper-based voice transcription
    <motor_surucu.py            # Motor control logic
    <openai_tts.py              # Voice feedback generation using TTS
    <server.py                  # Flask backend server
    <kayit_al.py                # Live audio recording script
    <canli_kayit_ve_tanima.py   # Live speaker verification
    <authorized_uids.txt        # RFID authentication list
    <requirements.txt           # Dependency list

5) Running the Project
    1. Start the Flask server on Raspberry Pi:
        ```bash
        python3 server.py
        ```
    < (Optional) Run the live recording + verification daemon:
        ```bash
        python3 canli_kayit_ve_tanima.py
        ```
    > On the mobile app, send commands or start recording.
        canli_kayit_ve_tanima.py will only activate if a valid RFID card was scanned and written to arac_durum.txt.

6) First-Time Setup Notes
    - Bluetooth Microphone: Pair using GUI or bluetoothctl.
    - RFID Setup: The Raspberry Pi must be connected to the RFID module via UART. kayit_al.py will detect and log authorized UID cards.
    - API Key Setup: Ensure OpenAI API key is defined in your Python scripts or environment.
        openai.api_key = "sk-..."

Additional Notes
All voice interactions are in Turkish.

Whisper API is used online, so stable internet is required.

Output logs are written to server_log.txt.

Animations and vehicle status are reflected in the Flutter-based mobile app.

## Usage
Provide instructions and examples on how to use the project. Include code snippets or screenshots where applicable.

## Screenshots
Include screenshots of the project in action to give a visual representation of its functionality. You can also add videos of running project to YouTube and give a reference to it here. 

## Acknowledgements
Give credit to those who have contributed to the project or provided inspiration. Include links to any resources or tools used in the project.

[Contributor 1](https://github.com/user1)
[Resource or Tool](https://www.nvidia.com)

# ISHI Technology - AI Assistant

ISHI is an AI-powered virtual assistant built using Python and PyQt5. It provides a graphical user interface (GUI) and supports voice commands for various tasks such as searching the web, controlling system volume, telling jokes, and more. The project also includes face recognition for secure login.

---

## Features

1. **Voice Commands**:
   - Control system volume (increase, decrease, mute).
   - Open websites like Google, Facebook, Instagram, etc.
   - Tell jokes using the `pyjokes` library.
   - Search Wikipedia for information.
   - Take screenshots.
   - Detect clap sounds to trigger actions.

2. **Face Recognition**:
   - Secure login using face recognition.
   - Recognizes multiple users and grants access based on stored images.

3. **Graphical User Interface (GUI)**:
   - Interactive and visually appealing UI built with PyQt5.
   - Dynamic animations for different states (listening, speaking, loading, sleeping).

4. **File Search**:
   - Search for files across multiple drives.
   - Open files directly from the search results.

5. **Sleep Mode**:
   - The assistant can enter sleep mode and wake up on command.

---

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.7 or higher**
- Required Python packages (see below for versions).

---

## Required Packages and Versions

Here are the required Python packages and their versions for this project:

| Package            | Version  | Installation Command                     |
|--------------------|----------|------------------------------------------|
| PyQt5              | 5.15.9   | `pip install PyQt5==5.15.9`              |
| SpeechRecognition  | 3.8.1    | `pip install SpeechRecognition==3.8.1`   |
| pyttsx3            | 2.90     | `pip install pyttsx3==2.90`              |
| pyautogui          | 0.9.53   | `pip install pyautogui==0.9.53`          |
| wikipedia          | 1.4.0    | `pip install wikipedia==1.4.0`           |
| pyjokes            | 0.6.0    | `pip install pyjokes==0.6.0`             |
| numpy              | 1.21.5   | `pip install numpy==1.21.5`              |
| sounddevice        | 0.4.4    | `pip install sounddevice==0.4.4`         |
| face_recognition   | 1.3.0    | `pip install face_recognition==1.3.0`    |
| opencv-python      | 4.5.5.64 | `pip install opencv-python==4.5.5.64`    |

You can install all the required packages using the following command:

```bash
pip install PyQt5==5.15.9 SpeechRecognition==3.8.1 pyttsx3==2.90 pyautogui==0.9.53 wikipedia==1.4.0 pyjokes==0.6.0 numpy==1.21.5 sounddevice==0.4.4 face_recognition==1.3.0 opencv-python==4.5.5.64
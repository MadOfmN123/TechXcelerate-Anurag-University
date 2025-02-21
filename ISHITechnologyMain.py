import sys
import os
import random
import pyttsx3
import datetime
import time
import pyautogui
import pywhatkit
import subprocess
import wikipedia
import pyjokes
import pyaudio
import webbrowser
import speech_recognition as sr
from datetime import datetime
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import QtGui
from ISHIMainGUI import Ui_Widget
from time import sleep
import requests
import json
from urllib.parse import quote

# Initialize Text-to-Speech Engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
for voice in voices:
    if "Zira" in voice.name or "Hazel" in voice.name:
        female_voice = voice
        break
if female_voice:
    engine.setProperty('voice', female_voice.id)
    print(f"Using voice: {female_voice.name}")
else:
    print("Female voice not found!")

# Add Sarvam API configuration
SARVAM_API_KEY = "19890b1a-e83d-4d82-b753-39946232dda4"
SARVAM_ENDPOINT = "https://api.sarvam.ai/v1/transcribe"

def speak(audio):
    """Speak with animation transitions"""
    ui.updateMovieDynamically("loading")
    QThread.msleep(500)  # Short delay before speaking
    ui.updateMovieDynamically("speaking")
    engine.say(audio)
    engine.runAndWait()
    QThread.msleep(300)  # Short delay after speaking
    ui.updateMovieDynamically("listening")

def wishings():
    ui.updateMovieDynamically("speaking")
    hour = int(datetime.now().hour)
    if hour < 12:
        greeting = "GOOD MORNING BOSS"
    elif hour < 17:
        greeting = "GOOD AFTERNOON BOSS"
    elif hour < 21:
        greeting = "GOOD EVENING BOSS"
    else:
        greeting = "GOOD NIGHT BOSS"
    print(f"ISHI: {greeting}")
    speak(greeting)

def query_mistral(prompt):
    """Sends a prompt to Mistral AI model and returns the response."""
    try:
        command = f'ollama run mistral "{prompt}"'
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=True
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception as e:
        print(f"Error querying Mistral AI: {e}")
        return None

def transcribe_with_sarvam(audio_data):
    """Transcribe audio using Sarvam API"""
    try:
        headers = {
            "Authorization": f"Bearer {SARVAM_API_KEY}",
            "Content-Type": "multipart/form-data"
        }
        
        # Create files payload with audio data
        files = {
            'audio_file': ('audio.wav', audio_data, 'audio/wav')
        }
        
        # Create form data
        data = {
            "language": "te-en",  # Telugu-English mixed language
            "task": "transcribe"
        }
        
        response = requests.post(SARVAM_ENDPOINT, headers=headers, files=files, data=data)
        if response.status_code == 200:
            result = response.json()
            return result.get('text', '')
        else:
            print(f"Sarvam API error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error in Sarvam transcription: {e}")
        return None

def get_voice_input():
    """Captures voice input with animation states and Sarvam transcription"""
    ui.updateMovieDynamically("listening")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 1.5
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Waiting for your command...")
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing...")
            ui.updateMovieDynamically("loading")
            
            # Try Sarvam API first for Tenglish recognition
            audio_data = audio.get_wav_data()  # Get audio data in WAV format
            sarvam_result = transcribe_with_sarvam(audio_data)
            
            if sarvam_result:
                print("Sarvam transcription:", sarvam_result)
                return sarvam_result.lower()
            else:
                # Fallback to Google Speech Recognition
                result = recognizer.recognize_google(audio, language='en-in').lower()
                print("Google transcription:", result)
                return result
                
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            ui.updateMovieDynamically("sleeping")
            QThread.msleep(1000)
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Listening error: {e}")
        return None

def open_application(app_name):
    """Opens specified application."""
    try:
        if app_name.lower() == "chrome":
            subprocess.run(["start", "chrome"], shell=True)  # Windows
        else:
            print(f"Opening {app_name} is not supported.")
    except Exception as e:
        print(f"Error opening {app_name}: {e}")

def play_youtube_video(query):
    """Opens YouTube with the given query."""
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)
    speak(f"Playing {query} on YouTube.")

class IshiMainClass(QThread):
    def run(self):
        try:
            # Start with sleeping state
            ui.updateMovieDynamically("sleeping")
            QThread.msleep(1000)
            self.commands()
        except Exception as e:
            print(f"Error in IshiMainClass: {e}")

    def commands(self):
        wishings()
        while True:
            user_query = get_voice_input()
            if not user_query:
                ui.updateMovieDynamically("sleeping")
                QThread.msleep(1000)
                continue

            # Show loading state while processing
            ui.updateMovieDynamically("loading")
            QThread.msleep(500)

            if "exit" in user_query or "quit" in user_query:
                print("Exiting. Goodbye!")
                speak("Goodbye!")
                break

            
            elif "what is your name" in user_query:
                speak("I am ISHI (INTELLEGENT SYSTEM HIGH INTERACTIVE TECHNOLOGY), I am Assist You You Can Call Me Ishi")


            elif "what is the time" in user_query:
                current_time = datetime.now().strftime("%H:%M:%S")
                response = f"The current time is {current_time}."
                print(response)
                speak(response)

            elif "open youtube and play" in user_query:
                video_query = user_query.replace("open youtube and play", "").strip()
                play_youtube_video(video_query)

            elif "open" in user_query:
                app_name = user_query.replace("open", "").strip()
                open_application(app_name)

            # Add Tenglish command handling
            elif "namaste" in user_query or "namaskar" in user_query:
                speak("Namaste! How can I help you today?")
                
            elif "ela unnavu" in user_query:  # Telugu: How are you?
                speak("I am doing well, thank you! How can I assist you?")
                
            elif "nee peru enti" in user_query:  # Telugu: What is your name?
                speak("My name is Ishi, I am your AI assistant")

            else:
                ui.updateMovieDynamically("loading")
                response = query_mistral(user_query)
                if response:
                    print("Mistral AI:", response)
                    speak(response)
                else:
                    print("No response from AI.")
                    speak("I'm sorry, I couldn't process that request.")


class Ui_ISHI(QMainWindow):
    def __init__(self):
        super(Ui_ISHI, self).__init__()
        self.IshiUI = Ui_Widget()
        self.IshiUI.setupUi(self)
        self.runAllMovies()
        
        # Initialize with sleeping state
        QTimer.singleShot(500, lambda: self.updateMovieDynamically("sleeping"))

    def updateMovieDynamically(self, state):
        # Hide all animations first
        animations = {
            "talking": self.IshiUI.Talking,
            "loading": self.IshiUI.reload,
            "listening": self.IshiUI.listing,
            "sleeping": self.IshiUI.reload_2
        }
        
        for anim in animations.values():
            anim.hide()

        # Show and raise the requested animation
        if state in animations:
            animations[state].raise_()
            animations[state].show()

        # Process events to ensure smooth transitions
        QApplication.processEvents()

    def runAllMovies(self):
        self.IshiUI.codingMovie = QtGui.QMovie("C:\\Users\\tarak\\Downloads\\AKK-main\\AKK-main\\IMAGES\\G.U.I Material\\ExtraGui\\B.G_Template_1.gif")


        self.IshiUI.label_4.setMovie(self.IshiUI.codingMovie)
        self.IshiUI.codingMovie.start()

        self.IshiUI.circleMovie = QtGui.QMovie("C:\\Users\\tarak\\Downloads\\AKK-main\\AKK-main\\IMAGES\\ani1.gif")
        self.IshiUI.label_3.setMovie(self.IshiUI.circleMovie)
        self.IshiUI.circleMovie.start()

        self.IshiUI.talkingMovie = QtGui.QMovie("C:\\Users\\tarak\\Downloads\\AKK-main\\AKK-main\\IMAGES\\G.U.I Material\\VoiceReg\\Siri_1.gif")
        self.IshiUI.Talking.setMovie(self.IshiUI.talkingMovie)
        self.IshiUI.talkingMovie.start()

        self.IshiUI.loadingMovie = QtGui.QMovie("C:\\Users\\tarak\\Downloads\\AKK-main\\AKK-main\\IMAGES\\G.U.I Material\\VoiceReg\\Qualt.gif")
        self.IshiUI.reload.setMovie(self.IshiUI.loadingMovie)
        self.IshiUI.loadingMovie.start()

        self.IshiUI.listingMovie = QtGui.QMovie("C:\\Users\\tarak\\Downloads\\AKK-main\\AKK-main\\IMAGES\\ani2.gif")
        self.IshiUI.listing.setMovie(self.IshiUI.listingMovie)
        self.IshiUI.listingMovie.start()

        self.IshiUI.sleepingMovie = QtGui.QMovie("C:\\Users\\tarak\\Downloads\\AKK-main\\AKK-main\\IMAGES\\ani3.gif")
        self.IshiUI.reload_2.setMovie(self.IshiUI.sleepingMovie)
        self.IshiUI.sleepingMovie.start()


if __name__ == '__main__':
    print("Starting GUI...")
    app = QApplication(sys.argv)
    ui = Ui_ISHI()
    ui.show()

    # Start voice assistant thread after UI is initialized
    startExecution = IshiMainClass()
    startExecution.start()

    sys.exit(app.exec_())
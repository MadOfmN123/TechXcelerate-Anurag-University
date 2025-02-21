import sys
import os
import random
import pyttsx3
import datetime
import time
import pyautogui
import wikipedia
import pyjokes
import pyaudio
import webbrowser
from time import sleep
from PyQt5.QtCore import QThread
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui
from ISHIMainGUI import Ui_Widget
import sounddevice as sd
import numpy as np

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

def replace_dot(text):
    return text.replace(" dot ", ".")
    output_text = replace_dot(input_text)
# File search function with improved logging
def search_file(file_name):
    drives = ['C:\\', 'D:\\', 'E:\\']  # List of drives to search
    found_locations = []

    for drive in drives:
        print(f"Searching in drive: {drive}")  # Log the drive being searched
        for root, dirs, files in os.walk(drive):
            if file_name.lower() in [file.lower() for file in files]:  # Case-insensitive search
                found_locations.append(os.path.join(root, file_name))
                print(f"File found at: {os.path.join(root, file_name)}")  # Log the file location

    if not found_locations:
        print(f"File '{file_name}' not found.")  # Log if no file is found
    return found_locations


def detect_clap(threshold=3000):
    """
    Detects a clap sound based on amplitude threshold.
    """
    duration = 1  # Duration to listen in seconds
    fs = 44100  # Sampling frequency
    try:
        # Record sound for the given duration
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until the recording is complete
        amplitude = np.max(np.abs(recording))  # Get max amplitude
        if amplitude > threshold:
            print("Clap detected!")
            return True
        else:
            return False
    except Exception as e:
        print("Error in clap detection:", e)
        return False


def speak(audio):
    ui.updateMovieDynamically("speaking")
    engine.say(audio)
    engine.runAndWait()


def wishings():
    ui.updateMovieDynamically("speaking")
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("ISHI : GOOD MORNING BOSS")
        speak("GOOD MORNING BOSS")
    elif hour >= 12 and hour < 17:
        print("ISHI : GOOD AFTERNOON BOSS")
        speak("GOOD AFTERNOON BOSS")
    elif hour >= 17 and hour < 21:
        print("ISHI : GOOD EVENING BOSS")
        speak("GOOD EVENING BOSS")
    else:
        print("ISHI : GOOD NIGHT BOSS")
        speak("GOOD NIGHT BOSS")


class ishiCodingClass(QThread):
    def __init__(self):
        super(ishiCodingClass, self).__init__()

    def run(self):
        self.executeISHI()

    def filterTheQueryForSpecificWord(self, queryToBeFiltered):
        queryToBeFiltered = queryToBeFiltered.replace("Ishi", '').replace("ishi", '')
        query = queryToBeFiltered.replace("hey", '').replace("can", '').replace("please", '').replace("bro", '')
        query = query.replace("baby", '').replace("jarvy", '').replace("ok", '').replace("now", '')
        query = query.replace("you", '').replace("no", '').replace("the", '').replace("to", '').replace("do",
                                                                                                        '').replace(
            "this", '')
        return query

    def wakeupCommands(self):
        ui.updateMovieDynamically("sleeping")
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source)
            try:
                query = r.recognize_google(audio, language='en-in')
            except:
                query = "none"
            if "wake up" in query:
                break


class ishiMainClass(QThread):
    def __init__(self):
        super(ishiMainClass, self).__init__()
        self.found_locations = None
        self.sleep_mode = False

    def run(self):
        self.runIshi()

    def open_location(self):
        try:
            # Extract the location number from the command
            command_parts = self.query.split()
            if len(command_parts) > 2 and command_parts[2].isdigit():
                location_number = int(command_parts[2]) - 1  # Convert to zero-based index

                if 0 <= location_number < len(self.found_locations):
                    location = self.found_locations[location_number]
                    print(f"Opening location: {location}")
                    speak(f"Opening location: {location}")
                    os.startfile(location)  # Open the file location
                else:
                    speak(f"There is no location number {command_parts[2]}. Please view properly.")
            else:
                speak("Please specify a valid location number.")
        except Exception as e:
            print("Error in opening location:", e)
            speak("There was an error in opening the location.")

    def commands(self):
        if self.sleep_mode:
            # Listen for the "wake up" command when in sleep mode
            print("In sleep mode. Waiting for 'wake up' command...")
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    audio = r.listen(source)
                try:
                    cmd = r.recognize_google(audio, language='en-in').lower()
                    if "wake up" in cmd:
                        self.sleep_mode = False
                        print("Waking up...")
                        speak("Hello sir, how can I assist you?")
                        return "wake up"
                except Exception as e:
                    continue
        else:
            ui.updateMovieDynamically("listening")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.pause_threshold = 1
                audio = r.listen(source)
            try:
                ui.updateMovieDynamically("loading")
                print("Wait for a few moments...")
                cmd = r.recognize_google(audio, language='en-in')
                cmd = cmd.lower().replace(" dot ", ".")
                print(f"You just said: {cmd}\n")
            except Exception as e:
                print(e)
                speak("Please repeat again")
                cmd = "none"
            return cmd

    def runIshi(self):
        wishings()

        while True:
            # Check for clap if not in sleep mode
            if not self.sleep_mode and detect_clap():
                print("System is going to sleep...")
                speak("Going to sleep, sir")
                self.sleep_mode = True
                ui.updateMovieDynamically("sleeping")
                continue

            self.query = self.commands().lower()

            if 'time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")

            elif ("volume up" in self.query) or ("increase volume" in self.query):
                pyautogui.press("volumeup")
                speak("Volume increased")
            elif ("volume down" in self.query) or ("decrease volume" in self.query):
                pyautogui.press("volumedown")
                speak("Volume decrease")
            elif ("volume mute" in self.query) or ("mute the sound" in self.query):
                pyautogui.press("volumemute")
                speak("Volume muted")

            elif "to sleep" in self.query:
                speak("Going to sleep, sir")
                self.sleep_mode = True
                ui.updateMovieDynamically("sleeping")

            elif 'hello' in self.query:
                speak("Hello sir, how are you?")

            elif 'i am fine' in self.query:
                speak("That's great, sir")
                speak("Sir, how can I help you?")

            elif 'how are you' in self.query:
                speak("Perfect, sir")
                speak("Sir, how can I help you?")

            elif 'thank you' in self.query:
                speak("You are welcome, sir")
                speak("Sir, how can I help you?")

            elif 'namaste' in self.query:
                speak("Namaste sir, Alaa Vunnaru")

            elif 'screenshot' in self.query or 'screen shot' in self.query:
                pyautogui.hotkey('win', 'alt', 'prtsc')
                speak("Screenshot saved, sir")

            elif 'open google' in self.query:
                speak("Opening Google, sir...")
                webbrowser.open("https://www.google.com")

            elif 'open facebook' in self.query:
                speak("Opening facebook, sir...")
                webbrowser.open("https://www.facebook.com")

            elif 'open instagram' in self.query:
                speak("Opening instagram, sir...")
                webbrowser.open("https://www.instagram.com")

            elif 'open discord' in self.query:
                speak("Opening discord, sir...")
                webbrowser.open("https://www.discord.com")

            elif 'open whatsapp' in self.query:
                speak("Opening whatsapp, sir...")
                webbrowser.open("https://web.whatsapp.com")

            elif 'who are you' in self.query:
                speak("Hi Sir, I am Ishi, I am invented by team titan's")

            elif 'hu r u' in self.query:
                speak("Hi Sir, I am Ishi, I am invented by team titan's")

            elif "wikipedia" in self.query:
                speak("Searching in Wikipedia...")
                try:
                    self.query = self.query.replace("wikipedia", "")
                    result = wikipedia.summary(self.query, sentences=1)
                    speak("According to Wikipedia...")
                    print(result)
                    speak(result)
                except:
                    speak("No result found, sir...")

            elif 'joke' in self.query:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)

            elif 'exit program' in self.query:
                speak("Bye, sir...")
                os.close()

            elif "search the" in self.query:
                file_name = self.query.replace("search the", "").strip()
                results = search_file(file_name)
                if results:
                    speak(f"File '{file_name}' found at the following locations:")
                    print("\n".join(results))
                    speak("\n".join(results))
                else:
                    speak(f"File '{file_name}' not found in the specified drives.")

            


startExecution = ishiMainClass()


class Ui_ISHI(QMainWindow):
    def __init__(self):
        super(Ui_ISHI, self).__init__()
        self.IshiUI = Ui_Widget()
        self.IshiUI.setupUi(self)

        self.runAllMovies()

    def updateMovieDynamically(self, state):
        if state == "speaking":
            self.IshiUI.Talking.raise_()
            self.IshiUI.Talking.show()
            self.IshiUI.reload.hide()
            self.IshiUI.listing.hide()
            self.IshiUI.reload_2.hide()

        if state == "listening":
            self.IshiUI.Talking.hide()
            self.IshiUI.reload.hide()
            self.IshiUI.listing.raise_()
            self.IshiUI.listing.show()
            self.IshiUI.reload_2.hide()

        if state == "loading":
            self.IshiUI.Talking.hide()
            self.IshiUI.reload.raise_()
            self.IshiUI.reload.show()
            self.IshiUI.listing.hide()
            self.IshiUI.reload_2.hide()

        if state == "sleeping":
            self.IshiUI.Talking.hide()
            self.IshiUI.reload.hide()
            self.IshiUI.listing.hide()
            self.IshiUI.reload_2.raise_()
            self.IshiUI.reload_2.show()

    def runAllMovies(self):
        try:
            # Store movie paths in variables for easier management
            bg_path = "C:\\Users\\tarak\\Downloads\\AKK-main\\AKK-main\\IMAGES\\G.U.I Material\\ExtraGui\\B.G_Template_1.gif"
            circle_path = "C:\\Users\\tarak\\Downloads\\AKK-main\\AKK-main\\IMAGES\\ani1.gif"
            talking_path = "C:\\Users\\tarak\\Downloads\\AKK-main\\AKK-main\\IMAGES\\G.U.I Material\\VoiceReg\\Siri_1.gif"
            loading_path = "C:\\Users\\tarak\\Downloads\\AKK-main\\AKK-main\\IMAGES\\G.U.I Material\\loadScreen.gif"
            listening_path = "C:\\Users\\tarak\\Downloads\\AKK-main\\AKK-main\\IMAGES\\G.U.I Material\\speakSpeech.gif"
            sleeping_path = "C:\\Users\\tarak\\Downloads\\AKK-main\\AKK-main\\IMAGES\\G.U.I Material\\Loading Sleep mode.gif"

            # Function to safely set up movie
            def setup_movie(path, label):
                if os.path.exists(path):
                    movie = QtGui.QMovie(path)
                    label.setMovie(movie)
                    movie.start()
                    return movie
                else:
                    print(f"Warning: Movie file not found: {path}")
                    return None

            # Set up all movies with error handling
            self.IshiUI.codingMovie = setup_movie(bg_path, self.IshiUI.label_4)
            self.IshiUI.circleMovie = setup_movie(circle_path, self.IshiUI.label_3)
            self.IshiUI.talkingMovie = setup_movie(talking_path, self.IshiUI.Talking)
            self.IshiUI.loadingMovie = setup_movie(loading_path, self.IshiUI.reload)
            self.IshiUI.listeningMovie = setup_movie(listening_path, self.IshiUI.listing)
            self.IshiUI.sleepingMovie = setup_movie(sleeping_path, self.IshiUI.reload_2)

        except Exception as e:
            print(f"Error setting up movies: {str(e)}")

        startExecution.start()

    def closeEvent(self, event):
        """Handle cleanup when the window is closed"""
        try:
            # Stop all movies
            movies = [
                self.IshiUI.codingMovie,
                self.IshiUI.circleMovie,
                self.IshiUI.talkingMovie,
                self.IshiUI.loadingMovie,
                self.IshiUI.listeningMovie,
                self.IshiUI.sleepingMovie
            ]

            for movie in movies:
                if movie is not None:
                    movie.stop()

            # Stop the execution thread
            if startExecution.isRunning():
                startExecution.terminate()
                startExecution.wait()

            event.accept()
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_ISHI()
    ui.show()
    sys.exit(app.exec_())
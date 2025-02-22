#runs offline and online
import subprocess
import webbrowser
import speech_recognition as sr
import pyttsx3
import requests
import json
import os
import sys
import socket
from datetime import datetime

# --- Check for Vosk availability for offline speech recognition ---
try:
    from vosk import Model, KaldiRecognizer
    import pyaudio
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False

# --- Global Mode Flag ---
ONLINE_MODE = True  # Will be set based on network check

# --- Set up Text-to-Speech Engine ---
def speak_text(text):
    """Converts text to speech using pyttsx3."""
    print(f"🔊 Speaking: {text}")
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"An error occurred while speaking: {e}")

# --- Network Check ---
def check_network():
    """Returns True if an internet connection is available, otherwise False."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

# --- Voice Input Functions ---
def get_voice_input_online():
    """Captures voice input using the Google Speech API (online mode)."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"🗣 You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("😕 Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        print(f"⚠️ Error connecting to Google Speech API: {e}")
        print("Switching to offline mode...")
        global ONLINE_MODE
        ONLINE_MODE = False  # Automatically switch to offline mode
        return get_voice_input_offline() if VOSK_AVAILABLE else None

    return None


def get_voice_input_offline():
    """Captures voice input using Vosk (offline mode)."""
    if not VOSK_AVAILABLE:
        print("⚠️ Vosk not available. Switching to online mode.")
        return get_voice_input_online()
    print("🎤 Say something (Offline Mode)...")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                    input=True, frames_per_buffer=8000)
    stream.start_stream()
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer_vosk.AcceptWaveform(data):
            result = json.loads(recognizer_vosk.Result())
            text = result.get("text", "")
            if text:
                print(f"🗣 You said: {text}")
                return text.lower()
            else:
                return None

def get_voice_input():
    """
    Uses online mode voice input if available; otherwise, falls back to offline mode.
    """
    if ONLINE_MODE:
        return get_voice_input_online()
    else:
        return get_voice_input_offline()

# --- Mistral Query Functions ---
def query_mistral_online(prompt):
    """Queries the Mistral AI API using the Mistral 7B model (online mode)."""
    api_key = "MiZl2nrcKmDvAKxFTh92eQQUTPgAejZP"  # Replace with your actual API key
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "open-mistral-7b",  # Using Mistral 7B
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        elif response.status_code == 401:
            return "Error: Unauthorized. Please check your Mistral API key."
        else:
            return f"Error: {response.status_code}, {response.text}"
    except requests.RequestException as e:
        return f"Error contacting Mistral API: {e}"

def query_mistral_offline(prompt):
    """Queries the locally installed Mistral model via Ollama (offline mode)."""
    command = f'ollama run mistral "{prompt}"'
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True
        )
        if result.returncode != 0:
            print("Error querying local Mistral:")
            print(result.stderr)
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"An error occurred while querying local Mistral: {e}")
        return None

# --- Command Processing ---
def process_command(command, online_mode):
    """
    Processes user commands:
      - "time", "date", "exit"/"quit" are handled locally.
      - In online mode, extra features (e.g., "open youtube") are available.
      - Otherwise, the command is forwarded to the appropriate Mistral query function.
    """
    if "time" in command:
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}."
    elif "date" in command:
        current_date = datetime.now().strftime("%Y-%m-%d")
        return f"Today's date is {current_date}."
    elif "exit" in command or "quit" in command:
        print("Exiting program. Goodbye!")
        speak_text("Goodbye!")
        sys.exit(0)
    else:
        if online_mode:
            if "open youtube on" in command and "play" in command:
                try:
                    parts = command.split("play")
                    browser_part = parts[0].strip()
                    video_part = parts[1].strip()
                    browser = browser_part.split("on")[-1].strip()
                    video_query = video_part
                    play_youtube_video(browser, video_query)
                    return "Opening YouTube..."
                except IndexError:
                    return "Sorry, I couldn't parse the command properly."
            elif "open" in command:
                app_name = command.split("open")[-1].strip()
                open_application(app_name)
                return f"Opening {app_name}."
            else:
                return query_mistral_online(command)
        else:
            # Offline mode: use local Mistral query; extra commands are not supported.
            return query_mistral_offline(command)

def open_application(app_name):
    """Opens the specified application (only in online mode)."""
    try:
        if app_name.lower() == "chrome":
            subprocess.run(["open", "-a", "Google Chrome"])  # macOS example
            # For Windows: subprocess.run(["start", "chrome"], shell=True)
            # For Linux: subprocess.run(["google-chrome"])
        else:
            print(f"Opening {app_name} is not supported in this script.")
    except Exception as e:
        print(f"An error occurred while opening {app_name}: {e}")

def play_youtube_video(browser, query):
    """Opens YouTube in the specified browser and plays a video (online mode only)."""
    try:
        search_query = query.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={search_query}"
        if browser.lower() == "chrome":
            webbrowser.get("chrome").open(url)
        else:
            print(f"Opening YouTube in {browser} is not supported.")
    except Exception as e:
        print(f"An error occurred while opening YouTube: {e}")

# --- Set Vosk Model Path ---
VOSK_MODEL_PATH = r"C:\\Users\\tarak\\OneDrive\\Desktop\\ishi1\\vosk-model-small-en-us-0.15\\vosk-model-small-en-us-0.15"
if VOSK_AVAILABLE and os.path.exists(VOSK_MODEL_PATH):
    vosk_model = Model(VOSK_MODEL_PATH)
    recognizer_vosk = KaldiRecognizer(vosk_model, 16000)
else:
    print("⚠️ Vosk model not found. Running only in online mode.")
    VOSK_AVAILABLE = False

# --- Main Program ---
if __name__ == "__main__":
    # Determine mode based on network connectivity
    ONLINE_MODE = check_network()
    if ONLINE_MODE:
        print("Entering online mode")
    else:
        print("Entering offline mode")
    
    print("Listening for voice commands... (Say 'exit' to quit)")
    run_count = 0
    while True:
        run_count += 1
        print(f"\nRun {run_count} - Awaiting user input...")
        voice_input = get_voice_input()
        if voice_input:
            response = process_command(voice_input, ONLINE_MODE)
            if response:
                print("Response:", response)
                speak_text(response)
        else:
            print("No voice input detected.")

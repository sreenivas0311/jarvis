import os
import json
import webbrowser
import pyttsx3
import psutil
import joblib
import pyaudio
from vosk import Model, KaldiRecognizer

# Optional external modules
try:
    from googletrans import Translator
    translator = Translator()
except:
    translator = None

try:
    import wikipedia
    wikipedia.set_lang("en")
except:
    wikipedia = None


# ----------------------------------------------------
# NLP MODEL
# ----------------------------------------------------
intent_model = joblib.load("intent_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def predict_intent(text):
    X = vectorizer.transform([text])
    return intent_model.predict(X)[0]


# ----------------------------------------------------
# TEXT TO SPEECH
# ----------------------------------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 175)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()


# ----------------------------------------------------
# MEMORY SYSTEM
# ----------------------------------------------------
MEMORY_FILE = "jarvis_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_memory(mem):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(mem, f, indent=2, ensure_ascii=False)
    except:
        pass

memory = load_memory()

def handle_memory(text):
    lower = text.lower()

    if lower.startswith("remember"):
        content = text[len("remember"):].strip()
        if not content:
            speak("What should I remember?")
            return True

        notes = memory.get("notes", [])
        notes.append(content)
        memory["notes"] = notes
        save_memory(memory)
        speak("I will remember that.")
        return True

    if "what do you remember" in lower:
        notes = memory.get("notes", [])
        if not notes:
            speak("I don't remember anything.")
        else:
            speak("You told me to remember these:")
            for n in notes:
                speak(n)
        return True

    return False


# ----------------------------------------------------
# APP CONTROL
# ----------------------------------------------------
def open_app(name):
    speak(f"Opening {name}")
    if name == "notepad":
        os.system("start notepad")
    elif name == "brave":
        os.system("start brave")
    elif name == "chrome":
        os.system("start chrome")
    elif name == "discord":
        os.system("start discord")
    else:
        speak("I cannot open that yet.")

def close_app(name):
    speak(f"Closing {name}")
    for p in psutil.process_iter(['name']):
        try:
            if name.lower() in p.info['name'].lower():
                p.kill()
        except:
            pass


# ----------------------------------------------------
# WEBSITE + SEARCH
# ----------------------------------------------------
def open_website(text):
    words = text.split()

    for w in words:
        if "." in w:
            webbrowser.open("https://" + w)
            return True

    sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "instagram": "https://www.instagram.com",
        "amazon": "https://www.amazon.in",
        "flipkart": "https://www.flipkart.com",
        "netflix": "https://www.netflix.com",
        "discord": "https://discord.com",
        "whatsapp": "https://web.whatsapp.com",
    }

    lower = text.lower()
    for k, v in sites.items():
        if k in lower:
            webbrowser.open(v)
            return True

    return False


def google_search(text):
    lower = text.lower().replace("google", "").replace("search", "")
    query = lower.strip()
    if not query:
        query = text
    speak("Searching Google")
    webbrowser.open("https://www.google.com/search?q=" + query.replace(" ", "+"))


def youtube_search(text):
    lower = text.lower().replace("youtube", "").replace("search", "")
    query = lower.strip()
    if not query:
        query = text
    speak("Searching YouTube")
    webbrowser.open("https://www.youtube.com/results?search_query=" + query.replace(" ", "+"))


def play_music(text):
    lower = text.lower().replace("play", "")
    if not lower:
        lower = "songs"
    speak("Playing music on YouTube")
    webbrowser.open("https://www.youtube.com/results?search_query=" + lower.replace(" ", "+"))


# ----------------------------------------------------
# TRANSLATION
# ----------------------------------------------------
def handle_translation(text):
    if translator is None:
        return False

    lower = text.lower()

    if "translate" not in lower:
        return False

    if "to hindi" in lower:
        dest = "hi"
        content = lower.split("to hindi")[0].replace("translate", "")
    elif "to tamil" in lower:
        dest = "ta"
        content = lower.split("to tamil")[0].replace("translate", "")
    elif "to telugu" in lower:
        dest = "te"
        content = lower.split("to telugu")[0].replace("translate", "")
    else:
        dest = "hi"
        content = lower.replace("translate", "")

    content = content.strip()

    if not content:
        speak("What should I translate?")
        return True

    try:
        result = translator.translate(content, dest=dest)
        speak("Translation: " + result.text)
    except:
        speak("Translation failed.")

    return True


# ----------------------------------------------------
# WIKIPEDIA
# ----------------------------------------------------
def handle_wikipedia(text):
    if wikipedia is None:
        return False

    lower = text.lower()
    if "wikipedia" not in lower:
        return False

    query = (lower.replace("wikipedia", "")
                 .replace("tell me about", "")
                 .replace("who is", "")
                 .replace("what is", "")
                 .strip())

    if not query:
        speak("What should I search on Wikipedia?")
        return True

    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except:
        speak("Couldn't fetch Wikipedia info.")

    return True


# ----------------------------------------------------
# TEXT MODE LOOP
# ----------------------------------------------------
def text_mode_loop():
    while True:
        text = input("\nType command: ").strip().lower()
        if not text:
            continue

        if text in ["exit", "quit", "back"]:
            speak("Exiting text mode.")
            return  # goes back to mode menu

        if handle_memory(text): continue
        if handle_translation(text): continue
        if handle_wikipedia(text): continue

        intent = predict_intent(text)
        print("Intent:", intent)

        if intent == "open_app":
            if "notepad" in text: open_app("notepad")
            elif "chrome" in text: open_app("chrome")
            elif "brave" in text: open_app("brave")
            elif "discord" in text: open_app("discord")
            else: speak("Which app?")
            continue

        if intent == "close_app":
            if "notepad" in text: close_app("notepad")
            elif "chrome" in text: close_app("chrome")
            elif "brave" in text: close_app("brave")
            elif "discord" in text: close_app("discord")
            else: speak("Which app?")
            continue

        if intent == "open_website":
            if open_website(text): speak("Opening website")
            else: speak("Website not found.")
            continue

        if intent == "google_search":
            google_search(text)
            continue

        if intent == "youtube_search":
            if "play" in text or "music" in text or "song" in text:
                play_music(text)
            else:
                youtube_search(text)
            continue

        speak(text)


# ----------------------------------------------------
# MODE SELECTION (FIRST!)
# ----------------------------------------------------
def choose_mode():
    print("\nSelect Mode:")
    print("1 → Voice Mode (Say 'Jarvis')")
    print("2 → Text Mode (Type commands)")
    choice = input("Enter 1 or 2: ").strip()

    return choice


# ----------------------------------------------------
# LOAD VOSK MODELS (AFTER MODE SELECTION)
# ----------------------------------------------------
wake_model = Model("vosk-model-en-us-0.22-lgraph")
wake_recognizer = KaldiRecognizer(wake_model, 16000)

cmd_model = Model("vosk-model-en-us-0.22-lgraph")
cmd_recognizer = KaldiRecognizer(cmd_model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=2048
)
stream.start_stream()


# ----------------------------------------------------
# VOICE MODE: WAKE WORD LISTENING
# ----------------------------------------------------
def listen_wake():
    while True:
        data = stream.read(2048, exception_on_overflow=False)

        if wake_recognizer.AcceptWaveform(data):
            text = json.loads(wake_recognizer.Result()).get("text", "")
            if not text:
                continue

            print("[Wake STT]:", text)
            for w in ["jarvis", "jarviz", "jervis"]:
                if w in text:
                    speak("Yes?")
                    return


# ----------------------------------------------------
# VOICE MODE: COMMAND LISTENING
# ----------------------------------------------------
def listen_command():
    while True:
        data = stream.read(4096, exception_on_overflow=False)

        if cmd_recognizer.AcceptWaveform(data):
            text = json.loads(cmd_recognizer.Result()).get("text", "")
            if not text:
                continue

            print("[CMD STT]:", text)

            # Exit voice mode
            if "exit" in text:
                speak("Exiting voice mode.")
                return

            if handle_memory(text): return
            if handle_translation(text): return
            if handle_wikipedia(text): return

            intent = predict_intent(text)
            print("Intent:", intent)

            lower = text.lower()

            if intent == "open_app":
                if "notepad" in lower: open_app("notepad")
                elif "chrome" in lower: open_app("chrome")
                elif "brave" in lower: open_app("brave")
                elif "discord" in lower: open_app("discord")
                else: speak("Which app?")
                return

            if intent == "close_app":
                if "notepad" in lower: close_app("notepad")
                elif "chrome" in lower: close_app("chrome")
                elif "brave" in lower: close_app("brave")
                elif "discord" in lower: close_app("discord")
                else: speak("Which app?")
                return

            if intent == "open_website":
                if open_website(text): speak("Opening website")
                else: speak("Website not found.")
                return

            if intent == "google_search":
                google_search(text)
                return

            if intent == "youtube_search":
                if "play" in lower or "song" in lower or "music" in lower:
                    play_music(text)
                else:
                    youtube_search(text)
                return

            speak(text)
            return


# ----------------------------------------------------
# MAIN PROGRAM LOOP
# ----------------------------------------------------
while True:

    mode = choose_mode()

    if mode == "2":
        speak("Text mode activated.")
        text_mode_loop()
        # When text mode ends → back to menu
        continue

    else:
        speak("Voice mode activated.")
        while True:
            listen_wake()
            listen_command()
            # After voice exit → back to menu
            break

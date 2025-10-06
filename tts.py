import threading, pyttsx3

tts_engine = pyttsx3.init()

voices = tts_engine.getProperty('voices')

# Choose a female-sounding voice (e.g., index 1)
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower():
        tts_engine.setProperty('voice', voice.id)
        break

tts_lock = threading.Lock()

def tts_say(text):
    def _speak(t):
        with tts_lock:
            tts_engine.say(t)
            tts_engine.runAndWait()
    threading.Thread(target=_speak, args=(text,), daemon=True).start()

import threading, pyttsx3

tts_engine = pyttsx3.init()
tts_lock = threading.Lock()

def tts_say(text):
    def _speak(t):
        with tts_lock:
            tts_engine.say(t)
            tts_engine.runAndWait()
    threading.Thread(target=_speak, args=(text,), daemon=True).start()

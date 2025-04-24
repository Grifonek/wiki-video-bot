import pyttsx3
import os

def generate_voice_over(article, summary):
    # init of pyttsx3
    engine = pyttsx3.init()

    # selecting and customizing voice
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

    # deleting previous file
    if os.path.exists("test.mp3"):
        os.remove("test.mp3")
    elif os.path.exists("test.wav"):
        os.remove("test.wav")

    # saving voice to file
    engine.save_to_file([article, summary], "test.wav")
    engine.runAndWait()
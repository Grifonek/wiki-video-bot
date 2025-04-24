import os
from gtts import gTTS

def generate_voice_over(article, summary):
    # deleting previous file
    if os.path.exists("test.mp3"):
        os.remove("test.mp3")
    elif os.path.exists("test.wav"):
        os.remove("test.wav")

    language = "en"

    myobj = gTTS(text=summary, lang=language, slow=False)

    myobj.save("test.mp3")
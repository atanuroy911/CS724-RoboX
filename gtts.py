from gtts import gTTS
import os

def textToSpeech(text):
    # Create a gTTS object
    tts = gTTS(text=text, lang='en', slow=False)

    # Save the speech as a temporary audio file
    tts.save("temp.mp3")

    # Play the audio file
    os.system("start temp.mp3")

if __name__ == "__main__":
    textToSpeech("hello world")

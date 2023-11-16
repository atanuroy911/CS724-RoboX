import pyttsx3

def textToSpeech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

    # Use a female voice (optional, depending on available voices)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Assuming index 1 is a female voice

    # Speak the text
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()

if __name__ == "__main__":
    textToSpeech("hello world")

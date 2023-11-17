import os

def textToSpeech(text):
    # -a is passed for voice amplitude
    # -p to control the pitch of voice
    # -s is passed for speed of speech
    # -g for word gap so that word will be clear
    # -v europe/hr
    speechCommand = "espeak -v en-us+f3 -s 150 '%s'" % (text)
    print("speech command---> ",speechCommand)
    os.system(speechCommand)
    

if __name__ == "__main__":
    textToSpeech("hello world")
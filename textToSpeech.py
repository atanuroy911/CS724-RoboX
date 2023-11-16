import os

def textToSpeech(text):
    # -a is passed for voice amplitude
    # -p to control the pitch of voice
    # -s is passed for speed of speech
    # -g for word gap so that word will be clear
    # -v europe/hr
    speechCommand = "espeak -a 200 -p 20 -s 125 -v en+f3 '%s'" % (text)
    print("speech command---> ",speechCommand)
    os.system(speechCommand)
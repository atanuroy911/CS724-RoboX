import speech_recognition as sr
import sys

# Redirect standard error to null
sys.stderr = open('/dev/null', 'w')

from ctypes import *
from contextlib import contextmanager

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

r = sr.Recognizer()
#mic = sr.Microphone(chunk_size=8192)
mic = sr.Microphone()

while True:
    with mic as source:
        with noalsaerr():
            try:
                print(mic)
                r.adjust_for_ambient_noise(source,1)
                r.energy_threshold = 500
                r.dynamic_enery_threshold = True
                r.pause_threshold=1.2
                
                print("Say something: ")
                audio = r.listen(source)
                #audio = r.listen(source,10)
                words = r.recognize_google(audio)
                print(words)
            
                if words == "exit":
                    print("GoodBye")
                    break      
            except sr.UnknownValueError:
                print("Could not understand audio")
                pass                                                                                   

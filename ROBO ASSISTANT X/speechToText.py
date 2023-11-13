import speech_recognition as sr
import sys

# Redirect standard error to null
sys.stderr = open('/dev/null', 'w')

r = sr.Recognizer()
#mic = sr.Microphone(chunk_size=8192)
mic = sr.Microphone()

while True:
    with mic as source:
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

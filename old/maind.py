
# take voice input
import import_ipynb
import speech_recognition as sr
from text_to_speech import textToSpeech
from initializer import initialize
from predict_answer import predictAnswer
import pandas as pd

def main():
    tokenizer,labelEncoder,responses = initialize()
    question = input("You:: ")
    print("You:: ",question)
    answer = predictAnswer(tokenizer,labelEncoder,responses,question)
    textToSpeech(answer)
#     r = sr.Recognizer()
#     mic = sr.Microphone()
#     tokenizer,labelEncoder,responses = initialize()
#     while True:
#         with mic as source:
#             print("ask anything:")
#             audio = r.listen(source)

#             try:
#                 question = r.recognize_google(audio)
#                 #textToSpeech(question)
#                 print("You:::: ",question)
#                 answer = predictAnswer(tokenizer,labelEncoder,responses,question)
#                 textToSpeech(answer)
#             except sr.RequestError:
#                 print("unable to catch words")
#             except sr.UnknownValueError:
#                 print("unknown value error")
                
if __name__ == "__main__":
    main()
import time
import subprocess
import speech_recognition as sr
import sounddevice as sd
import numpy as np
from audio import audio  # Import your audio class

# Dummy GPIO functions for testing on a non-Raspberry Pi device
def setmode(mode):
    pass

def setup(pin, direction):
    pass

def output(pin, state):
    pass

def PWM(pin, frequency):
    pass

def start(pwm, duty_cycle):
    pass

def cleanup():
    pass

# Set up PWM for motor speed control
pwm_a = PWM(18, 1000)  # 1000 Hz frequency
pwm_b = PWM(24, 1000)  # 1000 Hz frequency

# Initialize audio class
mic = audio(path='./audio/')  # Change the path accordingly

def stop():
    print("Stopping")

def move_forward(speed):
    print(f"Moving forward at speed {speed}")

def move_backward(speed):
    print(f"Moving backward at speed {speed}")

def turn_right(speed):
    print(f"Moving right at speed {speed}")

def turn_left(speed):
    print(f"Moving left at speed {speed}")

    
# Add other movement functions (move_backward, turn_right, turn_left) here

def voice_control():
    mic.recordWhileActive()  # Record audio while active
    text = mic.getText('sounds.wav')  # Use Google Speech Recognition to convert
    print("You said:", text)

    if "forward" in text:
        move_forward(50)
    elif "backward" in text:
        move_backward(50)
    elif "right" in text:
        turn_right(75)
    elif "left" in text:
        turn_left(75)
    elif "stop" in text:
        stop()
    elif "quit" in text:
        raise KeyboardInterrupt
    else:
        print('You said: ', text)

try:
    while True:
        voice_control()

except KeyboardInterrupt:
    pass

finally:
    stop()
    cleanup()

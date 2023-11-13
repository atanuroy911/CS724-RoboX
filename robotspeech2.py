import RPi.GPIO as GPIO
import time
import subprocess
import speech_recognition as sr
import sounddevice as sd
import numpy as np
from audio import audio  # Import your audio class
from textToSpeech import textToSpeech


# Define GPIO pins
IN1 = 17
IN2 = 27
IN3 = 22
IN4 = 23
ENA = 18
ENB = 24

# Set the GPIO mode and setup the pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# Set up PWM for motor speed control
pwm_a = GPIO.PWM(ENA, 1000)  # 1000 Hz frequency
pwm_b = GPIO.PWM(ENB, 1000)  # 1000 Hz frequency

# Initialize audio class
mic = audio(path='./audio/')  # Change the path accordingly

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def move_forward(speed):
    textToSpeech("Moving forward at speed " + str(speed))
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.start(speed)
    pwm_b.start(speed)

def move_backward(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.start(speed)
    pwm_b.start(speed)

def turn_right(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.start(speed)
    pwm_b.start(speed)

def turn_left(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.start(speed)
    pwm_b.start(speed)
    
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

try:
    while True:
        voice_control()

except KeyboardInterrupt:
    pass

finally:
    stop()
    GPIO.cleanup()

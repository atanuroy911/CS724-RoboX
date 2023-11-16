from flask import Flask, request, jsonify
import RPi.GPIO as GPIO

# import all the userdefind packages
from initializer import Initializer
from chatBots import predictResponse
from textToSpeech import textToSpeech
from chatBot import predictAnswer

import threading
import time

# set GPIO Pins
GPIO_TRIGGER = 2
GPIO_ECHO = 3

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

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

app = Flask(__name__)

words_to_exit = ["end", "quit", "terminate", "bye", "exit"]

# Model Initialize
print("inside main function")
# call the initializer function through the object
initializer_obj = Initializer()
initializer_obj.initialize()

# text to speech output to say all required fields has been initialised
# textToSpeech("Initilization of Robo assistant x is completed")

print("Initilization of Robo assistant x is completed")


# Use a lock to control access to the prompt function
prompt_lock = threading.Lock()

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance
def check_distance_routine():
    initial_speed = 50
    try:
        while True:
            dist = distance()
            print("Measured Distance = %.1f cm" % dist)

            if dist < 30:
                stop()
                time.sleep(1)  # Pause for 1 second

                # Change direction and move backward
                move_backward(initial_speed)
                time.sleep(1)  # Pause for 1 second

                # Change direction and turn right (you can customize the direction)
                turn_right(initial_speed)
                time.sleep(1)  # Pause for 1 second

                # Change direction back to forward
                move_forward(initial_speed)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

@app.before_first_request
def activate_job():
    thread = threading.Thread(target=check_distance_routine)
    thread.start()

@app.route('/check_connection')
def check_connection():
    response_data = {'status': 'success', 'message': 'Connection successful'}
    return jsonify(response_data), 200

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    user_query = data.get('user_query')
    print(user_query)
    if user_query == "Up":
        move_forward(100)
    elif user_query == "Down":
        move_backward(100)
    elif user_query == "Left":
        turn_left(50)
    elif user_query == "Right":
        turn_right(50)
    elif user_query == "OK":
        stop()
    response_data = {'status': 'success', 'message': f'Received ${data}'}
    return jsonify(response_data), 200



@app.route('/prompt', methods=['POST'])
def model_prompt():
    # Assuming the input data is in JSON format with a 'user_query' key
    data = request.json
    user_query = data.get('user_query')

    word_found = any(word in user_query for word in words_to_exit)

    if word_found:
        print("exit")
        textToSpeech("Exit Through Console")

    if user_query is None:
        response_data = {'status': 'error',
                         'message': 'Missing user_query in the request'}
        return jsonify(response_data), 400

    # Use a lock to ensure only one thread can execute the prompt function at a time
    with prompt_lock:
        # Call your prompt function with the user's query after a delay
        threading.Thread(target=delayed_prompt, args=(user_query,)).start()

    response_data = {'status': 'success',
                     'message': 'Query processed successfully'}
    return jsonify(response_data), 200

def delayed_prompt(user_query):
    # Introduce a delay (adjust the duration based on your needs)
    time.sleep(2)

    # Execute the prompt function
    prompt(user_query)

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    textToSpeech("Stopping")


def move_forward(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.start(speed)
    pwm_b.start(speed)
    textToSpeech("Moving forward at speed " + str(speed))

def move_backward(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.start(speed)
    pwm_b.start(speed)
    textToSpeech("Moving backward at speed " + str(speed))


def turn_right(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.start(speed)
    pwm_b.start(speed)
    textToSpeech("Turning Right")


def turn_left(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.start(speed)
    pwm_b.start(speed)
    textToSpeech("Turning Left")

def prompt(user_query):

    # TODO take this as user voice input

    print("You : ", user_query)

    # sending user input to predict answer using h5 model
    # answer = predictAnswer(initializer_obj.labelEncoder,initializer_obj.tokenizer,
        # initializer_obj.interpreter,initializer_obj.responses,user_query)
    # sending user input to predict chatbot response using tflite
    answer = predictResponse(initializer_obj.labelEncoder, initializer_obj.tokenizer,
                             initializer_obj.interpreter, initializer_obj.responses, user_query)
    # converting the predicted answer into voice
    textToSpeech(answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8900)

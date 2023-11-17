from flask import Flask, request, jsonify, Response, render_template
import cv2
import RPi.GPIO as GPIO

# import all the userdefind packages
from init2 import initialize
from textToSpeech import textToSpeech
from predict2 import predictAnswer

import threading
import time

# set GPIO Pins
GPIO_TRIGGER = 2
GPIO_ECHO = 3

GPIO.setmode(GPIO.BCM)

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
tokenizer, labelEncoder, responses = initialize()


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

camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


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
        turn_right(100)
    elif user_query == "Right":
        turn_left(100)
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
    stop_event.set()  # Set the event flag to signal the thread to stop
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    # textToSpeech("Stopping")


# Use threading event for signaling
stop_event = threading.Event()

# Additional flag to check if move_forward is in progress
forward_in_progress = False

def move_forward_with_distance_check(speed, min_distance=30):
    global forward_in_progress

    stop_event.clear()  # Clear the event flag

    # Check if move_forward is already in progress
    if forward_in_progress:
        return

    forward_in_progress = True

    while not stop_event.is_set():
        # Check the distance
        dist = distance()

        if dist < min_distance:
            stop()
            # Choose a direction to turn (left or right)
            turn_left(50)
            time.sleep(1)
            stop()
            move_forward(speed)
        else:
            # Continue moving forward
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
            pwm_a.start(speed)

        time.sleep(0.1)

    # Reset the event flag and forward_in_progress flag when the thread stops
    stop_event.clear()
    forward_in_progress = False

# Modify your existing move_forward function to call move_forward_with_distance_check
def move_forward(speed):
    threading.Thread(target=move_forward_with_distance_check, args=(speed,)).start()


def move_backward(speed):
    stop_event.set()  # Set the event flag to signal the thread to stop
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.start(speed)
    pwm_b.start(speed)
    # textToSpeech("Moving backward at speed " + str(speed))


def turn_right(speed):
    stop_event.set()  # Set the event flag to signal the thread to stop
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.start(speed)
    pwm_b.start(speed)
    # textToSpeech("Turning Right")


def turn_left(speed):
    stop_event.set()  # Set the event flag to signal the thread to stop
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.start(speed)
    pwm_b.start(speed)
    # textToSpeech("Turning Left")

def prompt(user_query):

    # TODO take this as user voice input

    print("You : ", user_query)

    # sending user input to predict answer using h5 model
    # answer = predictAnswer(initializer_obj.labelEncoder,initializer_obj.tokenizer,
        # initializer_obj.interpreter,initializer_obj.responses,user_query)
    # sending user input to predict chatbot response using tflite
    answer = predictAnswer(tokenizer, labelEncoder, responses, user_query)
    
    if 'forward' in answer :
        move_forward(100)
    elif 'backward' in answer :
        move_backward(100)
    elif 'right' in answer :
        turn_left(100)
    elif 'left' in answer :
        turn_right(100)
    elif 'stop' in answer :
        stop()

    # converting the predicted answer into voice
    textToSpeech(answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8900)

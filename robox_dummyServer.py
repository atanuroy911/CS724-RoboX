from flask import Flask, request, jsonify, render_template, Response
import cv2
# import RPi.GPIO as GPIO

# import all the userdefind packages
from init2 import initialize
from textToSpeech import textToSpeech
from predict2 import predictAnswer

import threading
import time

# # Define GPIO pins
# IN1 = 17
# IN2 = 27
# IN3 = 22
# IN4 = 23
# ENA = 18
# ENB = 24

# # Set the GPIO mode and setup the pins
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(IN1, GPIO.OUT)
# GPIO.setup(IN2, GPIO.OUT)
# GPIO.setup(IN3, GPIO.OUT)
# GPIO.setup(IN4, GPIO.OUT)
# GPIO.setup(ENA, GPIO.OUT)
# GPIO.setup(ENB, GPIO.OUT)

# # Set up PWM for motor speed control
# pwm_a = GPIO.PWM(ENA, 1000)  # 1000 Hz frequency
# pwm_b = GPIO.PWM(ENB, 1000)  # 1000 Hz frequency

app = Flask(__name__)

words_to_exit = ["end", "quit", "terminate", "bye", "exit"]

# Model Initialize
print("inside main function")
# call the initializer function through the object
# initializer_obj = initialize()
# initializer_obj.initialize()

tokenizer, labelEncoder, responses = initialize()

# text to speech output to say all required fields has been initialised
# textToSpeech("Initilization of Robo assistant x is completed")

print("Initilization of Robo assistant x is completed")


# Use a lock to control access to the prompt function
prompt_lock = threading.Lock()

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
    print("Stopping")


def move_forward(speed):
    print(f"Moving forward at speed {speed}")


def move_backward(speed):
    print(f"Moving backward at speed {speed}")


def turn_right(speed):
    print(f"Moving right at speed {speed}")


def turn_left(speed):
    print(f"Moving left at speed {speed}")


def prompt(user_query):

    # TODO take this as user voice input

    print("You : ", user_query)

    # sending user input to predict answer using h5 model
    # answer = predictAnswer(initializer_obj.labelEncoder,initializer_obj.tokenizer,
    # initializer_obj.interpreter,initializer_obj.responses,user_query)
    # sending user input to predict chatbot response using tflite
    # answer = predictAnswer(initializer_obj.labelEncoder, initializer_obj.tokenizer,
    #                          initializer_obj.interpreter, initializer_obj.responses, user_query)
    answer = predictAnswer(tokenizer, labelEncoder, responses, user_query)

    # converting the predicted answer into voice
    textToSpeech(answer)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8900)

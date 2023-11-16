import numpy
import pandas as pd
import string
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
import json
from tensorflow.lite.python import interpreter as interpreter_wrapper
#from tflite_runtime.interpreter import Interpreter
#from tflite_runtime.interpreter import InterpreterWithCustomOps
from sklearn.preprocessing import LabelEncoder
import random

def predictResponse(labelEncoder,tokenizer,interpreter,responses,user_query):
    new_user_query = tokenizer.texts_to_sequences([user_query])[0]
    max_sequence_length=22
    new_user_query = new_user_query[:max_sequence_length]

    #  pad the sequence if they are shorter then the expected length
    if len(new_user_query) < max_sequence_length:
        new_user_query += [0]* (max_sequence_length - len(new_user_query))
        
    new_user_query_tensor = tf.convert_to_tensor([new_user_query], dtype=tf.float32)

    interpreter.set_tensor(interpreter.get_input_details()[0]['index'], new_user_query_tensor)

    interpreter.invoke()

    output = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])
    output_max = output.argmax()

    response_tag = labelEncoder.inverse_transform([output_max])[0]
    response = random.choice(responses[response_tag])
    print("ROBO Assistant X response::: ",response)
    return response

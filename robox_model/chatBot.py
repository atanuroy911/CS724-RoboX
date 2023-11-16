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
from tensorflow.keras.models import load_model

def predictAnswer(labelEncoder,tokenizer,interpreter,responses,user_query):
    text_p = []
    # loading the h5 model
    new_model = load_model("/home/ayushi/project/ROBO ASSISTANT X/sensing_nlp.h5")
    prediction_input = [letters.lower() for letters in user_query if letters not in string.punctuation]
    prediction_input = ''.join(prediction_input)
    texts_p.append(prediction_input)
    
    # tokenizing
    prediction_input = tokenizer.texts_to_sequences(texts_p)
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input = pad_sequence([prediction_input],input_shape)
    output = new_model.predict(prediction_input)
    
    output = output.argmax()
    
    response_tag = labelEncoder.inverse_transform([output])[0]
    print("ROBO response ::: ",random.choice(responses[response_tag]))
    

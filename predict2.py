# code to save mode in pb format and load it for testing purpose
#from keras.models import load_model
from tensorflow import keras
import random
import pandas as pd
import string
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

new_model = keras.models.load_model("sensing_nlp.h5", compile=False)
new_model.summary()

input_shape = 22

def predictAnswer(tokenizer,labelEncoder,responses, question):
    texts_p=[]

    # removing punctuation and converting to lowercase
    prediction_input = [letters.lower() for letters in question if letters not in string.punctuation]
    prediction_input = ''.join(prediction_input)
    texts_p.append(prediction_input)

    # tokenizing and padding
    prediction_input = tokenizer.texts_to_sequences(texts_p)
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input = pad_sequences([prediction_input],input_shape)

    output= new_model.predict(prediction_input)
    output = output.argmax()

    response_tag = labelEncoder.inverse_transform([output])[0]
    answer = random.choice(responses[response_tag])
    print("ROBO ASSISTANT X::: ",answer)
    return answer
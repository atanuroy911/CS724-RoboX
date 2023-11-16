import numpy as np
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
from tensorflow import keras

def predictAnswer(labelEncoder,tokenizer, interpreter, responses,user_query):
    texts_p = []

    with open('intents.json') as content:
        data = json.load(content)

    # getting all the data to lists
    tags = []
    inputs = []
    responses = {}
    for intent in data['intents']:
        responses[intent['tag']] = intent['responses']
        for lines in intent['input']:
            inputs.append(lines)
            tags.append(intent['tag'])

    data = pd.DataFrame({"inputs":inputs,
                    "tags":tags})
    
    import string
    data['inputs'] = data['inputs'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
    data['inputs'] = data['inputs'].apply(lambda wrd: ''.join(wrd))

    tokenizer = Tokenizer(
    # num_words=None,
    num_words=200000,
    filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
    lower=True,
    split=' ',
    char_level=False,
    oov_token="<OOV>", #OOV means OOV
    analyzer=None
)
    tokenizer.fit_on_texts(data['inputs'])
    train = tokenizer.texts_to_sequences(data['inputs'])
    # loading the h5 model
    new_model = keras.models.load_model("./sensing_nlp.h5", compile=False)
    prediction_input = [letters.lower() for letters in user_query if letters not in string.punctuation]
    prediction_input = ''.join(prediction_input)
    texts_p.append(prediction_input)
    x_train = keras.preprocessing.sequence.pad_sequences(train)
    input_shape = x_train.shape[1]

    # tokenizing
    prediction_input = tokenizer.texts_to_sequences(texts_p)
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input = keras.preprocessing.sequence.pad_sequences([prediction_input],input_shape)
    output = new_model.predict(prediction_input)
    
    output = output.argmax()
    
    response_tag = labelEncoder.inverse_transform([output])[0]
    print("ROBO response ::: ",random.choice(responses[response_tag]))
    

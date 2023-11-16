import tensorflow as tf
import numpy as np
import pandas as pd
import json
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional, Input, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential
import matplotlib.pyplot as plt
import string
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences

def initialize():
    # importing the dataset
    with open('content.json') as content:
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
                
    # converting to dataframe
    data = pd.DataFrame({"inputs":inputs,"tags":tags})
    # Preprocessing the data
    # convertin words to lowercase and removing the punctuation
    data['inputs'] = data['inputs'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
    data['inputs'] = data['inputs'].apply(lambda wrd: ''.join(wrd))
    data
    
    # tokenize the data
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

    #apply padding
    x_train = pad_sequences(train)

    # encode the outputs
    labelEncoder = LabelEncoder()
    y_train = labelEncoder.fit_transform(data['tags'])
    
    return tokenizer,labelEncoder,responses
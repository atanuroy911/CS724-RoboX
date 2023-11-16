""" this function is to initialize all the required data
    first time only at the beginning of the code
"""
import pandas as pd
import string
import json
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.lite.python import interpreter as interpreter_wrapper

class Initializer:
    def __init(self):
        self.labelEncoder = None
        self.tokenizer = None
        self.interpreter = None
        self.responses = None
    def initialize(self):
        # Initialize all the requried data
        # load the json data
        with open('./intents.json') as content:
            data = json.load(content)

        self.labelEncoder = LabelEncoder()

        tags = []
        inputs = []
        self.responses = {}
        for intent in data['intents']:
            self.responses[intent['tag']] = intent['responses']
            for lines in intent['input']:
                inputs.append(lines)
                tags.append(intent['tag'])
                
        data = pd.DataFrame({"inputs":inputs, "tags":tags})

        data['inputs'] = data['inputs'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
        data['inputs'] = data['inputs'].apply(lambda wrd: ''.join(wrd))
        print(data)
        self.labelEncoder.fit_transform(data['tags'])

        self.tokenizer = Tokenizer(
            #num_words=None,
            num_words=200000,
            filters='',
            lower=True,
            split=' ',
            char_level=False,
            oov_token="<OOV>"
            )

        self.tokenizer.fit_on_texts(data['inputs'])
        
        # loading our tensorflow lite model
        nlp_model_path = "./sensor_nlp_model.tflite"

        with open(nlp_model_path,'rb') as file:
            model = file.read()
            
        #interpreter = Interpreter(nlp_model_path)
        self.interpreter = interpreter_wrapper.InterpreterWithCustomOps(
            model_content=model,
            )
        print("model loaded successfully")

        self.interpreter.allocate_tensors()
        print("input details ::: ",self.interpreter.get_input_details())
        print("outpure details ::::",self.interpreter.get_output_details())
    
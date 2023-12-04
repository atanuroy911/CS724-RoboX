# import all the userdefind packages
from initializer import Initializer
from textToSpeech import textToSpeech
from chatBot import predictAnswer

words_to_exit = ["end", "quit", "terminate", "bye","exit"]
def main():
    print("inside main function")
    # call the initializer function through the object
    initializer_obj = Initializer()
    initializer_obj.initialize()
    
    # text to speech output to say all required fields has been initialised
    textToSpeech("initilization of Robo assistant x is completed")
    
    # TODO take this as user voice input
    while True:
        user_query = input("You : ")
        
        word_found = any(word in user_query for word in words_to_exit)
        
        if word_found:
            print("exit")
            textToSpeech("exiting the program")
            break
        
        # sending user input to predict answer using h5 model
        #answer = predictAnswer(initializer_obj.labelEncoder,initializer_obj.tokenizer,
                                 #initializer_obj.interpreter,initializer_obj.responses,user_query)
        # sending user input to predict chatbot response using tflite
        answer = predictAnswer(initializer_obj.labelEncoder,initializer_obj.tokenizer,
                                 initializer_obj.interpreter,initializer_obj.responses,user_query)
        # converting the predicted answer into voice
        textToSpeech(answer)
        
    
if __name__ == "__main__":
    main()
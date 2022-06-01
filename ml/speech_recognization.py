import speech_recognition  as sr
import pyttsx3
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.models import load_model
from tensorflow import keras 
from main import model_parameter
import numpy as np
import torch
from utils import convert_input_file_to_tensor_dataset, init_logger, get_intent_labels, get_slot_labels, predict
from model import JointBERT
from transformers import BertTokenizer

############################ loading machine learning model ########################################################


def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

#will wait until it hears what you say
def speech_to_text():
    r = sr.Recognizer()
    mic = sr.Microphone()

    while 1:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            input = (r.recognize_google(audio)).lower()
            print(input)
            return input
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Please speak louder")
        


def main(parameter):
    while 1:
        print('running speech to text translation')
        command = speech_to_text()
        #command = 'can you change your language to english'
        keywords, intent = predict(command, parameter)
        if command == 'stop':
            SpeakText('I will retreat')
            #print('I will retreat')
            return
        else:
            print(keywords)
            print(intent)
            SpeakText('The intent is ' + intent)
            #print('The intent is ' + intent)



if __name__ == "__main__":
    parameter = model_parameter()
    main(parameter)

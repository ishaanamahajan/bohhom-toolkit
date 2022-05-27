import speech_recognition  as sr
import pyttsx3
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from tensorflow.python.keras.models import load_model
from tensorflow import keras 

############################ loading machine learning model ########################################################
class IntentClassifier:
    def __init__(self,classes,model,tokenizer,label_encoder):
        self.classes = classes
        self.classifier = model
        self.tokenizer = tokenizer
        self.label_encoder = label_encoder

    def get_intent(self,text):
        self.text = [text]
        self.test_keras = self.tokenizer.texts_to_sequences(self.text)
        self.test_keras_sequence = pad_sequences(self.test_keras, maxlen=12, padding='post')
        self.pred = self.classifier.predict(self.test_keras_sequence)
        return self.label_encoder.inverse_transform(np.argmax(self.pred,1))[0]

model = keras.models.load_model('models/intents.h5')
with open('utils/classes.pkl','rb') as file:
  classes = pickle.load(file)

with open('utils/tokenizer.pkl','rb') as file:
  tokenizer = pickle.load(file)

with open('utils/label_encoder.pkl','rb') as file:
  label_encoder = pickle.load(file)

nlu = IntentClassifier(classes,model,tokenizer,label_encoder)


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
        


def main():
    while 1:
        print('running speech to text translation')
        command = speech_to_text()
        if command == 'stop':
            SpeakText('I will retreat')
            return
        else:
            intent = nlu.get_intent(command)
            if intent == 'oos':
                SpeakText('I do not understand you')
            else:
                SpeakText('The intent is ' + intent)



if __name__ == "__main__":
    main()

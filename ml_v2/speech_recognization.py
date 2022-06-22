import speech_recognition  as sr
import pyttsx3
from main import model_parameter
import numpy as np
from utils import predict
from googletrans import Translator
from translate import Translator
from gtts import gTTS
from playsound import  playsound
from datetime import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

############################ loading machine learning model ########################################################
global language

def translate_lan(sentence, old_language, new_language):
    translator= Translator(from_lang=old_language,to_lang=new_language)
    translation = translator.translate(sentence)
    return translation

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
            input = r.recognize_google(audio, language = language)
            translator = Translator()
            en_translation = translator.translate(input)
            
            print(en_translation)
            return en_translation
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Please speak louder")
        


def main(parameter):
    #set language
    language = "en-US"
    old_language = language
    #initialize and train chatbot
    chatbot = ChatBot('Charlie')
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english.greetings")
    trainer.train("chatterbot.corpus.english.conversations")
    trainer.train("chatterbot.corpus.english.botprofile")
    #start interaction
    while 1:
        print('running speech to text translation')
        #command = speech_to_text()
        command = 'hello'
        keywords, intent = predict(command, parameter)
        response = chatbot.get_response(command)

        if command == 'stop':
            #SpeakText('I will retreat')
            print('I will retreat')
            return
        elif intent == 'greeting':
            reply_correct = translate_lan(response, old_language, language)
            print(reply_correct)
            #SpeakText(reply_correct)
        elif intent == 'change_language':
            if keywords and len(keywords) == 1:
                new_language = keywords[0].lower()
                if new_language == 'mandarin' or new_language == 'chinese':
                    new_language = "ZH-CN"
                print('language is switched to: ' + new_language)
            else:
                print('what language do you want to switch to?')
        elif intent == 'navigation':
            pass
        elif intent == 'introduce_item':
            pass
        elif intent == 'ask_name':
            pass
        else:
            print(keywords)
            print(intent)
            #SpeakText('The intent is ' + intent)
            print('The intent is ' + intent)



if __name__ == "__main__":
    parameter = model_parameter()
    main(parameter)

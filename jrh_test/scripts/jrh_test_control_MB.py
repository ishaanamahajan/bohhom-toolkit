#!/usr/bin/env python

from logging.config import listen
import rospy
from geometry_msgs.msg import Twist
import speech_recognization
from mainz import *
from utils import predict
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import rospy
from std_msgs.msg import Int16


if __name__ == "__main__":
   
    rospy.init_node("jrh_test_control_MB")
    pub = rospy.Publisher("jrh_zqw",Int16,queue_size=100)


    ############initialize and train chatbot###########
   # chatbot_greeting = ChatBot('greeting')
    #trainer_greeting = ChatterBotCorpusTrainer(chatbot_greeting)
    #trainer_greeting.train("chatterbot.corpus.english.greetings")

   # chatbot_navigation = ChatBot('navigation')
   # trainer_navigation = ChatterBotCorpusTrainer(chatbot_navigation)
   # trainer_navigation.train("chatterbot.corpus.custom.navigation")
    
    ############start interaction######################
    parameter = model_parameter()
    instruction = 0

    #main(parameter)
    start = False
    command_type = Int16()
    command_type = 0

    while 1:
        print("command_type published: " + str(command_type))
        pub.publish(command_type)
        instruction = 0
        command_type = Int16(instruction)
        print('\n########################## press enter to start interaction ##############################\n')
        trigger = str(input())
        if trigger == '':
            start = True
            print('\n################################ interaction started #####################################\n')
        #print("command_type published: " + str(command_type))
        #pub.publish(command_type)
        while start:
            print('the current instruction is: ' + str(instruction))
            if instruction !=0:
                start = False
                print('############################## registered singal ##############################')
            else:
                print('\n##################################### listening ##########################################\n')
                command = str(speech_recognization.speech_to_text())
                #command = str(input())
                print('>>>you said: ' + command) 
                keywords, intent = predict(command, parameter)
                print(intent)
                if intent == 'retreat':
                    print('>>>bot: I will retreat! Goodbye!')
                    speech_recognization.SpeakText('I will retreat')
                    instruction = 1
                    command_type = Int16(instruction)
                elif intent == 'greeting':
                #    response = str(chatbot_greeting.get_response(command))
                 #   response = response + ' What can I help you with?'
                  #  print('>>>bot: ' + response)
                    start = False

                elif intent == 'change_language':
                     if keywords and len(keywords) == 1:
                         new_language = keywords[0].lower()
                         if new_language == 'mandarin' or new_language == 'chinese':
                             new_language = "ZH-CN"
                         print('language is switched to: ' + new_language)
                         start = False
                     else:
                         print('what language do you want to switch to?')
                elif intent == 'navigation':
                     destination = ' '.join(keywords)
                     print(destination)
                     if destination == 'exit':
                        instruction = 8
                        command_type = Int16(instruction)
                     elif destination == 'location a':
                        instruction = 7
                        command_type = Int16(instruction)
                   #  response = str(chatbot_navigation.get_response(command))
                     print('>>>bot: Ok, please follow me ')

                elif intent == 'introduce_item':
                     start = False
                elif intent == 'ask_name':
                     print('my name is robot')
                     start = False
                elif intent == 'adjust_position':
                     print('>>>bot: Ok')
                     if 'forward' in keywords:
                         instruction = 2
                         command_type = Int16(instruction)
                     elif 'back' in keywords:
                         instruction = 3
                         command_type = Int16(instruction)
                     elif 'rotate' in keywords or 'around' in keywords:
                         instruction = 4
                         command_type = Int16(instruction)
                     elif 'left' in keywords:
                         instruction = 5
                         command_type = Int16(instruction)
                     elif 'right' in keywords:
                         instruction = 6
                         command_type = Int16(instruction)

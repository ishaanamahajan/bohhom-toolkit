from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


# Create a new chat bot named Charlie
chatbot = ChatBot('Charlie')

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")
#trainer.train("chatterbot.corpus.english.conversations")
#trainer.train("chatterbot.corpus.english.botprofile")

response = chatbot.get_response('good morning.')

print(response)
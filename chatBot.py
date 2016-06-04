from chatterbot import ChatBot
from chatterbot.training.trainers import ListTrainer
import sys
import os
#
# Execution: python chatBot.py Kyle.txt Kyle
#

dfan = ChatBot("DFan")
dfan.set_trainer(ListTrainer)
log = sys.argv[1]     # the name of your chat file (e.g. Kyle.txt)
friend = sys.argv[2]  # first name of friend (matches that in chat file)

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "Chats/" + log
abs_file_path = os.path.join(script_dir, rel_path)

with open(abs_file_path) as data_file:    
    data = open(abs_file_path, "r")


def createChunk(): # either input or response (indexes 0 or 1 of list fed to train DFan)
    line = '1'  # just initialized to something meaningless that's not empty
    string = ''
    while True:
        line = data.readline().rstrip('\n') # .rstrip is VERY IMPORTANT - avoids appending new line \n to end when parsing
        if line == '':
            break
        group = [string, line]
        string = ''.join(group) # to concatenate mixed ASCII strings with unicode emojis
    return string

# process input and train the chatbot
line = data.readline().rstrip('\n')
while True:
    line = data.readline().rstrip('\n')
    if line == '':
        break
    message = ''
    response = ''

    # depends on who started the chat first
    if line == 'Me:':
        message += createChunk()
        data.readline().rstrip('\n')
        response += createChunk()

    if line == friend + ':':
        response += createChunk()
        data.readline().rstrip('\n')
        message += createChunk()
   
    chunk = [message, response] # first entry of list is the input, second entry is what you expect that bot to output
    dfan.train(chunk)  # we're using the ListTrainer which takes a list as a training parameter.


# here the user is the one powering the conversation line-by-line
def chatWithDFan(dfan):
    while True:
        message = raw_input("You: ")
        if message == 'Bye':
            break
        print("DFan: " + str(dfan.get_response(message)))  #str cast to handle conversion

# here after entering an initial conversation starter the program takes its own simulated output to generate the next response.s
def simulate(dfan):
    print "Start off the conversation with a phrase and watch it unravel."
    response = raw_input("You: ")
    counter = 1
    while True:
        response = dfan.get_response(response)
        if counter % 2 == 1:
            print "DFan: " + str(response)
        else:
            print "You: " + str(response)
        counter += 1


print("Your chat has started; press and hold ctrl-c in terminal to stop the conversation.")
choice = raw_input("Would you like to chat with DFan? Or would you like to view a simulated chat (no user input on your part?) Type 'DFan' or 'Simulated' to make your selection. \n")
if choice == 'DFan':
    chatWithDFan(dfan)
if choice == 'Simulated':
    simulate(dfan)




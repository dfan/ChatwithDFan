import json
import sys
import os
import shutil
from os.path import join
from os import listdir, rmdir
from shutil import move
#
# Sample Execution: python parser.py Kyle.json Kyle
#

file = sys.argv[1]     # e.g. Kyle.json
output = sys.argv[2]   # e.g. Kyle (extension .txt is appended to this)
myID = 100001268660775 # replace with your ID (http://findmyfbid.com)

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "Chats/" + file
abs_file_path = os.path.join(script_dir, rel_path)

with open(abs_file_path) as data_file:    
    data = json.load(data_file)

target = open(output + '.txt', 'w')

count = 0
previous = ''
current = ''
for i in data:
    if 'author' in i:
        current = i['author']
        if current != previous:
            target.write('\n')
            if current == 'fbid:%d'  %(myID):
                target.write('Me:')
                target.write('\n')
            else:
                target.write(output + ':')
                target.write('\n')

    if 'body' in i:
        target.write(i['body'].encode('utf-8'))
        target.write('\n')
        count += 1
    previous = current
target.write('\n') 
numMessages = '%d messages' %(count)
target.write(numMessages)


script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
move(join(script_dir, output + '.txt'), join(script_dir, 'Chats', output + '.txt'))

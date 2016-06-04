# ChatwithDFan
Simulate your own chats with yourself or friends by feeding your own Facebook chats into a machine learning algorithm. Written in Python.
`dumper.py` which scrapes Facebook conversations and outputs in JSON format was modified from [/RaghavSood/FBMessageScraper](https://github.com/RaghavSood/FBMessageScraper) and the Python package [ChatterBot](https://github.com/gunthercox/ChatterBot) was used to create the ChatBot and train it. `parser.py` was written to extract messages-only from the JSON objects outputted by `dumper.py` and output in a .txt format.

Credentials Setup
=============

These instructions are identical to the first section of the README in [FBMessageScraper]((https://github.com/RaghavSood/FBMessageScraper)
The following fields in `dumper.py` need to be replaced with your own.

1. In Chrome, open [facebook.com/messages](https://www.facebook.com/messages/) and open any conversation with a fair number of messages
2. Open the network tab of the Chrome Developer tools
3. Scroll up in the conversation until the page attempts to load previous messages
4. Look for the POST request to [thread\_info.php](https://www.facebook.com/ajax/mercury/thread_info.php)
5. You need to copy certain parameters from this request into the python script to complete the setup:
  1. Set the `cookie` value to the value you see in Chrome under `Request Headers`
  2. Set the `__user` value to the value you see in Chrome under `Form Data` 
  3. Set the `__a` value to the value you see in Chrome under `Form Data`
  4. Set the `__dyn` value to the value you see in Chrome under `Form Data`
  5. Set the `__req` value to the value you see in Chrome under `Form Data`
  6. Set the `fb_dtsg` value to the value you see in Chrome under `Form Data`
  7. Set the `ttstamp` value to the value you see in Chrome under `Form Data`
  8. Set the `__rev` value to the value you see in Chrome under `Form Data`

Downloading Messages
====================

1. Get the conversation ID for your friend(s) at [findmyfbid.com](http://findmyfbid.com)
2. Run the command `python dumper.py {id} {name} 2000`, and put the value you just retrieved for ID. For {name} put the filename you want for the output, e.g. if you want Kyle.txt to appear in your directory, type Kyle here.
3. Messages are saved by default to `Chats`; check to make sure name.json is in your directory/Chats.

Parsing Messages to Retrieve Only the Conversation Text
====================

1. `dumper.py` outputs in JSON so to get the chats in a more readable format, we need to run `parser.py`
2. Go inside `parser.py` and change the entry for `myID` to that of your own Facebook profile ID.
3. If the file you produced in the download step was named `Kyle.json`, run python chatBot.py Kyle.json Kyle
4. This parsed output is saved to `Chats`; check to make sure name.txt is in your directory/Chats

Starting Up the ChatBot
====================

1. Execute `python chatBot.py Name.txt Name`
2. Follow the on-screen instructions and have fun!

Known Issues
============

1. The parsing script is not perfect. Pictures and GIFs sent by chat will just register as a blank line in the .txt output. When you send a message and your friend reads it but doesn't reply, and then you send another message a few days later, Facebook will add the new messages to a separate JSON object. So in your output the script might look like:

Me:
Blah blah


Me:
Blah Blah

Friend:
Oh sorry

As of now the script cannot fix this and you will have to manually remove the extra linebreaks. Leaving the extra line breaks won't cause the chatbot to crash, but the output will be less realistic because it will have trained itself correctly only on the chat up until that extra line break. 



import urllib2
import urllib
import gzip
import os
import json
import sys
import time
import StringIO

__author__ = "Raghav Sood"
__copyright__ = "Copyright 2014"
__credits__ = ["Raghav Sood"]
__license__ = "CC"
__version__ = "1.0"
__maintainer__ = "Raghav Sood"
__email__ = "raghavsood@appaholics.in"
__status__ = "Production"

if len(sys.argv) <= 1:
    print "Usage:\n     python dumper.py [conversation ID] [chunk_size (recommended: 2000)] [{optional} offset location (default: 0)]"
    print "Example conversation with Raghav Sood"
    print " python dumper.py 1075686392 2000 0"
    sys.exit()

error_timeout = 30 # Change this to alter error timeout (seconds)
general_timeout = 7 # Change this to alter waiting time afetr every request (seconds)
messages = []
talk = sys.argv[1]
offset = int(sys.argv[3]) if len(sys.argv) >= 4 else int("0")
timestamp = int("0")
messages_data = "lolno"
end_mark = "\"payload\":{\"end_of_history\""
limit = int(sys.argv[2])
headers = {"origin": "https://www.facebook.com", 
"accept-encoding": "gzip,deflate", 
"accept-language": "en-US,en;q=0.8", 
"cookie": "_ga=GA1.2.124705194.1451836936; datr=B0aJVqBA01yj5bcrWGVS6-jt; pl=n; lu=ghtK4yetiAygwUwNofY9Ew_A; c_user=100001268660775; xs=254%3A714vgwSrduSNbQ%3A2%3A1464899209%3A11412; csm=2; s=Aa47NJRZDIJbbA8q.BXUJaJ; sb=iZZQV2cr5XISP5lTYokxSYW-; fr=05zCRw4LImPjrNYEr.AWVrU_25RPS-qgdtAtxdjLgWzww.BXUJaJ._1.FdQ.0.0.AWURtNXU; p=-2; act=1464920913863%2F21; presence=EDvF3EtimeF1464921064EuserFA21B01268660775A2EstateFDsb2F1464920905409Et2F_5b_5dElm2FnullEuct2F1464920162011EtrFA2close_5fescA2EtwF497984414EatF1464920973623EwmlFDfolderFA2inboxA2Ethread_5fidFA2user_3a1B00334634805A2CG464921064743CEchFDp_5f1B01268660775F93CC; wd=722x678", 

"pragma": "no-cache", 
"user-agent": " Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36", 
"content-type": "application/x-www-form-urlencoded", 
"accept": "*/*", 
"cache-control": "no-cache", 
"referer": "https://www.facebook.com/messages/zuck"}

base_directory = "Messages/"
directory = base_directory + str(talk) + "/"
pretty_directory = base_directory + str(talk) + "/Pretty/"

try:
    os.makedirs(directory)
except OSError:
    pass # already exists

try:
    os.makedirs(pretty_directory)
except OSError:
    pass # already exists

while end_mark not in messages_data:

    data_text = {"messages[user_ids][" + str(talk) + "][offset]": str(offset), 
    "messages[user_ids][" + str(talk) + "][limit]": str(limit),
        "messages[user_ids]["+ str(talk) + "][timestamp]": str(timestamp),
    "client": "web_messenger", 
    "__user": "100001268660775", 
    "__a": "1", 
    "__dyn": "7AmajEzUGByFd112u6aOGeFxq9ACwKyaF7By8VFLFwxBxCbzES2N6xybxu13wIwYxebkwy3eF8W49XDG4UiCxicxW6otz9UcXCxaFEW2PxOcxu5ocE88C9ADBBGbx24o", 
    "__req": "y", 
    "fb_dtsg": "AQHkD0yfB1s9:AQHcFyPOgTr2", 
    "ttstamp": "2658172107684812110266491155758658172997012180791038411450", 
    "__rev": "2371355"}
    data = urllib.urlencode(data_text)
    url = "https://www.facebook.com/ajax/mercury/thread_info.php"

    print "Retrieving messages " + str(offset) + "-" + str(limit+offset) + " for conversation ID " + str(talk)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    compressed = StringIO.StringIO(response.read())
    decompressedFile = gzip.GzipFile(fileobj=compressed)


    outfile = open(directory + str(offset) + "-" + str(limit+offset) + ".json", 'w')
    messages_data = decompressedFile.read()
    messages_data = messages_data[9:]
    json_data = json.loads(messages_data)
    if json_data is not None and json_data['payload'] is not None:
        try:
            messages = json_data['payload']['actions'] + messages
            timestamp = int(json_data['payload']['actions'][0]['timestamp']) - 1
        except KeyError:
            pass #no more messages
    else:
        print "Error in retrieval. Retrying after " + str(error_timeout) + "s"
        print "Data Dump:"
        print json_data
        time.sleep(error_timeout)
        continue
    outfile.write(messages_data)
    outfile.close() 
    command = "python -mjson.tool " + directory + str(offset) + "-" + str(limit+offset) + ".json > " + pretty_directory + str(offset) + "-" + str(limit+offset) + ".pretty.json"
    os.system(command)
    offset = offset + limit
    time.sleep(general_timeout) 

finalfile = open(directory + "complete.json", 'wb')
finalfile.write(json.dumps(messages))
finalfile.close()
command = "python -mjson.tool " + directory + "complete.json > " + pretty_directory + "complete.pretty.json"
os.system(command)
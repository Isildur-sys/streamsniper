import time
import FetchDataIngame
import FetchFromTwitch
import queue
last_request = 0
request_interval = 0.3
nameQue = [] #holds the names that haven't been checked yet (due too many api calls)
nameStorage = []#holds all the names that have been checked

while (True):
    #get the the killfeed
    feed = FetchDataIngame.pullKillFeed()
    #extract player names from the feed
    names =  ["user_login=mrdogeétv&user_login=mrdogeé"]#FetchDataIngame.extractNames(feed)
    if names != None:
        #if the killfeed had names in it 
        for name in names:
            #add name to storage and queue
            if name not in nameStorage and name != "":
                print("New player found! {}".format(name))
                nameStorage.append(name)
                nameQue.append(name)
                         
    if time.time() - last_request > request_interval and len(nameQue) != 0:
        #search names which are in the queue from twitch
        nextName = nameQue[0]
        formattedNames = FetchDataIngame.format_Name(nextName)
        res = FetchFromTwitch.get_response(formattedNames)
        try:
            last_request = time.time()
            streamerStatus = FetchFromTwitch.response_live(res)
            nameQue.pop(0)
            print(len(nameQue))
            if streamerStatus == "live":
                print("----------Live Streamer In My Game!----------")
        except KeyError as e:
            err = "{}".format(e)
            if err == "400":
                #faulty name, get rid of it
                nameQue.pop(0)
            continue
        except IndexError:
            print("Player not found!")
            continue   
    time.sleep(0.25)
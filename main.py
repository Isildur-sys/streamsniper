import time
import FetchDataIngame
import FetchFromTwitch
import queue
last_request = 0
request_interval = 5
nameQue = [] #holds the names that haven't been checked yet (due too many api calls)
nameStorage = []#holds all the names that have been checked

while (True):
    #get the the killfeed
    feed = FetchDataIngame.pullKillFeed()
    #extract player names from the feed
    names =  FetchDataIngame.extractNames(feed)
    if names != None:
        #if the killfeed had names in it 
        for name in names:
            #search the names from twitch
            if name not in nameStorage and name != "":
                nameStorage.append(name)
                nameQue.append(name)
                if time.time() - last_request > request_interval:
                    nextName = nameQue[0]
                    formattedNames = FetchDataIngame.format_Name(nextName)
                    res = FetchFromTwitch.get_response(formattedNames)
                    try:
                        last_request = time.time()
                        streamerStatus = FetchFromTwitch.response_live(res)
                        nameQue.pop(0)
                        if streamerStatus == "live":
                            print("----------Live Streamer In My Game!----------")
                    except KeyError:
                        print("Too many requests!")
                        continue
                    except IndexError:
                        print("Player not found!")
                        continue          
    if time.time() - last_request > request_interval and len(nameQue) != 0:
        nextName = nameQue[0]
        formattedNames = FetchDataIngame.format_Name(nextName)
        res = FetchFromTwitch.get_response(formattedNames)
        try:
            last_request = time.time()
            streamerStatus = FetchFromTwitch.response_live(res)
            print("Should pop now!")
            nameQue.pop(0)
            if streamerStatus == "live":
                print("----------Live Streamer In My Game!----------")
        except KeyError:
            print("Too many requests!")
            continue
        except IndexError:
            print("Player not found!")
            continue   
    time.sleep(0.25)
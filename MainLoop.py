import time
import re
import FetchDataIngame
import FetchFromTwitch

flag = True
streamerQue = [] #holds live streamers in your match, until app.new_stream method 
                 #fetches them to spawn a new embedded Twitch Stream frame

def runMain():
    print("running main")
    last_request = 0
    request_interval = 1
    nameQue = [] #holds the names that haven't been checked yet (due too many api calls)
    nameStorage = []#holds all the names that have been checked
    streamerStorage = [] #all streamers in the match

    while (flag):
        #get the the killfeed
        feed = FetchDataIngame.pullKillFeed()
        #extract player names from the feed
        names =  FetchDataIngame.extractNames(feed)
        if names != None:
            #if the killfeed had names in it 
            for name in names:
                name = re.sub('\[.*?\]', '', name) #delete [CLANTAG]
                name = re.sub(r'[^A-Za-z0-9_ ]+', '', name) #delete non alphanumeric, keep spaces and underscores
                name = name.strip("_") #strip trailing or preceding underscores
                name = name.strip() #strip trailing or preceding spaces
                name = name.lower() #make name lowercase
                #add name to storage and queue
                if name not in nameStorage and name != "":
                    print("New player found! {}".format(name))
                    nameStorage.append(name)
                    nameQue.append(name)
                            
        if time.time() - last_request > request_interval and len(nameQue) != 0:
            #search twitch for names that are in the queue
            nextName = nameQue[0]
            formattedNames = FetchDataIngame.format_Name(nextName)
            res = FetchFromTwitch.get_response(formattedNames)
            try:
                print("Inspecting...")
                last_request = time.time()
                streamerStatus = FetchFromTwitch.response_live(res)
                nameQue.pop(0)
                #print(len(nameQue))
                if streamerStatus == "live":
                    streamerStorage.append(nextName)
                    streamerQue.append(nextName)
                    print("----------Live Streamer In My Game!----------")
                    print("-----------{}-----------".format(nextName))
                    
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
    print("Closing loop")
runMain()
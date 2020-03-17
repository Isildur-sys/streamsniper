import time
import FetchDataIngame
import FetchFromTwitch

while (True):
    #get the the killfeed
    feed = FetchDataIngame.pullKillFeed()
    #extract player names from the feed
    names = FetchDataIngame.extractNames(feed)
    if names != None:
        #if the killfeed had names in it 
        for name in names:
            #search the names from twitch
            formattedNames = FetchDataIngame.format_Name(name)
            res = FetchFromTwitch.get_response(formattedNames)
            FetchFromTwitch.response_live(res)
    
    time.sleep(0.25)
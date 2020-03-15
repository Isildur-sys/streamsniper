import time
import FetchDataIngame
import FetchFromTwitch

while (True):
    #feed = pullKillFeed()
    #names = extractNames(feed)
    usr = FetchFromTwitch.get_user("summit1g")
    res = FetchFromTwitch.get_response(usr)
    FetchFromTwitch.response_live(res)
    time.sleep(0.25)
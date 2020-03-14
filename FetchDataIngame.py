import pip
import tkinter
import cv2
import pytesseract
import numpy as np
import time
import re
import FetchFromTwitch

from PIL import ImageGrab, Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\maba9\AppData\Local\Tesseract-OCR\tesseract.exe'

def extractNames(names):
    #extract player names from the text passed from killfeed
    #return killer (= 0) and killed (= 1) as an array
    res = []
    if "killed" in names and "with" in names:
        #names = names.replace(" ", "")
        names = names.split("killed")
        killer = names[0]
        killed = re.match(r".+?(?=with)" ,names[1])[0]
        killer = killer.strip()
        killed = killed.strip()

        res[0] = killer
        res[1] = killed
        print(killer)
        print(killed)
        return res

def pullKillFeed():
    #take screenshot of the killfeed and run tesseract to extract text out of the image
    #returns feed as a string
    root = tkinter.Tk()
    winWidth = root.winfo_screenwidth()
    winHeight = root.winfo_screenheight()

    feed = ImageGrab.grab(bbox=(winWidth/1.5, winHeight/1.25, winWidth-100, winHeight-150))
    #feed.save("pic{}.png".format(param))
    grayed = cv2.cvtColor(np.array(feed), cv2.COLOR_BGR2GRAY)
    feedTxt = pytesseract.image_to_string(grayed, lang='eng')
    feedTxt = feedTxt.replace('\n', '')
    feedTxt = ''.join(feedTxt)

    #print(feedTxt)
    return feedTxt

def formatName(name):
    #extract tags from the name not related to the name
    name.replace(" ", "")
    names = []
    names.append(name)

    re.sub('\[.*?\]', '', name) #delete [CLANTAG]

    resName = name
    
    #search possible twitch indicators and remove them
    if "ttv" == name[:3] or "ttv" == name[:-3]:
        n = name
        n = n.replace("ttv", "") #someonettv or ttvsomeone
        names.append(n)
        print(n)
    if "twitch.tv" in name:
        resName = n.replace("twitch.tv", "")
    #search possible clan tag
    if "<" in name and ">" in name:
        re.sub(r'<.+?>', '', resName)
    
    print(name)
    print(resName)
    

respos = FetchFromTwitch.get_response(FetchFromTwitch.get_user("summit1g"))
FetchFromTwitch.print_response(respos)

#formatName("[CASH]summit1g")
while (True):
    feed = pullKillFeed()
    names = extractNames(feed)
    time.sleep(0.25)
    
    
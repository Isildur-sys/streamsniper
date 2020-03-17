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
    return None
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

def format_Name(name):
    #extract tags from the name not related to the name, by creating different
    #"strains" that are different mutations of the original screen name
    names = set([])
    #all strains will inherit these changes
    name = re.sub('\[.*?\]', '', name) #delete [CLANTAG]
    name = name.lower() #make name lowercase
    
    #create new strain from name with no underscores and spaces removed
    noUnderScore = name.replace(" ", "")
    noUnderScore = noUnderScore.replace("_", "")
    #replace all spaces with underscore for original strain
    name = name.replace(" ", "_")

    #make strings alphanumeric
    name = re.sub('[\W]+', '', name)
    noUnderScore = re.sub('[\W]+', '', noUnderScore)

    names.add(name) #add original strain to result
    name2 = name #new strain from original
    noUnderScore2 = noUnderScore #new strain from noUnderScores
    #search possible twitch indicators and remove them
    if name.endswith("ttv") or name.startswith("ttv"):
        n = name
        na = noUnderScore
        n = n.replace("ttv", "") #Streamer_1ttv or ttvStreamer_1
        na = na.replace("ttv", "") #Streamer1ttv or ttvStreamer1
        names.add(n)
        names.add(na)
    else:
        #if no ttv tag, add tv tag to the end and try it
        nameTV = "{}tv".format(name)
        noUnderScoreTV = "{}tv".format(noUnderScore)
        names.add(nameTV)
        names.add(noUnderScoreTV)
    if "twitch.tv" in name:
        noUnderScore2 = noUnderScore2.replace("twitch.tv", "")
        name2 = name2.replace("twitch.tv", "")
    elif "twitch" in name:
        noUnderScore2 = noUnderScore2.replace("twitch", "")
        name2 = name2.replace("twitch", "")
    
    names.add(noUnderScore)
    names.add(noUnderScore2)
    names.add(name)
    names.add(name2)

    res = ""
    for nam in names:
        if res != "":
            res += "&"
        res += format_user(nam)
    print(res)
    return names

def format_user(name):
    return "user_login={0}".format(name)

ns = format_Name("[CASH]summit1g")

    
    
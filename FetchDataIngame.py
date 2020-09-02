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

ROOT = tkinter.Tk()
WIN_WIDTH = ROOT.winfo_screenwidth()
WIN_HEIGHT = ROOT.winfo_screenheight()
REALM_ROYALE_FRAME = (WIN_WIDTH/1.5, WIN_HEIGHT/1.25, WIN_WIDTH-100, WIN_HEIGHT-150)
PUBG_FRAME = (WIN_WIDTH/1.4, WIN_HEIGHT/16.9, WIN_WIDTH-10, WIN_HEIGHT-950)

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

        res.append(killer)
        res.append(killed)
        return res
    return None
def pullKillFeed():
    #take screenshot of the killfeed and run tesseract to extract text out of the image
    #returns feed as a string
    feed = ImageGrab.grab(bbox=PUBG_FRAME)
    
    #feed.save("pic{}.png".format(1))
   
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
    elif name.endswith("tv") or name.startswith("tv"):
        m = name
        ma = noUnderScore
        m = m.replace("tv", "") #Streamer_1tv or tvStreamer_1
        ma = ma.replace("tv", "") #Streamer1tv or tvStreamer1
        names.add(m)
        names.add(ma)
    else:
        #if no ttv or tv tag, add tv tag to the end and try it
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
        nam = nam.strip("_")
        if res != "":
            res += "&"
        res += format_user(nam)
    return res

def format_user(name):
    return "user_login={0}".format(name)

#ns = format_Name("summit1g")

#count = 1
#while(count < 7): 
#    feed = ImageGrab.grab(bbox=(WIN_WIDTH/1.4, WIN_HEIGHT/16.9, WIN_WIDTH-10, WIN_HEIGHT-950))
#    feed.save("pic{}.png".format(count))
#    count = count + 1 
#    time.sleep(2)
    
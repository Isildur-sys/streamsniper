import pip
import tkinter
import cv2
import pytesseract
import numpy as np
import time
import re
from PIL import ImageGrab, Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\maba9\AppData\Local\Tesseract-OCR\tesseract.exe'

def extractNames(names):
    #extract player names from the text passed from killfeed
    if "killed" in names and "with" in names:
        #names = names.replace(" ", "")
        names = names.split("killed")
        killer = names[0]
        killed = re.match(r".+?(?=with)" ,names[1])[0]
        killer = killer.strip()
        killed = killed.strip()

        print(killer)
        print(killed)

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

while (True):
    feed = pullKillFeed()
    extractNames(feed)
    time.sleep(0.25)
    
    
import cv2
import numpy as np
import imutils 
import pyzbar.pyzbar as pyzbar
import math
from win10toast import ToastNotifier
from pynotifier import Notification as pyn
import requests
from pathlib import Path
import re
import webbrowser
import os

cap = cv2.VideoCapture(0)
toast = ToastNotifier()
font = cv2.FONT_HERSHEY_SIMPLEX
windowName = 'Qr Reader'
iconFolder = Path.joinpath(Path(__file__).resolve().parent, 'icons')
links = []

def scaledNumber(newMin, newMax, minimum, maximum, toScale):
    """Scales toMap between newMin and newMax while inversing the direction of the scale

    Args:
        newMin (float): New lower boundary
        newMax (float): New upper boundary
        minimum (float): Previous lower boundary
        maximum (float): Previous upper boundary
        toScale (float): Number to scale between newMin and newMax

    Returns:
        float: Scaled number
    """
    newNumber = (((newMin-newMax)*(float(toScale) - minimum))/(maximum - minimum)) + newMax
    if newNumber < newMin:
        return newMin
    elif newNumber > newMax:
        return newMax
    else:
        return newNumber


while True:
    success, frame = cap.read()
    frame = imutils.resize(frame,width=960,height=1080) 

    qrCodes = pyzbar.decode(frame)

    for qrCode in qrCodes:
        message = qrCode.data.decode('utf-8')

        #makes notification if it detects a link
        if 'http' in message or 'www' in message:   
            if message not in links:
                links.append(message)

                strippedMessage = re.sub('[/\\:*?\'\"<>|.]', '', message) + 'favicon.ico' 
                with open(Path.joinpath(iconFolder, strippedMessage), 'wb') as f:
                    f.write(requests.get(message + '/favicon.ico').content)  
                
                pyn(
                    title='QR Code Link',
                    description=message,
                    icon_path=str(Path.joinpath(iconFolder,strippedMessage)), # On Windows .ico is required, on Linux - .png
                    duration=10,                              # Duration in seconds
                    urgency=pyn.URGENCY_CRITICAL,
                    callback_on_click=lambda: webbrowser.open(message, new=0, autoraise=True)
                ).send()
        
        #dynamic bounding box
        corners = np.array(qrCode.polygon, np.int32)
        corners = corners.reshape((-1,1,2))
        cv2.polylines(frame, [corners], True, (255,0,100), 3)
        
        #static bounding box
        cornersFlat = qrCode.rect

        area = str(int(cornersFlat[2]) * int(cornersFlat[3]))
        fontScale = scaledNumber(.8,1,4000,220000,area)

        cv2.putText(frame, message, (cornersFlat[0], cornersFlat[1]-20), font, fontScale,(255, 240, 240), 3)      
        # cv2.putText(frame, str(area), (cornersFlat[0]+70, cornersFlat[1]+50), font, .9,(100, 100, 255), 2)
    
    cv2.imshow(windowName, frame)
    keyCode = cv2.waitKey(1)

    #Close when the window's 'X' button is clicked, or when the ESC button is pressed
    if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) <1 or keyCode ==27 :
        break

#delete downloaded favicons, may change how favicons are handled later
for files in os.listdir(str(iconFolder)):
    if files.endswith(".ico") or files.endswith(".png"):
        if os.path.isfile(str(Path.joinpath(iconFolder,files))) :
            os.remove(str(Path.joinpath(iconFolder,files)))
        else:
            #unnecessary?
            raise ValueError("{} is not a file.".format(str(Path.joinpath(iconFolder,files))))
    else:
        continue
cv2.destroyAllWindows()
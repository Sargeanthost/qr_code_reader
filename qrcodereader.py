#https://www.youtube.com/watch?v=-4MPtERPq2E
import cv2
import numpy as np
import imutils 
import pyzbar.pyzbar as pyzbar
import math

cap = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_SIMPLEX
windowName = 'Qr Reader'

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

    #Close when window's 'X' button is clicked, or ESC button is pressed
    if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) <1 or keyCode ==27 :
        break

cv2.destroyAllWindows()
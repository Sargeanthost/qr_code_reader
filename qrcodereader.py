from cv2 import VideoCapture, FONT_HERSHEY_SIMPLEX, polylines, putText, imshow, waitKey, destroyAllWindows, \
WND_PROP_VISIBLE, getWindowProperty
from numpy import array, int32
from imutils import resize
import pyzbar.pyzbar as pyzbar
from win10toast import ToastNotifier
from pynotifier import Notification as pyn
from requests import get
from pathlib import Path
from re import sub
from webbrowser import open as open_
from os import remove, listdir

cap = VideoCapture(0)
toast = ToastNotifier()
font = FONT_HERSHEY_SIMPLEX
windowName = "Qr Reader"
iconFolder = Path.joinpath(Path(__file__).resolve().parent, "icons")
links = []


def scaledNumber(newMin, newMax, minimum, maximum, toScale):
    """Inversely scale toMap to between newMin and newMax

    Args:
        newMin (float): New lower boundary
        newMax (float): New upper boundary
        minimum (float): Previous lower boundary
        maximum (float): Previous upper boundary
        toScale (float): Target number to scale between newMin and newMax

    Returns:
        float: Scaled number
    """
    newNumber = (((newMin - newMax) * (float(toScale) - minimum)) /
                 (maximum - minimum)) + newMax
    if newNumber < newMin:
        return newMin
    elif newNumber > newMax:
        return newMax
    else:
        return newNumber


while True:
    _, frame = cap.read()
    frame = resize(frame, width=960, height=1080)

    qrCodes = pyzbar.decode(frame)

    for qrCode in qrCodes:
        message = qrCode.data.decode("utf-8")

        # Currently only able to click the same website once per program instantiation.
        if "http" in message:
            if message not in links:
                links.append(message)

                # On Windows .ico is required, on Linux - .png
                strippedMessage = sub("[/\\:*?'\"<>|.]", "",
                                      message) + "favicon.ico"
                with open(Path.joinpath(iconFolder, strippedMessage),
                          "wb") as f:
                    f.write(get(message + "/favicon.ico").content)

                pyn(
                    title="QR Code Link",
                    description=message,
                    icon_path=str(
                        Path.joinpath(iconFolder, strippedMessage)
                    ),  # On Windows .ico is required, on Linux - .png
                    duration=10,
                    urgency=pyn.URGENCY_CRITICAL,
                    callback_on_click=lambda: open_(
                        message, new=0, autoraise=True),
                ).send()

        corners = array(qrCode.polygon, int32)
        corners = corners.reshape((-1, 1, 2))
        polylines(frame, [corners], True, (255, 0, 100), 3)

        cornersFlat = qrCode.rect

        area = str(int(cornersFlat[2]) * int(cornersFlat[3]))
        fontScale = scaledNumber(0.8, 1, 4000, 220000, area)

        putText(
            frame,
            message,
            (cornersFlat[0], cornersFlat[1] - 20),
            font,
            fontScale,
            (255, 240, 240),
            3,
        )

        putText(frame, message, (cornersFlat[0], cornersFlat[1] - 20), font,
                    fontScale, (255, 240, 240), 3)

    imshow(windowName, frame)
    keyCode = waitKey(1)

    if getWindowProperty(windowName,
                            WND_PROP_VISIBLE) < 1 or keyCode == 27:
        break

#delete downloaded favicons on close
for files in listdir(str(iconFolder)):
    if files.endswith(".ico") or files.endswith(".png"):
        remove(str(Path.joinpath(iconFolder, files)))
    else:
        continue

destroyAllWindows()

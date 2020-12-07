# Simple QR code reader for webcam on Windows

This is a simple qr code reader. It has a bounding box for each qr code it sees and scales text based on how close or far away the qr code is.

## **You will need to modify the pynotifier and win10toast libraries in order to click notifications.**

Look at my fork for pynotifier and copy the *pynotifier.py* file; place it into the folder named **pynotifier** in the location:

```path
~\python\lib\site-packages\pynotifier\
```

For win10Toast, copy the *\__init__* file from the fork, but instead go to:

```path
~\python\lib\site-packages\win10toast\
```

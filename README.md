# Simple QR code reader for webcam on Windows

This is a simple qr code reader. It has a bounding box for each qr code it sees and slightly scales text based on how close or far away the qr code is.

## **You will need to modify the pynotifier and win10toast libraries in order to maintain usability of the actionable toast in the *notification* branch.**

Look at my fork for pynotifier and copy the *pynotifier.py* file; place it into the folder named **pynotifier** in the location:

```path
C:\YOUR\PYTHON\INSTILLATION\LOCATION\python\lib\site-packages\pynotifier\
```

For win10Toast, copy *__init__* and *__main__*  from the fork, but instead go to:

```path
C:\YOUR\PYTHON\INSTILLATION\LOCATION\python\lib\site-packages\win10toast\
```


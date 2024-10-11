import cv2
import numpy as np
import winsound
import time
from threading import Thread

from datetime import datetime

cap = cv2.VideoCapture(0)

detected_motion=False
last_frame = 0
first_val = True
count = 0
f = open("TimeWhenMotionDetected.txt", "w")

def writeInFile():
    f.write(datetime.now().strftime("%H:%M:%S:%f"))
    f.write("\n")


def takeSnapshot(cont,myFrame):
    cv2.imwrite("frame%d.jpg" % cont, myFrame)



def playSound():
    winsound.PlaySound("SystemExclamation", winsound.SND_ASYNC | winsound.SND_ALIAS)

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while(True):
    ret, frame = cap.read()     ##current frame is set in variable frame (parameters: height, width, channels(=3 rgb)
    cv2.imshow('frame',frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  ##we transform the information from rgb to grayscale, grayscale image saved in gray as a numpy array

    ##calculate the difference between 2 frames
    motion = np.abs(np.mean(gray)-last_frame)
    last_frame=np.mean(gray)
    if first_val:     ##somehow for the first frame it always says that is in motion, so we skip it
        first_val = False
        pass
    else:

        if motion > 0.3:     ##we check the difference between the 2 frames

            print("TE MISTI!")
            count=count+1
            detected_motion=True
            playSound()
            writeInFile()
            takeSnapshot(count, frame)


        else:
            print("NU TE MISTI!")


        if(cv2.waitKey(1) & 0xFF == ord('q')):    ##close the app if 'q' button is pressed
            stop=time.time()
            break


cap.release()
cv2.destroyAllWindows()

from imutils.video import VideoStream
import cv2
import numpy as np
import imutils
import time


class Picture():
    def __init__(self):
        self.vs = VideoStream(srr=0).start()
        self.secounds = time.time()
        # stores the time that the picture should be taken at
        self.timeVec = []
        self.outputPicture


    def schedulePicture(self, delay):
        self.secounds.append(time.time() + delay)


    def takePicture(self):
        frame = self.vs.read()
        frame = imutils.resize(frame, width=400)


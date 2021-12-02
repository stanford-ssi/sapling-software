from imutils.video import VideoStream
#import cv2
import numpy as np
import imutils
import time


class Picture():
    def __init__(self):
        self.vs = VideoStream(srr=0).start()
        self.time = time.time()
        # stores the time that the picture should be taken at
        self.scheduledTimes = []
        self.frame

    def checkSchedule(self):
        if min(self.scheduledTimes) < time.time():
            self.scheduledTimes.remove(self.scheduledTimes.index(min_value))
            self.takePicture()

    def schedulePicture(self, delay):
        self.scheduledTimes.append(time.time() + delay)

    def takePicture(self):
        frame = self.vs.read()
        self.frame = frame

    def downsample(self, width=400):
        self.frame = imutils.resize(self.frame, width=width)

    def getPicture():
        return self.frame

if __name__=="__main__":
    picture = Picture()
    picture.takePicture()


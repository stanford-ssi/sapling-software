from imutils.video import VideoStream
import c2
import numpy as np
import imutils
import time
import asyncio


class Camea():
    def __init__(self):
        self.vs = VideoStream(srr=0).start()
        self.time = time.time()
        # stores the time that the picture should be taken at
        self.scheduledTimes = []
        self.frame

    #def checkSchedule(self):
    #    if min(self.scheduledTimes) < time.time():
    #        self.scheduledTimes.remove(self.scheduledTimes.index(min_value))
    #        self.takePicture()

    def take_scheduled_picture(self, delay):
        await asyncio.sleep(delay)
        self.frame = self.vs.read()
        
        #self.scheduledTimes.append(time.time() + delay)

    def take_picture(self):
        self.frame = self.vs.read()

    def downsample(self, width=400):
        self.frame = imutils.resize(self.frame, width=width)

    def get_picture():
        return self.frame

if __name__=="__main__":
    picture = Picture()
    picture.takePicture()
    frame = picture.getPicture()

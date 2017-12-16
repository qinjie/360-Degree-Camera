import os
import numpy as np
import urllib
import cv2
import base64
import time
import requests
import datetime
import math
import imutils

# Initization Parameter
BSIZE = 12 #size of each block | default: 12
T0 = 20 # expected begin value | default: 15
# Observation Window Config Parameter
Nmid = 75 # Observation Size | default: 75
Nsw = 5 # Segment Counter | default: 5 (Nmid / Nsz)
Nsz = 15 # Size of Each Segment | default: 15

Imt = 0.2  # default: 0.2
Ins = 0.5 # default: 0.5
Ivt = 0.4  # default: 0.4

# Others
lastMB = []

OB_x = 1
OB_y = 0

class MathHelper(object):
    def getValueVector(self, x, y, z):
        return math.sqrt(x * x + y * y + z * z)

    def getMean(self, x, y, z):
        return  (x + y + z) / 3.0


class Wood(object):
    def __init__(self, h, w):
        self.x = [[0 for x in range(w)] for y in range(h)]

    def __get__(self, i, j):
        return self.x[i][j]

    def __set__(self, i, j, value):
        self.x[i][j] = value


class Queue(object):
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.x = [Wood(h, w) for x in range(Nmid)] # for MID
        self.y = [Wood(h, w) for x in range(Nsz)] # for AMID
        self.xfront = 0
        self.yfront = Nsz - 1
        self.yrear = 0

    def add(self, newWood):
        tmp = self.get()
        for i in range(self.h):
            for j in range(self.w):
                tmp.x[i][j] = tmp.x[i][j] + newWood.x[i][j]


        self.xfront = (self.xfront + 1) % Nmid

        for i in range(self.h):
            for j in range(self.w):
                self.x[self.xfront].x[i][j] = tmp.x[i][j]

        self.yrear = (self.yrear + 1) % Nsz
        self.yfront = (self.yfront + 1) % Nsz

        for i in range(self.h):
            for j in range(self.w):
                self.y[self.yfront].x[i][j] = newWood.x[i][j]

    def get(self):
        newWood = Wood(self.h, self.w)
        for i in range(self.h):
            for j in range(self.w):
                newWood.x[i][j] = 0

        for i in range(self.h):
            for j in range(self.w):
                newWood.x[i][j] = self.x[self.xfront].x[i][j] - self.y[self.yrear].x[i][j]
        return newWood

    def getLastAMID(self):
        cp = Wood(self.h, self.w)
        for i in range(0, self.h):
            for j in range(0, self.w):
                cp.x[i][j] = self.x[self.xfront].x[i][j]
        return cp

class PQueue(object):
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.x = [Wood(h, w) for x in range(Nmid)] #AMID series
        self.front = 0

    def addAMID(self, newWood):
        self.front = (self.front + 1) % Nmid
        for i in range(self.h):
            for j in range(self.w):
                self.x[self.front].x[i][j] = newWood.x[i][j]

    def getProbSeries(self):
        set = []
        sum = Wood(self.h, self.w)
        for fr in range(0, Nmid, Nsz):
            pos = (self.front - fr + Nmid) % Nmid
            for i in range(self.h):
                for j in range(self.w):
                    sum.x[i][j] = sum.x[i][j] + self.x[pos].x[i][j]


        for fr in range(0, Nmid, Nsz):
            pos = (self.front - fr + Nmid) % Nmid
            newP = Wood(self.h, self.w)
            for i in range(self.h):
                for j in range(self.w):
                    if sum.x[i][j] > 0:
                        newP.x[i][j] = 1.0 * self.x[pos].x[i][j] / sum.x[i][j]

            set.append(newP)

        return set

    def run(self, img):
        detect = 0
        set = self.getProbSeries()

        # basic variable
        Smt0 = 1.0 * (Nsw + 1) / 2
        Svt0 = 1.0 * (Nsw * Nsw - 1) / 12
        Sns0 = Nsw

        count = 0
        for i in range(self.h):
            for j in range(self.w):
                Smt = 0.0
                Svt = 0.0
                Sns = 0.0
                for l in range(Nsw):
                    #print l
                    Smt = Smt + (Nsw - l) * set[l].x[i][j] # Expected value
                    if set[l].x[i][j] > 0: Sns = Sns + 1


                for l in range(Nsw):
                    Svt = Svt + (Nsw - Smt) * (Nsw - Smt) * set[l].x[i][j]

                Smt_av = Imt * Nsw
                Sns_av = Ins * Sns0
                Svt_av = Ivt * Svt0

                x = i * BSIZE
                y = j * BSIZE
                u = x + BSIZE - 1
                v = y + BSIZE - 1
                if abs(Smt - Smt0) < Smt_av and Svt > Svt_av and Sns > Sns_av:

                    if x >= 20 and u <= 220:
                        cv2.rectangle(img,(j * BSIZE, i * BSIZE), (j * BSIZE + BSIZE - 1, i * BSIZE + BSIZE - 1),(0,255,0), 2)
                        detect = detect + 1
                if x >= 20 and u <= 220: count = count + 1
        #print "moving point = ", detect

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'Density: {0:.2f}'.format(100.0 * detect / count),(20, 200), font, 0.5, (255,255,255), 1,cv2.LINE_AA)
        print "working "

# GLOBAL VARIABLE
ScreenH = 320 / BSIZE + ((320 % BSIZE) % 2)# 320 / 12
ScreenW = 240 / BSIZE + ((240 % BSIZE) % 2)# 240 / 12
AM_Queue = Queue(ScreenW, ScreenH)
P_Queue = PQueue(ScreenW, ScreenH)

# Add one image (frame) to process
def addImg(img):
    arr = np.array(img)
    h, w = img.shape[:2]

    subH = h // BSIZE
    subW = w // BSIZE

    # if last MB is not exist: create one
    if h % BSIZE != 0: subH = subH + 1
    if w % BSIZE != 0: subW = subW + 1

    newMID = Wood(subH, subW)

    if len(lastMB) == 0:
        for i in range(0, h, BSIZE):
            tmp = []
            for j in range(0, w, BSIZE):
                tmp.append([0.0, 0.0, 0.0])
            lastMB.append(tmp)

    # compute MID array
    for i in range(0, h, BSIZE):
        for j in range(0, w, BSIZE):
            x = 0.0
            y = 0.0
            z = 0.0
            for u in range(0, BSIZE):
                for v in range(0, BSIZE):
                    if (i + u < h) and (j + v < w): # must be inside of image
                        x += arr[i + u][j + v][0]
                        y += arr[i + u][j + v][1]
                        z += arr[i + u][j + v][2]

            x = x  / (BSIZE * BSIZE)
            y = y  / (BSIZE * BSIZE)
            z = z  / (BSIZE * BSIZE)
            delX = x
            delY = y
            delZ = z
            try:
                delX = x - lastMB[i / BSIZE][j / BSIZE][0]
                delY = y - lastMB[i / BSIZE][j / BSIZE][1]
                delZ = z - lastMB[i / BSIZE][j / BSIZE][2]
            except:
                print i, j

            Tt = T0 * (1 + (MathHelper().getMean(x, y, z) - 127) / 255) # base value

            lastMB[i / BSIZE][j / BSIZE] = [x, y, z]
            if MathHelper().getValueVector(delX, delY, delZ) >= Tt:
                midValue = 1
            else:
                midValue = 0

            newMID.x[i / BSIZE][j / BSIZE] = midValue

        # add MID to AMID queue
        AM_Queue.add(newMID)
        # add AMID to P-queue
        P_Queue.addAMID(AM_Queue.getLastAMID())
    # run the analysis
    P_Queue.run(img)



DIR_CAM01 = '../Data/Crowd_Analysis/Cam01_1/cam01_{}.jpg'
DIR_CAM02 = '../Data/Crowd_Analysis/Cam01_2/cam01_{}.jpg'
DIR_CAM03 = '../Data/Crowd_Analysis/Cam01_3/cam01_{}.jpg'
DIR_CAM04 = '../Data/Crowd_Analysis/Cam02_1/cam02_{}.jpg'
DIR_PANO = '../Data/Crowd_Analysis/Pano/pano_{}.jpg'
MIN_INDEX = 1
MAX_INDEX = 100

import sys
sys.path.append('../')

from ImageHelper.image_helper import ImageProcessing
ip = ImageProcessing()

if __name__ == "__main__":

    i = MIN_INDEX
    while True:
            print "turn ", i, ": "

            result = cv2.imread(DIR_PANO.format(i))
            crop_img_cam01 = cv2.imread(DIR_CAM01.format(i))
            crop_img_cam02 = cv2.imread(DIR_CAM02.format(i))
            crop_img_cam03 = cv2.imread(DIR_CAM03.format(i))
            crop_img_cam04 = cv2.imread(DIR_CAM04.format(i))

            result = cv2.resize(result, (320, 240))
            result = cv2.cvtColor(result,cv2.COLOR_RGBA2RGB)

            addImg(result)

            #crop_img_cam01 = imutils.rotate_bound(crop_img_cam01, 90)
            crop_img_cam01 = cv2.cvtColor(crop_img_cam01,cv2.COLOR_RGBA2RGB)
            crop_img_cam02 = cv2.cvtColor(crop_img_cam02,cv2.COLOR_RGBA2RGB)
            crop_img_cam03 = cv2.cvtColor(crop_img_cam03,cv2.COLOR_RGBA2RGB)
            crop_img_cam04 = cv2.cvtColor(crop_img_cam04,cv2.COLOR_RGBA2RGB)

            # demo for 4-camera
            all_image = ip.concatFour(result, crop_img_cam01, crop_img_cam02, crop_img_cam03, crop_img_cam04)

            # demo for 2-camera
            #all_image = ip.concatTwo(result, crop_img_cam01, crop_img_cam02)

            # show the result
            cv2.imshow("Camera 360 Project", all_image)

            cv2.waitKey(1)
            time.sleep(1.0 / 24)
            i = i + 1
            if i == MAX_INDEX:
                i = MIN_INDEX

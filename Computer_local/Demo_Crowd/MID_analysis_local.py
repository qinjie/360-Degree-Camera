import os
import numpy as np
import urllib
import cv2
import base64
import time
import requests
import datetime
# stitcher
from Panorama.panorama import Stitcher
from Panorama.utilsImage import load_image
from Panorama.transform import *
import math

# Initization Parameter
BSIZE = 12
T0 = 50
lastMB = []

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

# Add one image (frame) to process
def addImg(img, firstTime):
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
                if i >= 20 and i + BSIZE - 1 <= 220 and firstTime:
                    cv2.rectangle(img,(j, i), (j + BSIZE - 1, i + BSIZE - 1),(0,255,0), 2)
            else:
                midValue = 0

            newMID.x[i / BSIZE][j / BSIZE] = midValue


MIN_INDEX = 1
MAX_INDEX = 92
PANO_DIR = '../Data/Demo MID Analysis/Pano/cam{}.jpg'
DELAY = 5000

if __name__ == "__main__":

    firstTime = False
    for i in range(MIN_INDEX, MAX_INDEX + 1, 1):
        im = cv2.imread(PANO_DIR.format(i))
        addImg(im, firstTime)
        firstTime = True
        cv2.imshow("360 Camera", im)
        print "Finish frame:", i
        cv2.waitKey(DELAY)



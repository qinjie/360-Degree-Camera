import os
import numpy as np
import urllib
import cv2
import base64
import time
import requests
import datetime
# stitcher
import sys
sys.path.append('../')

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

    #initialization of lastMB which is a 3x1 zero vector for each block(i,j)
    #3x1 dimension because each pixel has R, G, B value
    if len(lastMB) == 0:
        for i in range(0, h, BSIZE):
            tmp = []
            for j in range(0, w, BSIZE):
                tmp.append([0.0, 0.0, 0.0])
            lastMB.append(tmp)

    tot = 0
    det = 0
    # compute MID array
    # block (i,j)
    # MID_{i,j} = sum_{u,v}(Image[u,v]) is to sum up the RGB value for all pixels in the block(i,j)

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

            # initialize
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
                # [0, 20] is tile part [220, 240] is the bottom to show density value
                # for demo
                if i >= 20 and i + BSIZE - 1 <= 220 and not firstTime:
                    cv2.rectangle(img,(j, i), (j + BSIZE - 1, i + BSIZE - 1),(0,255,0), 2)
                    det = det + 1
            else:
                midValue = 0

            if i >= 20 and i + BSIZE - 1 <= 220 and not firstTime:
                tot = tot + 1
            newMID.x[i / BSIZE][j / BSIZE] = midValue
    result = 0;
    if not firstTime:
        result = 100.0 * det / tot
        
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'Density: {0:.2f}'.format(result),(20, 230), font, 0.5, (255,255,255), 1,cv2.LINE_AA)
    return result

def analysis_two_pano(im1, im2):
    lastMB = []
    im1 = cv2.resize(im1, (320, 240))
    im2 = cv2.resize(im2, (320, 240))
    
    addImg(im1, True)
    result = addImg(im2, False)
    #print("Store Image analysised")
    #cv2.imwrite('../Data',im2)
    
    return result

MIN_INDEX = 1
MAX_INDEX = 100
DIR_PANO = '../Data/Crowd_Analysis/Pano/pano_{}.jpg'
DIR_CAM01 = '../Data/Crowd_Analysis/Cam01_1/cam01_{}.jpg'
DIR_CAM02 = '../Data/Crowd_Analysis/Cam01_2/cam01_{}.jpg'
DIR_CAM03 = '../Data/Crowd_Analysis/Cam01_3/cam01_{}.jpg'
DIR_CAM04 = '../Data/Crowd_Analysis/Cam02_1/cam02_{}.jpg'
DELAY = 3000

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

            crop_img_cam01_2 = cv2.imread(DIR_CAM01.format((i + 1)))
            crop_img_cam02_2 = cv2.imread(DIR_CAM02.format((i + 1)))
            crop_img_cam03_2 = cv2.imread(DIR_CAM03.format((i + 1)))
            crop_img_cam04_2 = cv2.imread(DIR_CAM04.format((i + 1)))
            
            im1_1 = cv2.resize(crop_img_cam01, (320, 240))
            im2_1 = cv2.resize(crop_img_cam02, (320, 240))
            im3_1 = cv2.resize(crop_img_cam03, (320, 240))
            im4_1 = cv2.resize(crop_img_cam04, (320, 240))
            
            im1_2 = cv2.resize(crop_img_cam01_2, (320, 240))
            im2_2 = cv2.resize(crop_img_cam02_2, (320, 240))
            im3_2 = cv2.resize(crop_img_cam03_2, (320, 240))
            im4_2 = cv2.resize(crop_img_cam04_2, (320, 240))
            
            addImg(im1_1, True)
            res1 = addImg(im1_2, False)
            lastMB = []
            
            addImg(im2_1, True)
            res2 = addImg(im2_2, False)
            lastMB = []
            
            addImg(im3_1, True)
            res3 = addImg(im3_2, False)
            lastMB = []
            
            addImg(im4_1, True)
            res4 = addImg(im4_2, False)
            lastMB = []
            
            motion = (res1 + res2 + res3 + res4)/4
            print("Result: res1 = %d, res2 = %d, res3 = %d, res4= %d",motion , res1, res2, res3, res4)
            result = cv2.resize(result, (320, 240))
            result = cv2.cvtColor(result,cv2.COLOR_RGBA2RGB)
            
            im1_2 = cv2.cvtColor(im1_2,cv2.COLOR_RGBA2RGB)
            im2_2 = cv2.cvtColor(im2_2,cv2.COLOR_RGBA2RGB)
            im3_2 = cv2.cvtColor(im3_2,cv2.COLOR_RGBA2RGB)
            im4_2 = cv2.cvtColor(im4_2,cv2.COLOR_RGBA2RGB)
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            #cv2.putText(result,'Density: {0:.2f}'.format(motion),(20, 200), font, 0.5, (255,255,255), 2,cv2.LINE_AA)
            
            # demo for 4-camera
            all_image = ip.concatFour(result, im1_2, im2_2, im3_2, im4_2)

            # demo for 2-camera
            #all_image = ip.concatTwo(result, crop_img_cam01, crop_img_cam02)

            # show the result
            cv2.imshow("Camera 360 Project", all_image)

            cv2.waitKey(1)
            time.sleep(1.0 / 24)
            i = i + 1
            if i == MAX_INDEX:
                i = MIN_INDEX



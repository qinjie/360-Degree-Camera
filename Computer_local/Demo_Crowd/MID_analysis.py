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
def addImg(img):
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
                if i >= 20 and i + BSIZE - 1 <= 220:
                    cv2.rectangle(img,(j, i), (j + BSIZE - 1, i + BSIZE - 1),(0,255,0), 2)
                    det = det + 1
            else:
                midValue = 0

            if i >= 20 and i + BSIZE - 1 <= 220:
                tot = tot + 1
            newMID.x[i / BSIZE][j / BSIZE] = midValue

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'Density: {0:.2f}'.format(100.0 * det / tot),(20, 230), font, 0.5, (255,255,255), 1,cv2.LINE_AA)

# 1. FETCH IMAGE
HOST = '192.168.2.71:8080'
URL = 'http://{}/?action=snapshot'.format(HOST)


from ImageHelper.image_helper import ImageProcessing
ip = ImageProcessing()
#from Testing.stitching_new import Stitcher

if __name__ == "__main__":

    while True:
        img = ip.url_to_image(URL)
        # CROP [ y : y + height , x : x + width ]
        beginX = 0
        beginY = 32
        imW = 640
        imH = 480

        crop_img_cam01 = img[beginY:beginY + imH, beginX:beginX + imW]
        crop_img_cam02 = img[beginY:beginY + imH, beginX + imW:beginX + imW + imW]
        #crop_img_cam03 = img[beginY + imH:beginY + imH + imH, beginX:beginX + imW]
        #crop_img_cam04 = img[beginY + imH:beginY + imH + imH, beginX + imW:beginX + imW + imW]

        # rorate if neccessary
        crop_img_cam01 = ip.rorate(crop_img_cam01, 180)
        crop_img_cam02 = ip.rorate(crop_img_cam02, 180)

        cv2.imwrite("cam01.jpg", crop_img_cam01)
        cv2.imwrite("cam02.jpg", crop_img_cam02)

        begin_time = datetime.datetime.now()

        try:

            # give list of images
            _images = ["cam02.jpg", "cam01.jpg"]

            # add to list
            images = []
            for _image in _images:
                images.append(load_image(_image))


            stitcher = Stitcher()
            result, kps, features, deg = stitcher.stitch([images[0], images[1]], firstTime=True)

            for idx in range(2, len(images)):
                stitcher = Stitcher()
                result, kps, features, deg = stitcher.stitch([result, images[idx]],
                                                     firstTime=False, l_ori_kps=kps,
                                                     l_features=features, l_deg=deg)

            print 'Elapsed time:', datetime.datetime.now() - begin_time


            '''
            # another way
            img1 = cv2.imread("cam02.jpg")
            img2 = cv2.imread("cam01.jpg")
            stitcher = Stitcher()
            (result, vis) = stitcher.stitch([img1, img2], showMatches=True) '''

            # resize for analysis
            result = cv2.resize(result, (320, 240))

            #convert color
            result = cv2.cvtColor(result,cv2.COLOR_RGBA2RGB)
            crop_img_cam01 = cv2.cvtColor(crop_img_cam01, cv2.COLOR_RGBA2RGB)
            crop_img_cam02 = cv2.cvtColor(crop_img_cam02, cv2.COLOR_RGBA2RGB)

            #mid analysis
            addImg(result)

            #concat
            all_image = ip.concatTwo(result, crop_img_cam01, crop_img_cam02)

            #showing
            cv2.imshow("Camera 360 Project", all_image)

            cv2.waitKey(1)

            print "done!"
        except Exception as e:
            print(e)

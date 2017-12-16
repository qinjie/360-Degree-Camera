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
# image processing
from ImageHelper.image_helper import ImageProcessing

# 1. FETCH IMAGE
HOST = '192.168.2.71:8080'
URL = 'http://{}/?action=snapshot'.format(HOST)

def url_to_image(url):
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

if __name__ == "__main__":
    ip = ImageProcessing()
    firstTime = False
    firstFrame = np.zeros((320, 240, 3), np.uint8)

    cnt = 1
    while True:
        img = url_to_image(URL)
        # CROP [ y : y + height , x : x + width ]
        beginX = 0
        beginY = 32
        imW = 640
        imH = 480
        crop_img_cam01 = img[beginY:beginY + imH, beginX:beginX + imW]
        crop_img_cam03 = img[beginY:beginY + imH, beginX + imW:beginX + imW + imW]

        cv2.imwrite("cam01.jpg", crop_img_cam01)
        cv2.imwrite("cam02.jpg", crop_img_cam03)
        begin_time = datetime.datetime.now()

        try:
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

            # resize the result
            result = cv2.resize(result, (320, 240))
            result = cv2.cvtColor(result,cv2.COLOR_RGBA2RGB)

            # convert to gray image
            gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if first time
            if firstTime == False:
                firstFrame = gray
                firstTime = True
                print "finish first time"
                continue

            print "second time"
            # delta with first frame
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            im2, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # draw contours
            for c in cnts:
                rect = cv2.boundingRect(c)
                #if rect[2] < 20 or rect[3] < 100: continue


                (x, y, w, h) = cv2.boundingRect(c)
                result = cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # convert image to right format + right direction
            result = cv2.cvtColor(result,cv2.COLOR_RGBA2RGB)
            crop_img_cam01 = cv2.cvtColor(crop_img_cam01,cv2.COLOR_RGBA2RGB)
            crop_img_cam03 = imutils.rotate_bound(crop_img_cam03, -90)
            crop_img_cam03 = cv2.cvtColor(crop_img_cam03,cv2.COLOR_RGBA2RGB)

            # concate all image to one
            all_image = ip.concatTwo(result, crop_img_cam01, crop_img_cam03)
            # show the image
            cv2.imshow("Camera 360 Project", all_image)
            # wait for showing
            cv2.waitKey(1)
            # notificatiion
            print "done!"
        except Exception as e:
            print(e)



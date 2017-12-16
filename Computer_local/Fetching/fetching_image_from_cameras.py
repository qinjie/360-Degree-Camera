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

path = os.path.dirname(os.path.realpath(__file__))

HOST = '192.168.1.22:8080'
URL = 'http://{}/?action=snapshot'.format(HOST)
DIR_CAM01 = path + '/../Data/Crowd_Analysis/Cam01_4/cam01_{}.jpg'
DIR_CAM02 = path + '/../Data/Crowd_Analysis/Cam02_1/cam02_{}.jpg'
DIR_CAM03 = path + '/../Data/Crowd_Analysis/Cam03_4/cam03_{}.jpg'
DIR_CAM04 = path + '/../Data/Crowd_Analysis/Cam04_4/cam04_{}.jpg'
MIN_INDEX = 1
MAX_INDEX = 100

def url_to_image(url):
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def fetching(min_index, max_index):
    for i in range(min_index, max_index + 1, 1):
        # fetching image
        img = url_to_image(URL)
        # CROP [ y : y + height , x : x + width ]
        beginX = 0
        beginY = 32
        imW = 640 # width of image
        imH = 480 # heigth of image
        # SPLIT INTO FOUR IMAGE
        crop_img_cam01 = img[beginY:beginY + imH, beginX:beginX + imW]
        crop_img_cam04 = img[beginY:beginY + imH, beginX + imW:beginX + imW + imW]
        crop_img_cam02 = img[beginY + imH:beginY + imH + imH, beginX:beginX + imW]
        crop_img_cam03 = img[beginY + imH:beginY + imH + imH, beginX + imW:beginX + imW + imW]
        
        #rotate image 180 Degree
        crop_img_cam01 = imutils.rotate(crop_img_cam01, 180)
        crop_img_cam02 = imutils.rotate(crop_img_cam02, 180)
        crop_img_cam03 = imutils.rotate(crop_img_cam03, 180)
        crop_img_cam04 = imutils.rotate(crop_img_cam04, 180)
        
        # write to dir
        cv2.imwrite(DIR_CAM01.format(i), crop_img_cam01)
        cv2.imwrite(DIR_CAM02.format(i), crop_img_cam02)
        cv2.imwrite(DIR_CAM03.format(i), crop_img_cam03)
        cv2.imwrite(DIR_CAM04.format(i), crop_img_cam04)
        # sleep
        time.sleep(10 / 24) # usually speed of camera
        print 'done ', i

def rotate_image(path, degree):
    #read image
    img = cv2.imread(path)
    img = imutils.rotate(img, degree)
    cv2.imwrite(path, img)

def rotate_images(min_index, max_index):
    for i in range(min_index, max_index + 1, 1):
        rotate_image(DIR_CAM01.format(i),180)
        rotate_image(DIR_CAM02.format(i),180)
        rotate_image(DIR_CAM03.format(i),180)
        rotate_image(DIR_CAM04.format(i),180)
        print("done 1 round")

if __name__ == "__main__":
    #Fetching Image -- Image already rotate, no need for rotate below
    fetching(MIN_INDEX, MAX_INDEX)
    #rotate_images(MIN_INDEX, MAX_INDEX)
    print("Main")
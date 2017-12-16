import os
import numpy as np
import urllib
import cv2
import base64
import time
import requests
import datetime

path = os.path.dirname(os.path.realpath(__file__))

import sys
sys.path.append(path + '/../')

# stitcher
from Panorama.panorama import Stitcher
# web_services
from Panorama.utilsImage import load_image
from Panorama.transform import *
import math

# directory
DIR_CAM01 = path + '/' + '../Data/Crowd_Analysis/Cam01_1/cam01_{}.jpg'
DIR_CAM02 = path + '/' + '../Data/Crowd_Analysis/Cam01_2/cam01_{}.jpg'
DIR_CAM03 = path + '/' + '../Data/Crowd_Analysis/Cam01_3/cam01_{}.jpg'
DIR_CAM04 = path + '/' + '../Data/Crowd_Analysis/Cam02_1/cam02_{}.jpg'

DIR_PANO = '../Data/Crowd_Analysis/Pano/pano_{}.jpg'

MIN_INDEX = 1
MAX_INDEX = 100

if __name__ == "__main__":

    k = 0;
    for i in range(MIN_INDEX, MAX_INDEX + 1, 1):
        try:
            _images = []
            _images.append(DIR_CAM01.format(i))
            _images.append(DIR_CAM02.format(i))
            _images.append(DIR_CAM03.format(i))
            _images.append(DIR_CAM04.format(i))
            
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

            k = k + 1
            
            #put Text
            #font = cv2.FONT_HERSHEY_SIMPLEX
            #cv2.putText(result,'Panorama',(20, 70), font, 3 , (0,0,255), 3, cv2.LINE_AA)
            
            cv2.imwrite(DIR_PANO.format(i), result)
            print 'done ', i
        except Exception as e:
            print(e)

import sys
#sys.path.append('../')
#sys.path.append('../package')
import os

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path + '/..')
sys.path.append(path + '/../package')

import numpy as np
import urllib
import cv2
import base64
import time
import requests
import datetime

# stitcher
from Panorama.panorama import Stitcher
# web_services
from Panorama.utilsImage import load_image
from Panorama.transform import *
import math

# directory
DIR_CAM01 = path + '/../Data/Cam01/cam01_{}.jpg'
DIR_CAM02 = path + '/../Data/Cam02/cam02_{}.jpg'
DIR_CAM03 = path + '/../Data/Cam03/cam03_{}.jpg'
DIR_CAM04 = path + '/../Data/Cam04/cam04_{}.jpg'
DIR_PANO = path + '/../Data/Pano/pano_{}.jpg'

MIN_INDEX = 1
MAX_INDEX = 1

def stitching(camera_id):
    for i in range(MIN_INDEX, MAX_INDEX + 1, 1):
        try:
            _images = []
            _images.append(DIR_CAM01.format(camera_id))
            _images.append(DIR_CAM02.format(camera_id))
	    _images.append(DIR_CAM03.format(camera_id))
	    _images.append(DIR_CAM04.format(camera_id))
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
	    # put Text
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(result,'Pano' + str(datetime.datetime.now()),(20, 70), font, 2 , (0,0,255), 3, cv2.LINE_AA)
            cv2.imwrite(DIR_PANO.format(camera_id), result)
            print 'done ', i
        except Exception as e:
            print(e)

if __name__ == "__main__":
    stitching(1)

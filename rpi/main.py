import os

import numpy as np
import urllib
import cv2
import base64
import time
import requests

# 1. FETCH IMAGE
from rpi.api_helper import ApiHelper

URL = 'http://192.168.2.71:8080/?action=snapshot'


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image


image_array = url_to_image(URL)
file_name = 'camera01.jpg'
_path_cur_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(_path_cur_dir, file_name)
cv2.imwrite(file_path, image_array)

# #2. STITCHING
# TODO

# #3. PUT METHOD
api = ApiHelper()
try:
    api.uploadImageBase64(file_path)
except Exception as e:
    print e

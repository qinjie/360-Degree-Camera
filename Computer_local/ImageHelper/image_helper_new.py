import numpy as np
import cv2
import imutils
import urllib

class ImageProcessing:

    def resize(self, img, w, h):
        return cv2.resize(img, (w, h))

    def rorate(self, img, angle):
        return imutils.rotate_bound(img, angle)

    def concatTwo(self, pano, cam01, cam02):
        # resize to fix whole image
        pano = cv2.resize(pano, (480, 360))
        cam01 = cv2.resize(cam01, (230, 175))
        cam02 = cv2.resize(cam02, (230, 175))
        # insert text to image
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(pano,'Panorama',(20, 20), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(cam01,'CAM 01',(20, 20), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(cam02,'CAM 02',(20, 20), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
        # make the big one
        all_image = np.zeros((370, 725, 3), np.uint8)
        all_image[5:365,5:485] = pano
        all_image[5:180, 490:720] = cam01
        all_image[185:360, 490:720] = cam02
        return all_image

    def concatFour(self, pano, cam01, cam02, cam03, cam04):
        #resize to fix whole image
        high = 200
        width = 260
        cam01 = cv2.resize(cam01, (width, high))
        cam02 = cv2.resize(cam02, (width, high))
        cam03 = cv2.resize(cam03, (width, high))
        cam04 = cv2.resize(cam04, (width, high))
        pano = cv2.resize(pano, (4*width, high))
        # insert text to image
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(pano,'Panorama',(20, 20), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(cam01,'CAM 01',(20, 20), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(cam02,'CAM 02',(20, 20), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(cam03,'CAM 03',(20, 20), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(cam04,'CAM 04',(20, 20), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
        # make the big one
        
        all_image = np.zeros((2*high + 15, 4*width + 25, 3), np.uint8)
        all_image[5:high+5, 5:4*width + 5] = pano
        all_image[high + 10: 2*high + 10, 5:width+5] = cam01
        all_image[high + 10: 2*high + 10, width + 2*5 : 2*width + 2*5] = cam02
        all_image[high + 10: 2*high + 10, 2*width + 3*5 : 3*width + 3*5] = cam03
        all_image[high + 10: 2*high + 10, 3*width + 4*5 : 4*width + 4*5] = cam04

        return all_image

    def loadParamImg(self, path, param):
        return cv2.imread(path.format(param))

    def loadSingleImg(self, path):
        return cv2.imread(path)

    def url_to_image(self, url):
        # download the image, convert it to a NumPy array, and then read
        # it into OpenCV format
        resp = urllib.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image

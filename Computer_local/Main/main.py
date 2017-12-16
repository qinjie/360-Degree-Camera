import time
import sys
import os
import json
import requests
import shutil #For copy of testing only

path = os.path.dirname(os.path.realpath(__file__))

sys.path.append(path + '/../Upload_S3')
sys.path.append(path + '/../Fetching')
sys.path.append(path + '/../Sqs_sender')

BASE_URL = "https://jyf7s0ji3m.execute-api.ap-southeast-1.amazonaws.com/dev/"
KEY_PREFIX = "360-degree-camera/"

PROJECT_NAME = "360 Degree Camera"
CAMERA_NAME = "001"
CAMERA_ID = 1
ACTION = ["stitch", "montion-analysis"]
OUTPUT = "panorama"
BUCKET = "iot-centre-projects"

PATH_ACTION_UPLOAD = "s3_signed_url/upload"
PATH_ACTION_DOWNLOAD = "s3_signed_url/download"

from upload_S3 import s3_signed_upload
from fetching_image_from_cameras import fetching, rotate_images
from Sqs_sender import sqs_sender, api_sqs_sender

MIN_INDEX = 1
MAX_INDEX = 100

def prepare_sqs_sender(cam01_key, cam02_key, cam03_key, cam04_key):
    #Send sqs message
    message = '{ "project": "'+ PROJECT_NAME +'", "camera_id": "'+ str(CAMERA_ID) +'", "camera_name": "'+ CAMERA_NAME +'", "action": '+ json.dumps(ACTION) +', "bucket": "'+ BUCKET +'", "output": "'+ OUTPUT +'", "key_prefix": "'+ KEY_PREFIX +'", "input" : {"cam01_key": "' + cam01_key + '", "cam02_key": "' + cam02_key + '", "cam03_key": "' + cam03_key + '","cam04_key": "' + cam04_key + '"}}'
    
    #Send direct to Queue but not good solutions.
    #url = 'https://sqs.ap-southeast-1.amazonaws.com/498107424281/DatntQueue'
    #r = sqs_sender(url, message)
    
    #Send to service api for sending message to Queue
    url = 'https://ipdic6z2s8.execute-api.ap-southeast-1.amazonaws.com/api/sqs'
    r = api_sqs_sender(url, message)
    print("Sent message to sqs: " + message);

index = 0
if __name__ == '__main__':
    while True:
        #fetching on really device
        #fetching(MIN_INDEX, MAX_INDEX)
        # Calling function fetching here and store to ../Data/Crowd_Analysis/Cam0x/cam0x_x.jpg
        
        #emulator fetching from folder
        print("Copying")
        index += 4
        if index >= 100: index = 1
        shutil.copyfile(path + '/../Data/Crowd_Analysis/Cam01_1/cam01_{}.jpg'.format(index), path + '/../Data/Crowd_Analysis/Cam01/cam01_1.jpg');
        shutil.copyfile(path + '/../Data/Crowd_Analysis/Cam01_2/cam01_{}.jpg'.format(index), path + '/../Data/Crowd_Analysis/Cam02/cam02_1.jpg');
        shutil.copyfile(path + '/../Data/Crowd_Analysis/Cam01_3/cam01_{}.jpg'.format(index), path + '/../Data/Crowd_Analysis/Cam03/cam03_1.jpg');
        shutil.copyfile(path + '/../Data/Crowd_Analysis/Cam02_1/cam02_{}.jpg'.format(index), path + '/../Data/Crowd_Analysis/Cam04/cam04_1.jpg');
        # This send for Unit 2 ( Change CAMERA_ID = 2 and CAMERA_NAME = "001" before uncomment to sent)
        '''shutil.copyfile(path + '/../Data/Crowd_Analysis_Unit2/Cam01/cam01_2.jpg'.format(index), path + '/../Data/Crowd_Analysis/Cam01/cam01_2.jpg');
        shutil.copyfile(path + '/../Data/Crowd_Analysis_Unit2/Cam02/cam02_2.jpg'.format(index), path + '/../Data/Crowd_Analysis/Cam02/cam02_2.jpg');
        shutil.copyfile(path + '/../Data/Crowd_Analysis_Unit2/Cam03/cam03_2.jpg'.format(index), path + '/../Data/Crowd_Analysis/Cam03/cam03_2.jpg');
        shutil.copyfile(path + '/../Data/Crowd_Analysis_Unit2/Cam04/cam04_2.jpg'.format(index), path + '/../Data/Crowd_Analysis/Cam04/cam04_2.jpg');'''
        #rotate_images(MIN_INDEX, MAX_INDEX)

        cam01_key, cam02_key, cam03_key, cam04_key = s3_signed_upload(BASE_URL, KEY_PREFIX, PATH_ACTION_UPLOAD, CAMERA_ID)
        prepare_sqs_sender(cam01_key, cam02_key, cam03_key, cam04_key);
        
        print("Sleep")
        time.sleep(120)
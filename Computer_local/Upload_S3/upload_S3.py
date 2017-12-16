import os
import shutil
import datetime
import time
import requests

import os
path = os.path.dirname(os.path.realpath(__file__))

DIR_CAM01 = path + '/../Data/Crowd_Analysis/Cam01/cam01_{}.jpg'
DIR_CAM02 = path + '/../Data/Crowd_Analysis/Cam02/cam02_{}.jpg'
DIR_CAM03 = path + '/../Data/Crowd_Analysis/Cam03/cam03_{}.jpg'
DIR_CAM04 = path + '/../Data/Crowd_Analysis/Cam04/cam04_{}.jpg'
MIN_INDEX = 1
MAX_INDEX = 1

def s3_signed_upload_a_image(file_name_local, key_name, base_url, path_action):
    # Get signed URL for file upload
    url = base_url + path_action
    json_body = {"key_name": key_name}
    r = requests.post(url, json=json_body)
    print(r.text)

    print(r.status_code)
    if r.status_code == 200:
        result = r.json()
        print(result["url"])

        # Upload file
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(cur_dir, file_name_local)
        files = {'file': open(file_path, 'rb')}
        r2 = requests.post(result["url"], data=result["fields"], files=files)
        print(r2.status_code)
        if r2.status_code == 204:
            print("Upload is successful")
        else:
            print("Upload failed")
            print(r2.text)

def s3_signed_upload(base_url, key_prefix, path_action, camera_id):

    #get timestamp
    timestamp = "%.0f" % round(time.time()*1000)
    cam01_key = 'Cam01/' + timestamp + '_{}.jpg'.format(camera_id)
    cam02_key = 'Cam02/' + timestamp + '_{}.jpg'.format(camera_id)
    cam03_key = 'Cam03/' + timestamp + '_{}.jpg'.format(camera_id)
    cam04_key = 'Cam04/' + timestamp + '_{}.jpg'.format(camera_id)
    
    s3_signed_upload_a_image(DIR_CAM01.format(camera_id), key_prefix + cam01_key, base_url, path_action)
    s3_signed_upload_a_image(DIR_CAM02.format(camera_id), key_prefix + cam02_key, base_url, path_action)
    s3_signed_upload_a_image(DIR_CAM03.format(camera_id), key_prefix + cam03_key, base_url, path_action)
    s3_signed_upload_a_image(DIR_CAM04.format(camera_id), key_prefix + cam04_key, base_url, path_action)
    
    return (cam01_key, cam02_key, cam03_key, cam04_key)

if __name__ == '__main__':
    BASE_URL = "https://jyf7s0ji3m.execute-api.ap-southeast-1.amazonaws.com/dev/"
    KEY_PREFIX = "360-degree-camera/"
    PATH_ACTION_UPLOAD = "s3_signed_url/upload"
    CAMERA_ID = 2
    s3_signed_upload(BASE_URL, KEY_PREFIX, PATH_ACTION_UPLOAD, CAMERA_ID)

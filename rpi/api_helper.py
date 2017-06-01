import base64
import os
import requests
import sys

BUCKET = 'iot-360-camera'
KEY = 'camera01.png'
URL = 'https://zhileq7qw2.execute-api.ap-southeast-1.amazonaws.com/dev/base64_object/{}/{}'.format(BUCKET, KEY)


class ApiHelper:
    def uploadImageBase64(self, file_path, url=URL):
        if not os.path.isfile(file_path):
            raise Exception("File not found: {}".format(file_path))
        try:
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                r = requests.put(url, data=encoded_string)
                print(
                    "status code ={},  header = {}, body = {}".format(r.status_code, r.headers['content-type'], r.text))
                return [r.status_code, r.headers, r.text]
        except Exception as e:
            print e
            raise e

    def downloadImageBase64(self, file_path, url=URL):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                json = r.json()
                data = base64.b64decode(json['body'])
                with open(file_path, 'wb') as f:
                    f.write(data)
                return True
            else:
                return False
        except Exception as e:
            print e
            raise e


if __name__ == '__main__':
    file_name = 'download.jpg'
    _path_cur_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(_path_cur_dir, file_name)
    api = ApiHelper()
    try:
        # api.uploadImageBase64(file_path)
        print api.downloadImageBase64(file_path)
    except Exception as e:
        print e.message

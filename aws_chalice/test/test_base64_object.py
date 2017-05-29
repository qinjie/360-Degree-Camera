import base64
import os
import shutil

import requests

URL = r'https://zhileq7qw2.execute-api.ap-southeast-1.amazonaws.com/dev/base64_object/{}/{}'
BUCKET = '360-degree-camera'


def photo_upload(bucket):
    filename = 'google.png'
    filepath = os.path.join(os.getcwd(), filename)
    url = URL.format(bucket, filename)
    print filepath
    print url
    with open(filepath, "rb") as f:
        b64data = base64.b64encode(f.read())
        response = requests.put(url, b64data)
        print response.status_code
        print response.content


def photo_download(bucket, from_filename, to_filename):
    url = URL.format(bucket, from_filename)
    filepath = os.path.join(os.getcwd(), to_filename)
    print url
    print filepath
    response = requests.get(url, stream=True)
    print response.status_code
    print response.content
    if response.status_code == 200:
        dec = base64.b64decode(response.content)
        with open(filepath, 'wb') as f:
            f.write(dec)


if __name__ == "__main__":
    photo_upload(BUCKET)
    photo_download(BUCKET, 'google.png', 'download.png')

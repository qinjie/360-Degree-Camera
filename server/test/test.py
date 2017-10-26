import os
import shutil

import requests

BASE_URL = "https://jyf7s0ji3m.execute-api.ap-southeast-1.amazonaws.com/dev/"
KEY_PREFIX = "360-degree-camera/"


def test_s3_signed_upload():
    # Get signed URL for file upload
    url = BASE_URL + "s3_signed_url/upload"
    file_name = '001/b.jpg'
    key_name = KEY_PREFIX + file_name
    json_body = {"key_name": key_name}
    r = requests.post(url, json=json_body)
    print(r.text)

    print(r.status_code)
    if r.status_code == 200:
        result = r.json()
        print(result["url"])

        # Upload file
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(cur_dir, file_name)
        files = {'file': open(file_path, 'rb')}
        r2 = requests.post(result["url"], data=result["fields"], files=files)
        print(r2.status_code)
        if r2.status_code == 204:
            print("Upload is successful")
        else:
            print("Upload failed")
            print(r2.text)


def test_s3_signed_download():
    # GET signed URL for file download
    url = BASE_URL + "s3_signed_url/download"
    file_name = "001/local_b.jpg"
    key_name = KEY_PREFIX + "001/b.jpg"
    json_body = {"key_name": key_name}
    r = requests.post(url, json=json_body)
    print(r.status_code)
    if r.status_code == 200:
        url = r.json()['url']
        print(url)

        # Download file
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(cur_dir, file_name)
        chunk_size = 2000
        r2 = requests.get(url, stream=True)
        print(r2.status_code)
        if r2.status_code == 200:
            print("Download is successful.")
            with open(file_path, 'wb') as f:
                for chunk in r2.iter_content(chunk_size):
                    f.write(chunk)
            return file_path
        else:
            print("Download failed.")
            print(r2.text)
            if os.path.exists(file_path):
                os.remove(file_path)
            return None


if __name__ == '__main__':
    test_s3_signed_upload()
    test_s3_signed_download()

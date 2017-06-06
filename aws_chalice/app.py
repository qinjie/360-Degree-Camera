import base64
import json
import os
import shutil
import uuid

import boto3
import time

from chalice import Chalice, NotFoundError, Response, BadRequestError
from chalice import Response
from datetime import datetime

app = Chalice(app_name='iot-360-camera')

# Enable debugging for dev
app.debug = True

BUCKET = 'iot-360-camera'
REGION = 'ap-southeast-1'
s3_client = boto3.client('s3', region_name=REGION)
s3_res = boto3.resource('s3', region_name=REGION)


# ToDo
# http://chalice.readthedocs.io/en/latest/quickstart.html#tutorial-customizing-the-http-response
@app.route('/binary_object/{bucket}/{key}', methods=['GET', 'PUT'])
def binary_object(bucket, key):
    request = app.current_request
    if request.method == 'GET':
        try:
            file_path = '/tmp/{}_{}'.format(uuid.uuid4(), key)
            s3_client.download_file(bucket, key, file_path)
            file_size = os.path.getsize(file_path)
            headers = {
                # 'Content-Disposition': 'attachment; filename=\"' + key + '\"',
                #        'Content-Type': 'application/octet-stream',
                'Content-Type': 'image'
                # 'Content-Length': str(file_size)
            }

            fsk = open(file_path, 'rb')
            return Response(body='abc', headers=headers, status_code=200)
        except Exception as e:
            print e
            raise e
    elif request.method == 'PUT':
        response = s3_client.put_object(Bucket=bucket, Key=key,
                                        Body=request.raw_body)
        return response
        # return request.to_dict()


@app.route('/list_buckets', methods=['GET'])
def list_buckets():
    list = []
    try:
        for bucket in s3_res.buckets.all():
            list.append(bucket.name)
        return list
    except Exception as e:
        print e
        raise e


@app.route('/list_objects/{bucket}', methods=['GET'])
def list_objects(bucket):
    list = []
    try:
        bucket = s3_res.Bucket(bucket)
        if not bucket:
            raise NotFoundError("Bucket not found: " + bucket)
        for obj in bucket.objects.all():
            list.append(obj.key)
        return json.dumps(list)
    except Exception as e:
        print e
        raise e


@app.route('/base64_object/{bucket}/{key}', methods=['GET', 'PUT', 'DELETE'],
           content_types=['image', 'application/octet-stream', 'text/plain', 'application/json'])
def base64_object(bucket, key):
    request = app.current_request
    if request.method == 'GET':
        try:
            bucket = s3_res.Bucket(bucket)
            obj = bucket.Object(key)
            try:
                timestamp = time.mktime(obj.last_modified.timetuple())
            except Exception as e:
                print e
                raise NotFoundError("No file found with key = {}".format(key))

            if request.query_params and request.query_params.get('timestamp'):
                earliest = request.query_params.get('timestamp')
                if timestamp <= int(earliest):
                    raise NotFoundError("No new file version available")

            body = {'timestamp': timestamp, 'body': base64.b64encode(obj.get()['Body'].read()), 'encode': 'base64'}
            response = json.dumps(body)
            return response
        except Exception as e:
            print e
            raise e
    elif request.method == 'PUT':
        try:
            raw = base64.b64decode(request.raw_body)
            response = s3_client.put_object(Bucket=bucket, Key=key,
                                            Body=raw)
            return response
        except Exception as e:
            print e
            raise e
    elif request.method == 'DELETE':
        try:
            return s3_client.delete_object(Bucket=bucket, Key=key)
        except Exception as e:
            print e
            raise e

# @app.route('/cv2_version/{bucket}', methods=['GET'])
# def cv2_version():
#     cv_version = cv2.__version__
#     numpy_version = numpy.__version__
#     return {'cv2': cv_version, 'numpy': numpy_version}
#
#
# @app.route('/stitch_images/{bucket}', methods=['POST'])
# def stitch_images(bucket):
#     request = app.current_request
#     try:
#         json = request.json_body
#     except Exception as e:
#         raise BadRequestError("Invalid JSON data: {}".format(e.message))
#     if 'output_key' not in json:
#         raise BadRequestError('Missing output_key value.')
#     if 'input_keys' not in json:
#         raise BadRequestError('Missing input_keys value')
#     output_key = json['output_key']
#     output_path = '/tmp/{}'.format(output_key)
#     input_keys = json['input_keys']
#     if len(input_keys) < 2:
#         raise BadRequestError('More than 1 image is needed to perform stiching.')
#
#     '''Download images from S3'''
#     input_paths = {}
#     for k, input_key in input_keys.iteritems():
#         file_path = '/tmp/{}'.format(input_key)
#         print input_key, file_path
#         input_paths[k] = file_path
#         s3_client.download_file(bucket, input_key, file_path)
#
#     '''Timing'''
#     begin_time = datetime.datetime.now()
#
#     '''Load the to-be-stitched image_files beforehand'''
#     images = []
#     for key in sorted(input_paths):
#         print key, input_paths[key]
#         images.append(load_image(input_paths[key]))
#
#     '''stitch the first 2 image_files
#     because this is the first 2 image_files to be stitched, set firstTime=True
#     kps contains the position of the keypoints
#     features contains the descriptors of the corresponding keypoints
#     deg is the degree the right image had been bent'''
#     stitcher = Stitcher()
#     result, kps, features, deg = stitcher.stitch([images[0], images[1]], firstTime=True)
#
#     '''Continuously stitch the result with the other image_files,
#     each time, an image is stitched to the right of the previous-result image'''
#     for idx in range(2, len(images)):
#         stitcher = Stitcher()
#     result, kps, features, deg = stitcher.stitch([result, images[idx]],
#                                                  firstTime=False, l_ori_kps=kps,
#                                                  l_features=features, l_deg=deg)
#
#     print 'Elapsed time:', datetime.datetime.now() - begin_time
#
#     '''Show and save the result'''
#     cv2.imwrite(output_path, result)
#     s3_client.upload_file(output_path, bucket, output_key)
#
#     return output_path

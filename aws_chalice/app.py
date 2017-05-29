import base64
import json
import os
import shutil
import uuid

import boto3
from chalice import Chalice, NotFoundError, Response, BadRequestError
from chalice import Response

app = Chalice(app_name='iot-360-camera')

# Enable debugging for dev
app.debug = True

BUCKET = 'iot-360-camera'
REGION = 'ap-southeast-1'
s3_client = boto3.client('s3', region_name=REGION)
s3_res = boto3.resource('s3', region_name=REGION)


# ToDo
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
            body = base64.b64encode(obj.get()['Body'].read())
            response = Response(body=body, headers={'Content-Transfer-Encoding': 'base64', 'Content-Type': 'image'})
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


@app.route('/stitch_images/{bucket}', methods=['POST'])
def stitch_images(bucket):
    request = app.current_request
    json = request.json_body
    if 'output_key' not in json:
        raise BadRequestError('Missing output_key value.')
    if 'input_keys' not in json:
        raise BadRequestError('Missing input_keys value')
    output_key = json['output_key']
    input_keys = json['input_keys']

    input_paths = {}
    for k, input_key in input_keys.iteritems():
        file_path = '/tmp/{}'.format(input_key)
        input_paths[input_key] = file_path
        s3_client.download_file(bucket, input_key, file_path)

    for input_key, input_path in input_paths.iteritems():
        s3_client.upload_file(input_path, bucket, '{}_{}'.format(output_key, input_key))

    return 'ok'

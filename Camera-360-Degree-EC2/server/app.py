from chalice import Chalice, BadRequestError, ChaliceViewError
import os
import json
import boto3

from chalicelib.config import SQS_QUEUE, S3_BUCKET

app = Chalice(app_name='server')
app.debug = True


@app.route('/')
def index():
    return {'hello': '360-degree-camera'}


# Get a signed url from s3 for uploading file
# Test:
# >> echo '{"key_name":"360-degree-camera/001/a.jpg"}' | http -v POST https://jyf7s0ji3m.execute-api.ap-southeast-1.amazonaws.com/dev/s3_signed_url/upload
#
@app.route('/s3_signed_url/upload', methods=['POST'])
def s3_signed_post():
    # Only allow user to upload jpg image file
    FILE_TYPE = 'image/jpg'
    MIN_SIZE = 1024
    MAX_SIZE = 10240000
    EXPIRE_SEC = 60 * 60 * 24
    KEY_START = '360-degree-camera/'

    # Check incoming data
    try:
        incoming_data = app.current_request.json_body
        key_name = incoming_data["key_name"]
    except Exception as e:
        raise BadRequestError('Input required: {"key_name":"360-degree-camera/xxxx"}. Error:' + repr(e))

    # Generate signed post
    s3 = boto3.client('s3')
    presigned_post = s3.generate_presigned_post(
        Key=key_name,
        Bucket=os.environ.get("S3_BUCKET"),
        Fields={"acl": "public-read", "Content-Type": FILE_TYPE},
        Conditions=[
            {"acl": "public-read"},
            {"Content-Type": FILE_TYPE},
            ['starts-with', '$key', KEY_START],
            ['content-length-range', MIN_SIZE, MAX_SIZE]
        ],
        ExpiresIn=EXPIRE_SEC
    )

    return json.dumps(presigned_post)


# Get a signed url from s3 for download file
# Test:
# >> echo '{"key_name":"360-degree-camera/001/a.jpg"}' | http -v POST https://jyf7s0ji3m.execute-api.ap-southeast-1.amazonaws.com/dev/s3_signed_url/download
#
@app.route('/s3_signed_url/download', methods=['POST'])
def s3_signed_url():
    EXPIRE_SEC = 60 * 60 * 24

    # Check incoming data
    try:
        incoming_data = app.current_request.json_body
        key_name = incoming_data["key_name"]
    except Exception as e:
        raise BadRequestError('Input required: {"key_name":"xxx"}. Error:' + repr(e))

    # Generate signed url
    s3 = boto3.client('s3')
    presigned_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': os.environ.get("S3_BUCKET"),
            'Key': key_name
        },
        ExpiresIn=EXPIRE_SEC
    )

    return json.dumps({"url": presigned_url})


# Send a job (in json) to SQS
# Test:
# >> echo '{"action": "stitch_images", "node_id":"1", "input": {"picture_0":"360_degree_camera/001/a.jpg", "picture_1":"360_degree_camera/001/b.jpg", "picture_2":"360_degree_camera/001/c.jpg", "picture_3":"360_degree_camera/001/d.jpg"}, "output": "360_degree_camera/001.jpg"}' | http -v POST https://jyf7s0ji3m.execute-api.ap-southeast-1.amazonaws.com/dev/sqs_add_job
#
@app.route('/sqs_add_job', methods=['POST'])
def sqs_add_job():
    json_data = app.current_request.json_body
    keys = ['action', 'input', 'output']
    for key in keys:
        if key not in json_data:
            raise BadRequestError('Data json must contains all keys: ' + ','.join(keys))

    keys_input = ['picture_0', 'picture_1', 'picture_2', 'picture_3']
    for key in keys_input:
        if key not in json_data['input']:
            raise BadRequestError('Input json must contains all keys: ' + ','.join(keys_input))

    # Add bucket
    json_data['s3_bucket'] = S3_BUCKET
    print(json.dumps(json_data))

    sqs = boto3.resource('sqs')
    queue_name = SQS_QUEUE
    try:
        queue = sqs.get_queue_by_name(QueueName=queue_name)
    except:
        # Create new queue if it does not exist
        queue = sqs.create_queue(QueueName=queue_name)

    str = json.dumps(json_data)
    response = queue.send_message(MessageBody=str)
    return response

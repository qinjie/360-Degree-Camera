import boto3
import json
import sys
import os
import logging
import datetime
import time
import shutil #For copy of testing only

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path + '/..')

from StitchingMaker.stitching import stitching 
from MotionDetection.MID_analysis import analysis_two_pano
from MotionDetection.create import create_new_photo,create_new_analysis

QUEUE_URL = 'https://sqs.ap-southeast-1.amazonaws.com/498107424281/DatntQueue'
DIR_DATA = path + '/../Data/'
BUCKET_NAME = 'iot-centre-projects'
KEY_PREFIX = "360-degree-camera/"
STITCH = "stitch"
MA = "montion-analysis"

#download a file from s3
def download_file(bucket_name, key, store_path):
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(bucket_name).download_file(key, store_path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(key + " : the object does not exist.")
        else:
            raise

def upload_file(bucket_name, store_path, key):
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(bucket_name).upload_file(store_path, key)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(key + " : the object does not exist.")
        else:
            raise

#polling for a new message
def sqs_polling(queue_url):
    # Create SQS client
    sqs = boto3.client('sqs')

    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=20
    )

    if ('Messages' not in response):
        print('Nothing in SQS')
        sys.exit()

    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    result = ("","")
    try:
        index = 1
        body = json.loads(message['Body'])
        print('Message json found) Received message: %s' % body)
        try:
            print(body['input']['cam01_key'])
	    print(body['action'])
	    print(body['output'])
	    print(body['key_prefix'])
	    key_prefix = body['key_prefix']
	    camera_id = body['camera_id']
            download_file(BUCKET_NAME, key_prefix + body['input']['cam01_key'], DIR_DATA + 'Cam01/' + 'cam01_{}.jpg'.format(camera_id))
            download_file(BUCKET_NAME, key_prefix + body['input']['cam02_key'], DIR_DATA + 'Cam02/' + 'cam02_{}.jpg'.format(camera_id))
            download_file(BUCKET_NAME, key_prefix + body['input']['cam03_key'], DIR_DATA + 'Cam03/' + 'cam03_{}.jpg'.format(camera_id))
            download_file(BUCKET_NAME, key_prefix + body['input']['cam04_key'], DIR_DATA + 'Cam04/' + 'cam04_{}.jpg'.format(camera_id))
	    print("Download finished")
	    result = (body['action'], body['camera_id'], body['camera_name'])
        except:
            print("Download errored")
    except:
        #print("Exception occur")
        print('No message json found instead text: %s' % message['Body'])
   
    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('Delete message')
    return result

if __name__ == '__main__':
    action, camera_id, camera_name = sqs_polling(QUEUE_URL)
    # save a copy pano for MA
    shutil.copyfile(DIR_DATA + '/Pano/pano_{}.jpg'.format(camera_id), DIR_DATA + '/Pano/pano_previous_{}.jpg'.format(camera_id));

    #get timestamp
    timestamp = "%.0f" % round(time.time()*1000)

    if (STITCH in action):
	try:
	    print('Start stitching')
    	    stitching(camera_id)
	    #get timestamp
	    print('Transfer data back to S3')
            #timestamp = "%.0f" % round(time.time()*1000)
	    upload_file(BUCKET_NAME, DIR_DATA + 'Pano/pano_{}.jpg'.format(camera_id), KEY_PREFIX + 'Pano/' + camera_name + '/' + '{}.jpg'.format(timestamp))
	    upload_file(BUCKET_NAME, DIR_DATA + 'Pano/pano_{}.jpg'.format(camera_id), KEY_PREFIX + 'Pano/' + 'pano{}.jpg'.format(camera_name))
	    print("Finish")
	except Exception, error:
	    print('Error occur : ' + str(error))
    if (MA in action):
	try:
	    p1 = DIR_DATA + 'Pano/pano_{}.jpg'.format(camera_id)
	    p2 = DIR_DATA + 'Pano/pano_previous_{}.jpg'.format(camera_id)
	    print("Do analysis : " + p1 + " & " + p2)
	    result = analysis_two_pano(p1, p2)
	    print("Finish analysis, result :" + str(result))
            print("Store photo to database")
	    photo = create_new_photo(camera_id, KEY_PREFIX + 'Pano/' + camera_name + '/' + '{}.jpg'.format(timestamp))
            print("Finish store photo to database")
	    print("Store analysis to database")
	    create_new_analysis(photo.id, result, "montion")
	    print("Finish store analysis to database")
	    print("FINISH ALL JOB")
	except Exception, error:
	    print('Error occur : ' + str(error))

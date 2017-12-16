import json
import datetime
import pymysql
import boto3
import requests

from chalice import Chalice

db_host = "iot-centre-rds.crqhd2o1amcg.ap-southeast-1.rds.amazonaws.com"
db_name = "360-degree-camera"
db_username = "root"
db_password = "Soe7014Ece"

app = Chalice(app_name='360-Degree-Image')


@app.route('/sqs', content_types=['application/json'], methods=['POST'])
def sqs_service():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='DatntQueue')
    message = app.current_request.raw_body
    response = queue.send_message(MessageBody=message)
    
    return {"status": message}
    

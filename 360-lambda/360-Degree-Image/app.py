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


@app.route('/{camera_id}')
def index(camera_id):
    conn = connect_database()
    with conn.cursor() as cur:
        cur.execute("SELECT result FROM analysis a, photo b, node n WHERE n.id = '{}' and n.id = b.node_id and b.id = a.photo_id ORDER BY a.id DESC LIMIT 1".format(camera_id))
    result = -1
    for row in cur:
        result = row[0]
    return {'percent': result}

@app.route('/sqs', content_types=['application/json'], methods=['POST'])
def sqs_service():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='DatntQueue')
    message = app.current_request.raw_body
    response = queue.send_message(MessageBody=message)
    
    # Create SQS client
    #sqs = boto3.client('sqs')
    '''print "Sending...."
    queue_url = 'https://sqs.ap-southeast-1.amazonaws.com/498107424281/DatntQueue'
    sqs_sender(queue_url, "ABC")
    print "Sent message"'''
    # Send message to SQS queue
    '''try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody='HUHU'
        )
    except Exception as e:
        print e
    '''
    return {"status": message}
    
def sqs_sender(url, message):
    #url = 'https://sqs.ap-southeast-1.amazonaws.com/498107424281/DatntQueue'
    #message = '{ "name": "MrDat", "image1_url": "http1"}'
    payload = {'Action': 'SendMessage', 'MessageBody': message, 'Version': '2012-11-05', 'Expires': '2011-10-15T12%3A00%3A00Z', 'AUTHPARAMS': ''}
    r = requests.post(url, data=payload)
    
def connect_database():
    try:
        conn = pymysql.connect(db_host, user=db_username, passwd=db_password, db=db_name, connect_timeout=5)
    except Exception as e:
        print (e)
        conn = pymysql.connect()
    print("SUCCESS: Connection to RDS mysql instance succeeded")
    return conn
    
# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

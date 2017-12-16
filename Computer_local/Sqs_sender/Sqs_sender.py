import requests

def sqs_sender(url, message):
    #url = 'https://sqs.ap-southeast-1.amazonaws.com/498107424281/DatntQueue'
    #message = '{ "name": "MrDat", "image1_url": "http1"}'
    payload = {'Action': 'SendMessage', 'MessageBody': message, 'Version': '2012-11-05', 'Expires': '2011-10-15T12%3A00%3A00Z', 'AUTHPARAMS': ''}
    r = requests.post(url, data=payload)

def api_sqs_sender(url, message):
    r = requests.post(url, data=message)
    print r.status_code
    if (r.status_code != 200):
        print "Webservice was broken, Back up solution : directly to SQS (not good solution)"
        sqs_sender(url, message)
	
if __name__ == '__main__':
	python_sqs_sender()
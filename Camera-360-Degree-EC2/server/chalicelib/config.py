import os

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "360-degree-camera")
DB_USERNAME = os.environ.get("DB_USERNAME", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "abcd1234")
S3_BUCKET = os.environ.get("S3_BUCKET")
SQS_QUEUE = os.environ.get('SQS_QUEUE')

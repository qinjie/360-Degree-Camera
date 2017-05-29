import gzip
import zipfile


def zip2gzip(s3_client, bucket, key):
    # # Get the object from the event and show its content type
    # bucket = event['Records'][0]['s3']['bucket']['name']
    # key = event['Records'][0]['s3']['object']['key']

    try:
        s3_client.download_file(bucket, key, '/tmp/file.zip')
        zfile = zipfile.ZipFile('/tmp/file.zip')
        namelist = zfile.namelist()

        if len(namelist) > 1:
            pass

        for filename in namelist:
            data = zfile.read(filename)
            f = open('/tmp/' + str(filename), 'wb')
            f.write(data)
            f.close()

        zipToGzip = gzip.open('/tmp/data.gz', 'wb')
        zipToGzip.write(data)
        zipToGzip.close()
        s3_client.upload_file('/tmp/data.gz', bucket, key + '.gz')
        s3_client.delete_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(e)
        print(
            'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
                key, bucket))
        raise e

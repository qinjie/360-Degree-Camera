import os
import sys
import datetime
from classes import Node, Photo, Analysis

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path + '/../package')


def create_new_photo(node_id, s3_path):
    #id auto increase
    photo = Photo.create(
        node = node_id,
        s3_path = s3_path,
        created_at = datetime.datetime.now(),
        updated_at = datetime.datetime.now()
    )
    print(str(photo.id))
    return photo

def create_new_analysis(photo_id, result, type):
    Analysis.create(
        photo = photo_id,
        result = result,
        type = type,
        created_at = datetime.datetime.now(),
        updated_at = datetime.datetime.now()
    )

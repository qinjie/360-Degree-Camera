import os
import sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path + '/../package')
# import peewee as pw
from peewee import *
from classes import Node, Photo, Analysis
import datetime
from create import create_new_photo, create_new_analysis
from MID_analysis import analysis_two_pano

def node_create():
    cam1 = Node.create(
        id = 1,
        name = "Cam001",
        status = 1,
        create_at = datetime.datetime.now(),
        update_at = datetime.datetime.now()
    )

if __name__ == '__main__':
    analysis_two_pano('../Data/Pano/pano_1.jpg', '../Data/Pano/pano_previous_1.jpg')
	
# myDB = MySQLDatabase("360-degree-camera", host="iot-centre-rds.crqhd2o1amcg.ap-southeast-1.rds.amazonaws.com", port=3306, user="root",
    #                         passwd="Soe7014e")
    #node = Node(myDB)
    '''new_node = {
        'id' : 2,
        'name' : 'Cam002',
        'status': 1,
        'created_at' :datetime.datetime.now(),
        'updated_at' :datetime.datetime.now()
    }'''

    #Node.create(**new_node)
    #create_new_photo(1,"abc")
    '''Photo.create(
        id = 1,
        node = 1,
        s3_path = '',
        created_at = datetime.datetime.now(),
        updated_at = datetime.datetime.now()
    );'''

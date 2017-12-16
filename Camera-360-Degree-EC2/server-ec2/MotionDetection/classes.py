import os
import sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path + '/../package')

from peewee import *

db = MySQLDatabase("360-degree-camera", host="iot-centre-rds.crqhd2o1amcg.ap-southeast-1.rds.amazonaws.com", port=3306, user="root",
                            passwd="Soe7014Ece")
# class BaseModel(Model):
#     def __init__(self, db, table_name = ""):
#         self.db = db
#         self.table_name = table_name
#
#     class Meta:
#         def __init__(self):
#             database = self.outer.db
#             if (self.outer.table_name != ""):
#                 db_table = self.outer.table_name


class BaseModel(Model):
    class Meta:
        database = db

class Node(BaseModel):
    id = IntegerField()
    name = CharField()
    status = IntegerField()
    create_at = DateTimeField()
    update_at = DateTimeField()

    class Meta:
        db_table = 'node'

class Photo(BaseModel):
    id = IntegerField()
    node = ForeignKeyField(db_column='node_id', rel_model=Node, to_field='id')
    s3_path = TextField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

class Analysis(BaseModel):
    id = IntegerField()
    photo = ForeignKeyField(db_column='photo_id', rel_model=Photo, to_field='id')
    result = FloatField()
    type = CharField()
    create_at = DateTimeField()
    update_at = DateTimeField()

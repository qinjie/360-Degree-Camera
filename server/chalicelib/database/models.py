from peewee import *

from chalicelib import config

database = MySQLDatabase(config.DB_NAME, host=config.DB_HOST, port=3306,
                         user=config.DB_USERNAME,
                         passwd=config.DB_PASSWORD)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Node(BaseModel):
    name = CharField(unique=True)
    status = SmallIntegerField(default=0)
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)

    detail_fields = [name, status]
    ignored_added_fields = ['id', 'created_at', 'updated_at']
    ignored_updated_fields = ['id', 'created_at', 'updated_at']

    class Meta:
        db_table = 'node'


class Photo(BaseModel):
    node = ForeignKeyField(db_column='node_id', null=False, rel_model=Node, to_field='id', related_name='owner_node')
    s3_path = CharField()
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)

    detail_fields = [s3_path, node]
    ignored_added_fields = ['id', 'created_at', 'updated_at']
    ignored_updated_fields = ['id', 'created_at', 'updated_at']

    class Meta:
        db_table = 'photo'


class Analysis(BaseModel):
    photo = ForeignKeyField(db_column='photo_id', rel_model=Photo, to_field='id', index=True)
    type = CharField()
    result = FloatField()
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)

    detail_fields = [photo, type, result]
    ignored_added_fields = ['id', 'created_at', 'updated_at']
    ignored_updated_fields = ['id', 'created_at', 'updated_at']

    class Meta:
        db_table = 'analysis'

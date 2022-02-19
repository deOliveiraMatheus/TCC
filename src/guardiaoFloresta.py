from datetime import datetime
from peewee import *

db = SqliteDatabase('guardian.db')

class GuardiaoTemp(Model):
    sensor_temp = CharField()
    value_temp = IntegerField()
    join_date_temp = DateTimeField()

    class Meta:
        database = db

class GuardiaoGas(Model):
    sensor_gas = CharField()
    value_gas = IntegerField()
    join_date_gas = DateTimeField()

    class Meta:
        database = db

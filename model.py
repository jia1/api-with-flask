from mongoengine import *

class Store(Document):
    name = StringField()
    pairs = DictField()

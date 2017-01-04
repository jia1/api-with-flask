from mongoengine import *

class Store(Document):
    name = StringField(required = True, unique = True)
    pairs = DictField()

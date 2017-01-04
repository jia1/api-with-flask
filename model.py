from mongoengine import *

class Pair(Document):
    name = StringField(required = True, unique = True)
    key = StringField(required = True)
    versions = ListField(DictField(required = True))

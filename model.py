from mongoengine import *

class Pair(Document):
    key = StringField(required = True)
    value = StringField(required = True)

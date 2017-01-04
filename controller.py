from flask import Flask, abort, jsonify, request
from mongoengine import connect
from flask_mongoengine import MongoEngine
from secret import DB_NAME, DB_URI
from model import Pair

app = Flask(__name__)
app.config['MONGODB_DB'] = DB_NAME

connect(DB_NAME, host = DB_URI)
db = MongoEngine(app)

@app.route('/', methods = ['GET'])
def root():
    return 'HOME'

@app.route('/<queryName>', methods = ['GET'])
def index(queryName):
    querySet = Pair.objects(name = queryName).only('key', 'versions')
    if querySet != None:
        document = querySet.first()
        dictionary = {getKey(document): getValue(document)}
        return jsonify(dictionary)
    else:
        abort(404)

@app.route('/<queryName>/<queryKey>', methods = ['GET'])
def show(queryName, queryKey):
    querySet = Pair.objects(name = queryName, key = queryKey)
    document = querySet.first()
    if document != None:
        queryTime = request.args.get('timestamp', type = float)
        return getValue(document, queryTime)
    else:
        abort(404)

@app.route('/<queryName>', methods = ['POST'])
def create(queryName):
    querySet = Pair.objects(name = queryName)
    document = querySet.first()
    if document != None:
        # UPDATE
        return 'UPDATE'
    else:
        # INSERT
        return 'INSERT'

def getKey(document):
    return document.key

def getValue(document, queryTime = None):
    if queryTime == None:
        return getLatestVersion(getVersions(document)).values()[0]
    else:
        for version in getVersions(document):
            if queryTime >= float(version.keys()[0]):
                return version.values()[0]
        abort(404)

def getVersions(document):
    return document.versions

def getLatestVersion(versions):
    return versions[0]

if __name__ == '__main__':
    app.run()

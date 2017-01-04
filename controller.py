from flask import Flask, abort, jsonify, request
from mongoengine import connect
from flask_mongoengine import MongoEngine
from secret import DB_NAME, DB_URI
from model import Store

app = Flask(__name__)
app.config['MONGODB_DB'] = DB_NAME

connect(DB_NAME, host = DB_URI)
db = MongoEngine(app)

@app.route('/', methods = ['GET'])
def root():
    return 'HOME'

@app.route('/<queryName>', methods = ['GET'])
def index(queryName):
    gotStore, pairs = getPairs(queryName)
    if gotStore:
        dictionary = {}
        for key in pairs:
            dictionary[key] = getValue(pairs, key)
        return jsonify(dictionary)
    else:
        abort(404)

@app.route('/<queryName>/<queryKey>', methods = ['GET'])
def show(queryName, queryKey):
    gotStore, pairs = getPairs(queryName)
    if gotStore and queryKey in pairs:
        queryTime = request.args.get('timestamp', type = float)
        return getValue(pairs, queryKey, queryTime)
    else:
        abort(404)

@app.route('/<queryName>', methods = ['POST'])
def create(queryName):
    if request.headers['Content-Type'] == 'application/json':
        requestJson = request.json
        # VALIDATE
        # abort(400)
        gotStore, pairs = getPairs(queryName)
        if gotStore:
            if queryKey in pairs:
                return 'UPDATE STORE, UPDATE VAL'
            else:
                return 'UPDATE STORE, INSERT KEY'
        else:
            return 'INSERT STORE, INSERT KEY'
    else:
        abort(400)

def getPairs(queryName):
    store = Store.objects(name = queryName).first()
    gotStore = (store != None)
    if gotStore:
        pairs = store.pairs
    else:
        pairs = None
    return (gotStore, pairs)

# key is in pairs
def getValue(pairs, key, queryTime = None):
    versions = pairs[key]
    if queryTime == None:
        return getLatestVersion(versions).values()[0]
    else:
        for v in versions:
            if queryTime >= float(v.keys()[0]):
                return v.values()[0]
        abort(404)

def getLatestVersion(versions):
    return versions[0]

if __name__ == '__main__':
    app.run()

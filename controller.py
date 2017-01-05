from flask import Flask, abort, jsonify, request
from mongoengine import connect
from flask_mongoengine import MongoEngine
from time import time
from json import loads
from model import Store
from secret import DB_NAME, DB_URI

app = Flask(__name__)
app.config['MONGODB_DB'] = DB_NAME

connect(DB_NAME, host = DB_URI)
db = MongoEngine(app)

@app.route('/', methods = ['GET'])
def root():
    collection = {}
    for store in Store.objects().only('name', 'pairs'):
        collection[store.name] = store.pairs
    return jsonify(collection)

@app.route('/<queryName>', methods = ['GET'])
def index(queryName):
    gotStore, pairs = getPairs(queryName)
    if gotStore:
        displayStore = {}
        for key in pairs:
            displayStore[key] = getValue(pairs, key)
        return jsonify(displayStore)
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
        # INSERT VALIDATION
        gotStore, store = getStore(queryName)
        if not gotStore:
            Store.ensure_indexes()
            Store(name = queryName, pairs = {}).save()
        return upsertPairs(queryName, requestJson)
    else:
        abort(400)

def getStore(queryName):
    store = Store.objects(name = queryName).first()
    return (store != None, store)

def getPairs(queryName):
    gotStore, store = getStore(queryName)
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

# Store where name = storeName exists
def upsertPairs(storeName, newPairs):
    updatePairs = Store.objects(name = storeName).first().pairs
    for key in newPairs:
        if key not in updatePairs:
            updatePairs[key] = []
        timestamp = str(int(time()))
        updatePairs[key].insert(0, {timestamp: newPairs[key]})
    Store.objects(name = storeName).update(pairs = updatePairs)
    return timestamp

if __name__ == '__main__':
    app.run()

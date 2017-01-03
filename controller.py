from flask import Flask
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

@app.route('/<collection>', methods = ['GET'])
def index(collection):
    return Pair.objects.only('key', 'value').to_json()

@app.route('/<collection>/<key>', methods = ['GET'])
def show(collection, key):
    return 'SHOW'

@app.route('/<collection>', methods = ['POST'])
def create(collection):
    return 'CREATE'

if __name__ == '__main__':
    app.run()

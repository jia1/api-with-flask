from flask import Flask, jsonify, request, url_for
from collections import deque
from copy import deepcopy
from time import time
import math

app = Flask(__name__)

dictionary = {}
history = {}
name = 'dictionary'
timestamp = 'timestamp'
TIME, VAL = 0, 1

@app.route('/', methods = ['GET'])
def root():
    return url_for('index')

@app.route('/'+ name, methods = ['GET'])
def index():
    return jsonify(dictionary)

@app.route('/' + name + '/<key>', methods = ['GET'])
def show(key):
    if key not in history:
        return 'Not Found'
    else:
        t = request.args.get(timestamp)
        if t == None:
            return dictionary[key]
        else:
            for version in history[key]:
                if int(t) >= version[TIME]:
                    return version[VAL]
            return 'Not Found'

@app.route('/' + name, methods = ['POST'])
def create():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        for key in data:
            dictionary[key] = data[key]
            if key not in history:
                history[key] = deque()
            history[key].appendleft([int(math.floor(time())), data[key]])
        return jsonify(data)
    else:
        return 'None'

@app.route('/history', methods = ['GET'])
def log():
    serializable = deepcopy(history)
    for key in serializable:
        serializable[key] = list(serializable[key])
    return jsonify(serializable)

if __name__ == '__main__':
    app.run()

# api-with-flask
Key-value store via HTTP API (Flask and MongoDB)

### Description
Version-controlled key-value store via HTTP API. Every time you save a key-value pair on the database, the current timestamp will be attached to that value. This is so that you can query for keys at a certain timestamp (e.g. in the past) and get the various values written to it at that time.

### Tools required

1. Linux?
2. Flask ([Installation](http://flask.pocoo.org/docs/0.12/installation/))
3. Flask-MongoEngine ([Installation](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/))
  - Flask extension for integration with MongoEngine.
  - MongoEngine is a document-object mapper for working with MongoDB from Python.
4. mLab for remote MongoDB deployment ([Website](https://mlab.com/home))
  - This should be used for prototyping, not for any real product.
  
### Setting up and testing

1. `git clone https://github.com/jia1/api-with-flask.git`
2. `cd api-with-flask/`
3. `export FLASK_APP=controller.py`
  - See [quickstart](http://flask.pocoo.org/docs/0.12/quickstart/).
4. `flask run`
5. Go to the URL shown in the terminal standard output.
  - Usually `http://127.0.0.1:5000`
6. `chmod +x sampleRequests.sh`
  - Create a new terminal tab to do this (i.e. leave step 4 alone and let it stay running).
  - sampleRequests.sh contain curl commands for making HTTP POST requests to the local Flask app.
  - Only need to run this step once.
7. `./sampleRequests.sh`
8. Repeat step 5 and see the changes caused by the requests that you ran in step 7.

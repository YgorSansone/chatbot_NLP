from config import Config
from flask import Flask
import flask
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r'/*': {'origins': '*'}})

# mongodb_client = PyMongo(app, uri="mongodb+srv://admin:cNyZf724mDTEqU3@cluster0.fy7kj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mongodb_client = PyMongo(app, uri="mongodb+srv://martins:P9v2Mi0TjHtgSGeG@cluster0.busl5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = mongodb_client.db

from app import routes

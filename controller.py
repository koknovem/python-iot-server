from api import *
from flask import Flask
app = Flask(__name__)
@app.route("/")
def peoplecount():
    return getPeoplecount()
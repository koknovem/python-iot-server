from api import *
from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return showCameraStream()

@app.route("/peoplecount")
def peoplecount():
    return getPeoplecount()

@app.route("/heatmap")
def heatmap():
    return getHeatmap()


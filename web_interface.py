import os

from bottle import Bottle, route, static_file
from WookieDb import WookieDb
from TrendAnalyser import TrendAnalyser

app = Bottle()
PATH = os.path.dirname(os.path.abspath(__file__))
TA = TrendAnalyser()

@route("/filters.json")
def filters_json():
    return {"res" : TA._get_filter_keywords()}

@route("/<filename>")
def static_resource(filename):
    return static_file("/static/"+filename, root=PATH)

@route("/")
def index_page():
    return "Index page is working"

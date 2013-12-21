import os

from bottle import Bottle, route, static_file

app = Bottle()
PATH = os.path.dirname(os.path.abspath(__file__))

@route("/<filename>")
def static_resource(filename):
    return static_file("/static/"+filename, root=PATH)

@route("/")
def index_page():
    return "Index page is working"

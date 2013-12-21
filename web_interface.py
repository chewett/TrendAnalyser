from bottle import Bottle, route

app = Bottle()

@route("/")
def index_page():
    return "Index page is working"

import os

from bottle import Bottle, route, static_file
from WookieDb import WookieDb
from TrendAnalyser import TrendAnalyser

app = Bottle()
PATH = os.path.dirname(os.path.abspath(__file__))
TA = TrendAnalyser()
debug = True


@route("/hashtags.json/<term>")
def hashtags_search_json(term):
    return {"res" : TA._get_hashtag_details(term)}

@route("/hashtag_frequency.json/<term>")
def hashtag_frequency_json(term):
    return {"res" : TA._get_hashtag_frequency(term)}

@route("/filters.json")
def filters_json():
    return {"res" : TA._get_filter_keywords()}

@route("/trends.json")
def trends_json():
    return {"res" : TA._get_latest_trends()}

@route("/trend_search.json/<term>")
def trends_search_json(term):
    return {"res" : TA._get_trending_details(term)}

@route("/<filename>")
def compile_file(filename):
    if not os.path.isdir(os.path.join(PATH, "compiled")):
        os.mkdir(os.path.join(PATH, "compiled"))

    if debug == False and os.path.exists(os.path.join(PATH, "compiled", filename + ".html")):
        return static_file("/compiled" + filename, root=PATH)
    else:
        compiled = open(os.path.join(PATH, "compiled", filename), "w")

        template = open(os.path.join(PATH, "static", "inc", "header.html"), "r")
        compiled.write(template.read())
        template.close()

        template = open(os.path.join(PATH, "static", filename), "r")
        compiled.write(template.read())
        template.close()

        template = open(os.path.join(PATH, "static", "inc", "footer.html"), "r")
        compiled.write(template.read())
        template.close()

        compiled.close()

    return static_file("/compiled/" + filename, root=PATH)

@route("/")
def index_page():
    return "Index page is working"

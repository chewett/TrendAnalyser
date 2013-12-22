import os

from bottle import Bottle, route, static_file
from WookieDb import WookieDb
from TrendAnalyser import TrendAnalyser

app = Bottle()
PATH = os.path.dirname(os.path.abspath(__file__))
TA = TrendAnalyser()

@route("/hashtags.json/<term>")
def hashtags_search_json(term):
    return {"res" : TA._get_hashtag_details(term)}

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
def static_resource(filename):
    return static_file("/static/"+filename, root=PATH)

@route("/")
def index_page():
    return "Index page is working"

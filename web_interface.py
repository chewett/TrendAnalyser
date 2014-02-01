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

@route("/woeid_data.json")
def woeid_data_json():
    return {"res" : TA._get_woeid_data()}

@route("/words_positive.json")
def words_positive_json():
    return {"res" : TA._get_words_positive()}

@route("/words_negative.json")
def words_negative_json():
    return {"res" : TA._get_words_negative()}

@route("/css/<filename>")
def css(filename):
    return static_file("/static/css/" + filename, root=PATH)

@route("/images/<filename>")
def images(filename):
    return static_file("/static/images/" + filename, root=PATH)

@route("/")
@route("/<filename>")
def compile_file(filename="index.html"):
    if not os.path.isdir(os.path.join(PATH, "compiled")):
        os.mkdir(os.path.join(PATH, "compiled"))

    if not os.path.isfile(os.path.join(PATH, "static", filename)):
        return static_file("/static/"+ filename, root=PATH)

    #TODO: Fix this so it properly stores a log of what needs to be regenerated
    if false and TA.conf['debug'] == False and os.path.exists(os.path.join(PATH, "compiled", filename + ".html")):
        return static_file("/compiled" + filename, root=PATH)
    else:
        compiled = open(os.path.join(PATH, "compiled", filename), "w")

        template = open(os.path.join(PATH, "static", "inc", "header.html"), "r")
        compiled.write(template.read())
        template.close()

        if TA.conf['debug'] == True:
            template = open(os.path.join(PATH, "static", "inc", "debug.html"), "r")
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


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

@route("/mentions.json/<term>")
def mentions_search_json(term):
    return {"res" : TA._get_mention_details(term)}

@route("/mention_frequency.json/<term>")
def mention_frequency_json(term):
    return {"res" : TA._get_mention_frequency(term)}

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

@route("/trending_woeids_downloading.json")
def trending_woeids_downloading():
    return {"res" : TA._get_trending_woeids_downloading()}

@route("/css/<filename>")
def css(filename):
    return static_file("/static/css/" + filename, root=PATH)

@route("/js/<filename>")
def css(filename):
    return static_file("/static/js/" + filename, root=PATH)

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
    if False and TA.conf['debug'] == False and os.path.exists(os.path.join(PATH, "compiled", filename + ".html")):
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


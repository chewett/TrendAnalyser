'''
This is the bottle powered web interface for the TrendAnalyser project
'''

import os

from bottle import Bottle, route, static_file
from WookieDb import WookieDb
from TrendAnalyser import TrendAnalyser

app = Bottle()
PATH = os.path.dirname(os.path.abspath(__file__))
TA = TrendAnalyser()

@route("/hashtags.json?term=<term>")
def hashtags_search_json(term):
    '''Used to get the data for hashtag searches'''
    return {"res" : TA._get_hashtag_details(term)}

@route("/hashtag_frequency.json?term=<term>")
def hashtag_frequency_json(term):
    '''Used to get the data for hashtag frequency searches for the graphs'''
    return {"res" : TA._get_hashtag_frequency(term)}

@route("/mentions.json?term=<term>")
def mentions_search_json(term):
    '''Used to get the data for mention searches'''
    return {"res" : TA._get_mention_details(term)}

@route("/mention_frequency.json?term=<term>")
def mention_frequency_json(term):
    '''Used to get the data for mention frequency searchs for the graphs'''
    return {"res" : TA._get_mention_frequency(term)}

@route("/filters.json")
def filters_json():
    '''Used to display what filters we are currently downloading'''
    return {"res" : TA._get_filter_keywords()}

@route("/trends.json")
def trends_json():
    '''Used to display the latest trends in the database'''
    return {"res" : TA._get_latest_trends()}

@route("/trend_search.json?term=<term>")
def trends_search_json(term):
    '''Used to search through the trending items'''
    return {"res" : TA._get_trending_details(term)}

@route("/woeid_data.json")
def woeid_data_json():
    '''Used to display all the woeid data'''
    return {"res" : TA._get_woeid_data()}

@route("/words_positive.json")
def words_positive_json():
    '''Used to display all the positive words'''
    return {"res" : TA._get_words_positive()}

@route("/words_negative.json")
def words_negative_json():
    '''Used to display all the negative words'''
    return {"res" : TA._get_words_negative()}

@route("/trending_woeids_downloading.json")
def trending_woeids_downloading():
    '''Ued to display the woeid areas we are downloading'''
    return {"res" : TA._get_trending_woeids_downloading()}

@route("/css/<filename>")
def css(filename):
    '''Used to serve css files'''
    return static_file("/static/css/" + filename, root=PATH)

@route("/js/<filename>")
def css(filename):
    '''Used to serve javascript files'''
    return static_file("/static/js/" + filename, root=PATH)

@route("/images/<filename>")
def images(filename):
    '''Used to serve image files'''
    return static_file("/static/images/" + filename, root=PATH)

@route("/")
@route("/<filename>")
def compile_file(filename="index.html"):
    '''Used to try and serve any HTML files in the main directory'''
    if TA.conf['offline']:
        filename = "offline.html"
    
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


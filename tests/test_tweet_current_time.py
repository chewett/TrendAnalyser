import json
from TwitterAPI import TwitterAPI
from time import gmtime, strftime

def load_conf():
    conf = json.load(open("conf.json"))
    return conf

def get_api():
    conf = load_conf()

    det_file = open(conf['twitter_key_location'])
    det = json.load(det_file)

    api = TwitterAPI(det['consumer_key'],
                     det['consumer_secret'],
                     det['access_token_key'],
                     det['access_token_secret'])

    return api



api = get_api()

r = api.request("statuses/update", {'status' : "Posting from my Twitter python program using the #twitterapi #3rdyearproject Current time is: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) } )

print json.loads(r.text)

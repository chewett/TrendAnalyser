import json

from TwitterAPI import TwitterAPI

class TrendAnalyser:

    def __init__(self, config_location="conf.json"):
        self.load_conf(config_location)
        self.load_api()

    def load_conf(self, config_location):
        self.conf = json.load(open(config_location))

    def load_api(self):
        details = json.load(open(self.conf['twitter_key_location']))

        self.api = TwitterAPI(details['consumer_key'],
                              details['consumer_secret'],
                              details['access_token_key'],
                              details['access_token_secret'])


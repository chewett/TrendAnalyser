import json
import os
import time
import errno

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

    def save_data(self, response, location):
        filename = os.path.join(self.conf['save_data_location'], location + "_" + str(int(time.time())) + ".json")

        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        json.dump(response, open(filename, 'w'))

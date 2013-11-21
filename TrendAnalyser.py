import json
import os
import time
import errno
import md5

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

    def save_trend_data(self, json_data, woeid):
        filelocation = os.path.join(self.conf['save_data_location'],
                                "trends/place/weoid_" + str(woeid) + "_" +
                                str(int(time.time())) + ".json")
        self.save_data(json_data, filelocation)

    def save_twitter_sample_data(self, json_data):
        time_folder = int(time.time() / 300) * 300

        filelocation = os.path.join(self.conf['save_data_location'],
                                "statuses/sample", str(time_folder),
                                str(int(time.time())) + "_" +
                                md5.md5(json.dumps(json_data)).hexdigest() +
                                ".json")
        self.save_data(json_data, filelocation)



    def save_data(self, json_data, location):

        try:
            os.makedirs(os.path.dirname(location))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        json.dump(json_data, open(location, 'w'))

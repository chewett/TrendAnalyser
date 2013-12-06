import json
import os
import time
import errno
import md5
import uuid

from TwitterAPI import TwitterAPI
from WookieDb import WookieDb


class TrendAnalyser:

    def __init__(self, config_location="conf.json"):
        self.load_conf(config_location)
        self.load_api()

        self.db = WookieDb(self.conf['database_host'],
                           self.conf['database_username'],
                           self.conf['database_password'],
                           self.conf['database_schema'],
                           select_type='dict')

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

    def save_twitter_filter_data(self, json_data):
        time_folder = int(time.time() / 300) * 300

        filelocation = os.path.join(self.conf['save_data_location'],
                                "statuses/filter", str(time_folder),
                                str(int(time.time())) + "_" +
                                uuid.uuid4().hex +
                                ".json")
        self.save_data(json_data, filelocation)


    def start_stream_filter(self):
        terms = self._get_filter_keywords()

        print "Loading terms from database"
        print "Terms to download data for:"
        for term in terms:
            print term
        conjoined_terms = ','.join(terms)

        print "Starting to download data"
        response = self.api.request("statuses/filter", {"track" : conjoined_terms})

        items = 0
        item_data = []
        for item in response.get_iterator():
            items += 1
            item_data.append(item)

            if items > 1000:
                self.save_twitter_filter_data(item_data)
                item_data = []
                items = 0

    def _get_filter_keywords(self):
        terms = self.db.select("filter_status_terms", "*")
        combined_terms = []
        for term in terms:
            combined_terms.append(term['term_name'])

        return combined_terms

    def save_data(self, json_data, location):

        try:
            os.makedirs(os.path.dirname(location))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        json.dump(json_data, open(location, 'w'))

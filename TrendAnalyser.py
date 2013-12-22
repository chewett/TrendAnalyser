import json
import os
import time
import errno
import md5
import uuid

from TwitterAPI import TwitterAPI
from WookieDb import WookieDb


class TrendAnalyser:

    def __init__(self, config_location="conf.json", load_api=True):
        self.load_conf(config_location)
        if load_api:
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

    def _get_latest_trends(self):
        woeids = self.db.select("trend_top_list", "distinct(woeid)")
        latest_trends = {}
        for row in woeids:
            trend_details = self.db.select("trend_top_list", "*",
                                           "WHERE woeid = '" + str(row['woeid']) + "' " +
                                           "order by trend_top_list_id desc limit 1")
            trend_details = trend_details[0]

            trends = self.db.select("trend_top_list_trends",
                                    "*", "WHERE trend_top_list_id = '" + str(trend_details['trend_top_list_id']) + "'" );

            trend_details['trends'] = []
            for trend in trends:
                trend_details['trends'].append(trend)

            latest_trends[row['woeid']] = trend_details

        return latest_trends

    def _get_trending_details(self, search_term):
        details = self.db.select("trend_top_list l left join trend_top_list_trends t on t.trend_top_list_id = l.trend_top_list_id",
                                 "l.*, t.name, t.events, t.promoted_content",
                                 "WHERE name = '"+ search_term+"'")
        return details

    def download_trend_list(self, woeid):
        response = self.api.request("trends/place", {"id" : woeid})
        response_json = json.loads(response.text)[0]

        trend_top_list_data = {
            'woeid' : response_json['locations'][0]['woeid'],
            'as_of' : response_json['as_of'],
            'created_at' : response_json['created_at']
        }

        self.db.insert("trend_top_list", trend_top_list_data)
        trend_top_list_id = self.db.get_last_autoincrement()

        for trend in response_json['trends']:
            trend_data = {
                'trend_top_list_id' : trend_top_list_id,
                'name' : trend['name'],
                'events' : trend['events'],
                'promoted_content' : trend['promoted_content']
            }
            self.db.insert("trend_top_list_trends", trend_data)

        self.db.connection.commit()

    def save_data(self, json_data, location):

        try:
            os.makedirs(os.path.dirname(location))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        json.dump(json_data, open(location, 'w'))

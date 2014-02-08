'''
This is the main class that deals with the whole system. It exposes a number
of methods that can be accessed by the web interface
'''

import json
import os
import time
import errno
import md5
import uuid
from dateutil import parser
import calendar

from TwitterAPI import TwitterAPI
from WookieDb import WookieDb
from StreamMessage import StreamMessage
import _mysql_exceptions
from helpers import save_data, convert_to_unix

class TrendAnalyser:
    '''Holds all connection information with the database and Twitter'''

    def __init__(self, config_location="conf.json", load_api=True, load_db=True):
        '''Initialises the TrendAnalyser class object'''
        self.load_conf(config_location)
        self.api = None
        self.db = None
        self.conf = None
        
        if load_db:
            self.connect_to_db()
            self.load_db_conf()

        if load_api:
            self.load_api()

    def connect_to_db(self):
        '''Connects to the database using the details in conf'''
        self.db = WookieDb(self.conf['database_host'],
                           self.conf['database_username'],
                           self.conf['database_password'],
                           self.conf['database_schema'],
                           select_type='dict', charset="utf8")

    def load_conf(self, config_location):
        '''Loads the config from the given conf file location'''
        self.conf = {"debug" : False,
                     "offline": False}
        self.conf.update(json.load(open(config_location)))

    def load_db_conf(self):
        '''Accesses the DB and loads all the config details into the object'''
        db_options = self.db.select("options", "*")
        for option in db_options:
            value = option["value"]
            if value == "true":
                value = True
            elif value == "false":
                value = False

            self.conf[option['key']] = value

    def load_api(self):
        '''creates an instance of the TwitterAPI class to use'''
        details = json.load(open(self.conf['twitter_key_location']))

        self.api = TwitterAPI(details['consumer_key'],
                              details['consumer_secret'],
                              details['access_token_key'],
                              details['access_token_secret'])

    def save_trend_data(self, json_data, woeid):
        '''Saves Twitter Trend data to a json file'''
        filelocation = os.path.join(self.conf['save_data_location'],
                                "trends/place/weoid_" + str(woeid) + "_" +
                                str(int(time.time())) + ".json")
        save_data(json_data, filelocation)

    def save_twitter_sample_data(self, json_data):
        '''Saves data from the sample API to json files'''
        time_folder = int(time.time() / 300) * 300

        filelocation = os.path.join(self.conf['save_data_location'],
                                "statuses/sample", str(time_folder),
                                str(int(time.time())) + "_" +
                                md5.md5(json.dumps(json_data)).hexdigest() +
                                ".json")
        save_data(json_data, filelocation)

    def save_sample_data_db(self, json_data):
        '''Saves as little as possible from the sample API to the database'''
        msg = StreamMessage(json_data)

        if msg.get_type() == "tweet":
            if msg.data['entities']['hashtags'] != [] or msg.data['entities']['user_mentions'] != []:
                words = map(json.dumps, msg.data['text'].split(" "))
                where_clause = "WHERE word in (" + ",".join(words) + ");"

                positive = self.db.select("words_positive", "count(*)", where_clause)[0]["count(*)"]
                negative = self.db.select("words_negative", "count(*)", where_clause)[0]["count(*)"]

                tweet_details = {"tweetId" : msg.data['id'],
                                 "positive" : positive,
                                 "negative" : negative,
                                 "created_at" : convert_to_unix(msg.data['created_at'])}
                try:
                    self.db.insert("tweet_details", tweet_details)
                except _mysql_exceptions.IntegrityError as err:
                    if err[0] == 1062: #Duplicate error, ignore as twitter has resent the hashtag id
                        return
                    else:
                        raise

                for mention in msg.data['entities']['user_mentions']:
                    mention_details = {"tweetId": msg.data["id"],
                                       "user_id": mention["id"],
                                       "name" : mention["name"],
                                       "screen_name" : mention["screen_name"]}
                    try:
                        self.db.insert("tweet_mentions", mention_details)
                    except _mysql_exceptions.IntegrityError as err:
                        if err[0] == 1062: #Duplicate error, ignore it as they ahve put multiple mentions in the message
                            pass
                        else:
                            raise

                for hashtag in msg.get_hashtags():
                    tweet_hashtags = {"tweetId" : msg.data['id'], "hashtag" : hashtag}
                    try:
                        self.db.insert("tweet_hashtags", tweet_hashtags)
                    except _mysql_exceptions.IntegrityError as err:
                        if err[0] == 1062: #Duplicate error, ignore it as they have put multiple hashtags in the message
                            pass
                        else:
                            raise

                self.db.commit()

    def save_twitter_filter_data(self, json_data):
        '''Saves the given json data into the filter directory'''
        time_folder = int(time.time() / 300) * 300

        filelocation = os.path.join(self.conf['save_data_location'],
                                "statuses/filter", str(time_folder),
                                str(int(time.time())) + "_" +
                                uuid.uuid4().hex +
                                ".json")
        save_data(json_data, filelocation)

    def start_stream_filter(self):
        '''Gets the filter terms to search for them starts downloading them'''
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
        '''Get all the filter keywords from the database'''
        terms = self.db.select("filter_status_terms", "*")
        combined_terms = []
        for term in terms:
            combined_terms.append(term['term_name'])

        return combined_terms

    def _get_latest_trends(self):
        '''Gets the latest trending topics from each woeid'''
        woeids = self.db.select("trend_top_list", "distinct(woeid)")
        latest_trends = {}
        for row in woeids:
            trend_details = self.db.select("trend_top_list t "+
                                           "left join woeid_data w on t.woeid = w.woeid" ,
                                           "t.*, w.name",
                                           "WHERE t.woeid = '" + str(row['woeid']) + "' " +
                                           "order by t.trend_top_list_id desc limit 1")
            trend_details = trend_details[0]

            trends = self.db.select("trend_top_list_trends",
                                    "*", "WHERE trend_top_list_id = '" + str(trend_details['trend_top_list_id']) + "'" )

            trend_details['trends'] = []
            for trend in trends:
                trend_details['trends'].append(trend)

            latest_trends[row['woeid']] = trend_details

        return latest_trends

    def _get_trending_details(self, search_term):
        '''Gets all trending information for a specific search term'''
        details = self.db.select("trend_top_list l "+
                                 "left join trend_top_list_trends t on t.trend_top_list_id = l.trend_top_list_id " +
                                 "left join woeid_data w on l.woeid = w.woeid",
                                 "l.*, t.events, t.promoted_content, w.name as woeid_name",
                                 "WHERE t.name = '"+ search_term+"'")
        search_details = {'trends' : details, 'search_term' : search_term}
        return search_details

    def _get_hashtag_details(self, search_term):
        '''Gets the details about a specific hashtag from the database'''
        details = self.db.select("tweet_hashtags h left join tweet_details d on h.tweetId = d.tweetId", "d.*",
                                 "WHERE hashtag = '"+ search_term +"'")
        search_details = {'hashtags' : details, 'hashtag' : search_term}
        return search_details

    def _get_hashtag_frequency(self, search_term):
        '''Returns data about a hashtag's popularity over time'''
        time_period = 86400# seconds in a day

        details = self._get_hashtag_details(search_term)
        tweet_spikes = {}
        for hashtag in details['hashtags']:
            if hashtag['created_at'] is None:
                continue
            created_at = hashtag['created_at']

            if created_at / time_period in tweet_spikes:
                tweet_spikes[created_at / time_period] += 1
            else:
                tweet_spikes[created_at / time_period] = 1

        if not tweet_spikes:
            return []

        largest_value = max(tweet_spikes.keys())
        smallest_value = min(tweet_spikes.keys())
        for i in xrange(largest_value - smallest_value):
            if not smallest_value + i in tweet_spikes:
                tweet_spikes[smallest_value + i] = 0

        data = []
        for spike in tweet_spikes:
            data.append({"x": int(spike), "y": tweet_spikes[spike]})

        data.sort(key=lambda x : x['x'])

        return data

    def _get_mention_details(self, search_term):
        '''Returns data about a specific mention screenname'''
        details = self.db.select("tweet_mentions m left join tweet_details d on m.tweetId = d.tweetId",
                                 "d.*",
                                 "WHERE screen_name = '" + search_term +"'")
        search_details = {'mentions' : details, 'screen_name' : search_term}
        return search_details

    def _get_mention_frequency(self, search_term):
        '''Returns data about a mention's popularity over time'''
        time_period = 86400# seconds in a day

        details = self._get_mention_details(search_term)
        tweet_spikes = {}
        for mention in details['mentions']:
            if mention['created_at'] is None:
                continue
            created_at = mention['created_at']

            if created_at / time_period in tweet_spikes:
                tweet_spikes[created_at / time_period] += 1
            else:
                tweet_spikes[created_at / time_period] = 1

        if not tweet_spikes:
            return []

        largest_value = max(tweet_spikes.keys())
        smallest_value = min(tweet_spikes.keys())
        for i in xrange(largest_value - smallest_value):
            if not smallest_value + i in tweet_spikes:
                tweet_spikes[smallest_value + i] = 0

        data = []
        for spike in tweet_spikes:
            data.append({"x": int(spike), "y": tweet_spikes[spike]})

        data.sort(key=lambda x : x['x'])
        return data

    def _get_trending_woeids_downloading(self):
        '''Gets the details of woeids you want to download from the database'''
        return self.db.select("woeids_download d left join woeid_data w on d.woeid = w.woeid", "d.*, w.name")

    def download_trends(self):
        '''Downloads all the woeid data from the ones you want to download'''
        woeids = self.db.select("woeids_download", "*")
        for woeid in woeids:
            self.download_trend_list(woeid['woeid'])

    def download_trend_list(self, woeid):
        '''Saves one woeid data to the data'''
        response = self.api.request("trends/place", {"id" : woeid})
        response_json = json.loads(response.text)[0]

        trend_top_list_data = {
            'woeid' : response_json['locations'][0]['woeid'],
            'as_of' : convert_to_unix(response_json['as_of']),
            'created_at' : convert_to_unix(response_json['created_at'])
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

    def _update_woeid_data(self):
        '''Downloads all the avalible woeid data from Twitter and stores it'''
        response = self.api.request("trends/available")
        response_json = json.loads(response.text)

        for res in response_json:
            data = {"woeid" : res['woeid'],
                    "country" : res['country'],
                    "countryCode" : res['countryCode'],
                    "name" : res['name'],
                    "parentWoeid" : res['parentid'],
                    "placeCode" : res['placeType']['code'],
                    "placeName" : res['placeType']['name'],
                    "url" : res['url']}
            self.db.delete("woeid_data", "WHERE woeid = " + str(data['woeid']))
            self.db.insert("woeid_data", data)

        self.db.commit()

    def _get_woeid_data(self):
        '''Gets all woeid data from the database'''
        details = self.db.select("woeid_data", "*")
        return details

    def _get_words_positive(self):
        '''Gets all the positive words from the database'''
        details = self.db.select("words_positive", "*")
        return details

    def _get_words_negative(self):
        '''Gets all the negative words from the database'''
        details = self.db.select("words_negative", "*")
        return details

    def set_option(self, key, value):
        '''Allows you to set database options'''
        existing = self.db.select("options", "*", " WHERE options.key = '" + key + "' LIMIT 1;")
        if existing:
            self.db.update("options", {"value" : value}, "WHERE options.key = '" + key + "' LIMIT 1;")
        else:
            self.db.insert("options", {"options.key" : key, "value" : value})
        self.db.commit()

import json

class StreamMessage:

    def __init__(self, tweet_data):
        try: #assume they are passing in json
            self.data = json.loads(tweet_data)
        #if not json, assume its a dict and use it as the data
        except TypeError:
            self.data = tweet_data

    def get_type(self):
        try:
            if "delete" in self.data:
                return "delete"
        except KeyError:
            pass

        try:
            if "disconnect" in self.data:
                print "We have loaded a disconnect object and will close the program"
                print "Disconnect message payload:"
                print self.data['disconnect']
                exit()
        except KeyError:
            pass

        try:
            if "text" in self.data:
                return "tweet"
        except KeyError:
            pass

        return "unknown"

    def get_hashtags(self):
        hashtags = []
        for hashtag in self.data['entities']['hashtags']:
            hashtags.append(hashtag['text'])

        return hashtags

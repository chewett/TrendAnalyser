import json

class StreamMessage:

    def __init__(self, tweet_data, disconnect_closes=True):
        '''Sets up the StreamMessage object by passing in a json object'''
        try: #assume they are passing in json
            self.data = json.loads(tweet_data)
        #if not json, assume its a dict and use it as the data
        except TypeError:
            self.data = tweet_data

        self.disconnect_closes = disconnect_closes

    def get_type(self):
        '''Used to work out what type the message is'''
        try:
            if "delete" in self.data:
                return "delete"
        except KeyError:
            pass

        try:
            if "disconnect" in self.data:
                if self.disconnect_closes:
                    print "We have loaded a disconnect object and will close the program"
                    print "Disconnect message payload:"
                    print self.data['disconnect']
                    exit()
                else:
                    return "disconnect"
        except KeyError:
            pass

        try:
            if "text" in self.data:
                return "tweet"
        except KeyError:
            pass

        return "unknown"

    def get_hashtags(self):
        '''Used to get the hashtags out of the message'''
        hashtags = []
        for hashtag in self.data['entities']['hashtags']:
            hashtags.append(hashtag['text'])

        return hashtags

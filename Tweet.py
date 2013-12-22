import json

class TrendAnalyser:

    def __init__(self, tweet_data):
        self.data = json.loads(tweet_data)

    def get_type(self):
        if self.data['delete']:
            return "delete"
        else:
            return "unknown"

import json

class StreamMessage:

    def __init__(self, tweet_data):
        self.data = json.loads(tweet_data)

    def get_type(self):
        try:
            if "delete" in self.data:
                return "delete"
        except KeyError:
            pass

        try:
            if "text" in self.data:
                return "tweet"
        except KeyError:
            pass

        return "unknown"

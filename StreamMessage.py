import json

class StreamMessage:

    def __init__(self, tweet_data):
        self.data = json.loads(tweet_data)

    def get_type(self):
        if "delete" in self.data:
            return "delete"
        elif "text" in self.data:
            return "tweet"
        else:
            return "unknown"

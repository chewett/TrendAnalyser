import json
from time import gmtime, strftime
import datetime
import sys

from TrendAnalyser import TrendAnalyser

TA = TrendAnalyser()
response =TA.api.request("statuses/sample")

print "Starting to download streaming sample data"

for item in response.get_iterator():
    TA.save_twitter_sample_data(item)


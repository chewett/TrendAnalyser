import json
from time import gmtime, strftime
import datetime
import sys

from TrendAnalyser import TrendAnalyser

if len(sys.argv) == 2:
    keywords = sys.argv[1]
else:
    print "Cannot find keywords to filter and download"
    exit()

TA = TrendAnalyser()
response =TA.api.request("statuses/filter", {"track": keywords})

print "Starting to download streaming data matching:", keywords

for item in response.get_iterator():
    TA.save_twitter_filter_data(item)


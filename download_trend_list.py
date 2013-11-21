import json
from time import gmtime, strftime
import datetime
import sys

from TrendAnalyser import TrendAnalyser

if len(sys.argv) == 2:
    woeid = int(sys.argv[1])
else:
    woeid = 1 #worldwide

TA = TrendAnalyser()
response = TA.api.request("trends/place", {"id": woeid})
response_json = json.loads(response.text)


TA.save_trend_data(response_json, woeid)

print "Time: " + str(datetime.datetime.now())
print "Got trends for place woeid: " + str(woeid)


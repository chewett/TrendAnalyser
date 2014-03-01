import json
import time
from time import gmtime, strftime
import datetime
import sys
from dateutil import parser
import calendar

from TrendAnalyser import TrendAnalyser

TA = TrendAnalyser(load_api=False)
TA.load_api()

start_time = time.time()
print TA._get_trending_details("sochi")
end_time = time.time()

print "Time Taken:", end_time - start_time

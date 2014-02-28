import json
import time
from time import gmtime, strftime
import datetime
import sys
from dateutil import parser
import calendar

from TrendAnalyser import TrendAnalyser

start_time = time.time()
TA = TrendAnalyser(load_api=True, load_db=False)
end_time = time.time()

print "Time Taken:", end_time - start_time

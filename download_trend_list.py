import json
from time import gmtime, strftime
import datetime
import sys

from TrendAnalyser import TrendAnalyser

TA = TrendAnalyser()
TA.download_trends()

print "Time: " + str(datetime.datetime.now())


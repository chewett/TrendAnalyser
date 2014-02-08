'''
This script is used to download the current trends from the woeid locations
specified in the database table.
'''

import datetime

from TrendAnalyser import TrendAnalyser

TA = TrendAnalyser()
TA.download_trends()

print "Time: " + str(datetime.datetime.now())


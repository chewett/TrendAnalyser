import datetime

from TrendAnalyser import TrendAnalyser

TA = TrendAnalyser()
TA.download_trends()

print "Time: " + str(datetime.datetime.now())


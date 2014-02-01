from dateutil import parser
import calendar

from TrendAnalyser import TrendAnalyser
from WookieDb import WookieDb

TA = TrendAnalyser(load_api=False)

to_convert = TA.db.select("tweet_details", "*", "WHERE created_at_new = 0 LIMIT 10000")

for row in to_convert:
    timestamp = {"tweetId" : str(row['tweetId']),
                 "created_at" : "",
                 "created_at_new" :  str(calendar.timegm(parser.parse(row['created_at']).utctimetuple()))}

    TA.db.update("tweet_details", timestamp, "WHERE tweetId = '" + str(timestamp['tweetId']) + "' LIMIT 1")
   # print timestamp
   # print row

TA.db.commit()


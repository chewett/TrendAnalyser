from dateutil import parser
import calendar

from TrendAnalyser import TrendAnalyser
from WookieDb import WookieDb

TA = TrendAnalyser(load_api=False)

to_convert = TA.db.select("trend_top_list", "*", "WHERE created_at_new is NULL LIMIT 1000")

for row in to_convert:
    timestamp = {"trend_top_list_id" : str(row['trend_top_list_id']),
                 "as_of" : "",
                 "as_of_new" : str(TA._convert_to_unix(row['as_of'])),
                 "created_at" : "",
                 "created_at_new" :  str(TA._convert_to_unix(row['created_at']))}

    TA.db.update("trend_top_list", timestamp, "WHERE trend_top_list_id = '" + str(timestamp['trend_top_list_id']) + "' LIMIT 1")
    #print timestamp
    #print row

TA.db.commit()

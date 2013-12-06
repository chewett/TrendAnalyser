import json
from time import gmtime, strftime
import datetime
import sys

from TrendAnalyser import TrendAnalyser


TA = TrendAnalyser()
TA.start_stream_filter()

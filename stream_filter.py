'''
Starts up the streaming API request specific hashtags. The tags that are
downloaded are loaded from the database
'''

from TrendAnalyser import TrendAnalyser

TA = TrendAnalyser()
TA.start_stream_filter()

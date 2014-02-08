'''
This allows you to set database options using the command line
'''

import sys

from TrendAnalyser import TrendAnalyser

if len(sys.argv) == 3:
    key = sys.argv[1]
    value = sys.argv[2]
else:
    print "You must include a key and value to insert/modify this option"
    exit()

TA = TrendAnalyser(load_api=False)
TA.set_option(key, value)

print "Set the value of " + key + " to " + value

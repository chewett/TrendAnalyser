import sys
import os
import codecs

sys.path.append(".")
old_dir = os.getcwd()
os.chdir("../")

from TrendAnalyser import TrendAnalyser

TA = TrendAnalyser(load_db=False, load_api=False)
os.chdir(old_dir)


print TA.conf

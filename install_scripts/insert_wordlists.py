import sys
import os
import codecs

sys.path.append(".")
old_dir = os.getcwd()
os.chdir("../")

from TrendAnalyser import TrendAnalyser

TA = TrendAnalyser(load_api=False)
os.chdir(old_dir)

positive = open("positive-words.txt", "r")

for line in positive:
    fixed = line.rstrip("\n").decode("iso-8859-1")
    if fixed == "":
        continue
    elif fixed[0] == ";":
        continue

    #print fixed
    TA.db.insert("words_positive", {"word": fixed})

negative = open("negative-words.txt", "r")

for line in negative:
    fixed = line.rstrip("\n").decode("iso-8859-1")
    if fixed == "":
        continue
    elif fixed[0] == ";":
        continue

    #print fixed
    TA.db.insert("words_negative", {"word": fixed})

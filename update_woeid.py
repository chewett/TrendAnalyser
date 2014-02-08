'''
This downloads the data about which locations Twitter provide top the top 10
trending item lists from and stores the data in the database
'''

from TrendAnalyser import TrendAnalyser

TA = TrendAnalyser()
print TA._update_woeid_data()

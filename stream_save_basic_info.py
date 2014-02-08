from TrendAnalyser import TrendAnalyser

TA = TrendAnalyser()
response = TA.api.request("statuses/sample")

for item in response.get_iterator():
    TA.save_sample_data_db(item)

